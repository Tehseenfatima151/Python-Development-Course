"""
Tests for the Stripe webhook handler.

Covers:
- Signature verification (valid / invalid)
- checkout.session.completed happy path
- payment_intent.payment_failed
- IDEMPOTENCY: same webhook delivered twice must NOT:
  - mark the order paid twice
  - decrease stock twice
  - create duplicate payment records
  - queue the confirmation email more than once
"""
import json
import pytest
from unittest.mock import patch, MagicMock, call

from app.extensions import db
from app.models.order import Order
from app.models.payment import Payment
from app.models.product import Product


# ------------------------------------------------------------------ #
# Helpers
# ------------------------------------------------------------------ #

def _make_checkout_completed_event(order_id: int, session_id: str = "cs_test_webhook_session") -> dict:
    return {
        "type": "checkout.session.completed",
        "data": {
            "object": {
                "id": session_id,
                "payment_intent": "pi_test_payment_intent",
                "amount_total": 99999,
                "currency": "usd",
                "metadata": {
                    "order_id": str(order_id),
                    "user_id": "1",
                },
            }
        },
    }


def _make_payment_failed_event(order_id: int) -> dict:
    return {
        "type": "payment_intent.payment_failed",
        "data": {
            "object": {
                "id": "pi_test_failed",
                "amount": 99999,
                "currency": "usd",
                "metadata": {"order_id": str(order_id)},
            }
        },
    }


def _post_webhook(client, payload: dict):
    """Post a webhook with a mocked valid Stripe signature."""
    raw = json.dumps(payload).encode()
    with patch("app.routes.payments.construct_webhook_event") as mock_construct:
        mock_construct.return_value = payload
        return client.post(
            "/api/payments/webhook",
            data=raw,
            content_type="application/json",
            headers={"Stripe-Signature": "t=123,v1=fakesig"},
        )


# ------------------------------------------------------------------ #
# Signature verification tests
# ------------------------------------------------------------------ #

class TestWebhookSignature:
    def test_invalid_signature_returns_400(self, client):
        import stripe
        with patch("app.routes.payments.construct_webhook_event",
                   side_effect=stripe.error.SignatureVerificationError("bad sig", "sig_header")):
            res = client.post(
                "/api/payments/webhook",
                data=b'{"type":"checkout.session.completed"}',
                content_type="application/json",
                headers={"Stripe-Signature": "invalid"},
            )
        assert res.status_code == 400
        assert res.get_json()["error"] == "INVALID_SIGNATURE"

    def test_valid_webhook_returns_200(self, client, pending_order):
        payload = _make_checkout_completed_event(pending_order.id)
        with patch("app.tasks.email_tasks.send_order_confirmation_email"):
            res = _post_webhook(client, payload)
        assert res.status_code == 200


# ------------------------------------------------------------------ #
# checkout.session.completed happy path
# ------------------------------------------------------------------ #

class TestCheckoutCompleted:
    def test_order_marked_paid(self, client, app, pending_order):
        payload = _make_checkout_completed_event(pending_order.id)

        with patch("app.tasks.email_tasks.send_order_confirmation_email") as mock_email:
            mock_email.delay = MagicMock()
            res = _post_webhook(client, payload)

        assert res.status_code == 200

        with app.app_context():
            order = Order.query.get(pending_order.id)
            assert order.status == "paid"

    def test_stock_decreased_after_payment(self, client, app, pending_order, sample_product):
        """Stock must decrease by the ordered quantity after webhook."""
        original_stock = sample_product.stock  # 10
        payload = _make_checkout_completed_event(pending_order.id)

        with patch("app.tasks.email_tasks.send_order_confirmation_email"):
            _post_webhook(client, payload)

        with app.app_context():
            product = Product.query.get(sample_product.id)
            # pending_order has 2 units of sample_product
            assert product.stock == original_stock - 2

    def test_payment_record_created(self, client, app, pending_order):
        payload = _make_checkout_completed_event(pending_order.id)

        with patch("app.tasks.email_tasks.send_order_confirmation_email"):
            _post_webhook(client, payload)

        with app.app_context():
            payment = Payment.query.filter_by(order_id=pending_order.id).first()
            assert payment is not None
            assert payment.status == "succeeded"
            assert payment.stripe_payment_intent_id == "pi_test_payment_intent"

    def test_email_task_queued(self, client, pending_order):
        payload = _make_checkout_completed_event(pending_order.id)

        with patch("app.routes.payments.send_order_confirmation_email") as mock_task:
            mock_task.delay = MagicMock()
            _post_webhook(client, payload)
            mock_task.delay.assert_called_once_with(pending_order.id)

    def test_cart_cleared_after_payment(self, client, app, pending_order, customer_user):
        from app.models.cart import Cart, CartItem
        # pending_order.items may be detached; use the pre-loaded dict list instead.
        first_item_product_id = pending_order._loaded_item_dicts[0]["product_id"]

        # Create a cart with items for the user
        with app.app_context():
            cart = Cart.query.filter_by(user_id=customer_user.id).first()
            if not cart:
                cart = Cart(user_id=customer_user.id)
                db.session.add(cart)
                db.session.flush()
            item = CartItem(cart_id=cart.id, product_id=first_item_product_id, quantity=1)
            db.session.add(item)
            db.session.commit()

        payload = _make_checkout_completed_event(pending_order.id)
        with patch("app.tasks.email_tasks.send_order_confirmation_email"):
            _post_webhook(client, payload)

        with app.app_context():
            cart = Cart.query.filter_by(user_id=customer_user.id).first()
            if cart:
                assert len(cart.items) == 0


# ------------------------------------------------------------------ #
# IDEMPOTENCY — duplicate webhook delivery
# ------------------------------------------------------------------ #

class TestWebhookIdempotency:
    def test_duplicate_webhook_order_paid_only_once(self, client, app, pending_order):
        """Send the same webhook twice — order should only be paid once."""
        payload = _make_checkout_completed_event(pending_order.id)

        with patch("app.tasks.email_tasks.send_order_confirmation_email"):
            _post_webhook(client, payload)
            res2 = _post_webhook(client, payload)

        # Second call still returns 200 (safe acknowledgement)
        assert res2.status_code == 200

        with app.app_context():
            order = Order.query.get(pending_order.id)
            assert order.status == "paid"

    def test_duplicate_webhook_stock_decreased_only_once(self, client, app, pending_order, sample_product):
        """Stock must decrease exactly once even if the webhook fires twice."""
        original_stock = sample_product.stock  # 10
        payload = _make_checkout_completed_event(pending_order.id)

        with patch("app.tasks.email_tasks.send_order_confirmation_email"):
            _post_webhook(client, payload)
            _post_webhook(client, payload)

        with app.app_context():
            product = Product.query.get(sample_product.id)
            assert product.stock == original_stock - 2  # NOT original_stock - 4

    def test_duplicate_webhook_no_duplicate_payment_record(self, client, app, pending_order):
        """Only one Payment record should exist after two identical webhooks."""
        payload = _make_checkout_completed_event(pending_order.id)

        with patch("app.tasks.email_tasks.send_order_confirmation_email"):
            _post_webhook(client, payload)
            _post_webhook(client, payload)

        with app.app_context():
            payments = Payment.query.filter_by(order_id=pending_order.id).all()
            assert len(payments) == 1

    def test_duplicate_webhook_email_queued_only_once(self, client, pending_order):
        """The confirmation email task must be queued exactly once."""
        payload = _make_checkout_completed_event(pending_order.id)

        with patch("app.routes.payments.send_order_confirmation_email") as mock_task:
            mock_task.delay = MagicMock()
            _post_webhook(client, payload)
            _post_webhook(client, payload)
            assert mock_task.delay.call_count == 1


# ------------------------------------------------------------------ #
# payment_intent.payment_failed
# ------------------------------------------------------------------ #

class TestPaymentFailed:
    def test_order_marked_failed(self, client, app, pending_order):
        payload = _make_payment_failed_event(pending_order.id)
        res = _post_webhook(client, payload)
        assert res.status_code == 200

        with app.app_context():
            order = Order.query.get(pending_order.id)
            assert order.status == "failed"

    def test_stock_not_decreased_on_failure(self, client, app, pending_order, sample_product):
        """Stock must NOT be touched when payment fails."""
        original_stock = sample_product.stock
        payload = _make_payment_failed_event(pending_order.id)
        _post_webhook(client, payload)

        with app.app_context():
            product = Product.query.get(sample_product.id)
            assert product.stock == original_stock

    def test_unknown_event_type_returns_200(self, client):
        """Unhandled event types should be acknowledged gracefully."""
        payload = {"type": "some.unknown.event", "data": {"object": {}}}
        res = _post_webhook(client, payload)
        assert res.status_code == 200
