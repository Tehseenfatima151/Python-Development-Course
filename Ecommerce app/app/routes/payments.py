"""Payment routes — Stripe Checkout and Webhook handler."""
import logging

import stripe
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..extensions import db
from ..models.cart import Cart, CartItem
from ..models.order import Order
from ..models.payment import Payment
from ..services.stripe_service import create_checkout_session, construct_webhook_event
from ..services.inventory_service import decrease_stock_for_order
from ..services.order_service import create_order_from_cart
from ..tasks.email_tasks import send_order_confirmation_email

logger = logging.getLogger(__name__)
payments_bp = Blueprint("payments", __name__)


@payments_bp.route("/create-checkout-session", methods=["POST"])
@jwt_required()
def create_checkout():
    """POST /api/payments/create-checkout-session

    Flow:
    1. Read user's cart (server-side)
    2. Create pending Order
    3. Create Stripe Checkout Session with order metadata
    4. Return the Stripe Checkout URL
    """
    user_id = int(get_jwt_identity())
    frontend_url = current_app.config.get("FRONTEND_URL", "http://localhost:5000")

    # Create order from cart (validates stock, calculates total server-side)
    try:
        order = create_order_from_cart(user_id)
    except ValueError as exc:
        return jsonify({"success": False, "message": str(exc), "error": "ORDER_CREATION_FAILED"}), 400

    # Build Stripe Checkout Session
    success_url = f"{frontend_url}/order-success.html?session_id={{CHECKOUT_SESSION_ID}}"
    cancel_url = f"{frontend_url}/order-cancel.html?order_id={order.id}"

    try:
        session = create_checkout_session(order, success_url, cancel_url)
    except stripe.error.StripeError as exc:
        logger.error("Stripe error creating checkout session for order id=%s: %s", order.id, exc)
        # Roll back the order we just created since payment setup failed
        db.session.delete(order)
        db.session.commit()
        return jsonify({
            "success": False,
            "message": "Payment provider error. Please try again.",
            "error": "STRIPE_ERROR",
        }), 502

    # Store the Stripe session ID on the order
    order.stripe_session_id = session.id
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Checkout session created",
        "data": {
            "checkout_url": session.url,
            "session_id": session.id,
            "order_id": order.id,
        },
    }), 200


@payments_bp.route("/webhook", methods=["POST"])
def stripe_webhook():
    """POST /api/payments/webhook — Stripe webhook endpoint.

    Security:
    - Signature is verified using STRIPE_WEBHOOK_SECRET before any processing.
    - Processing is idempotent: already-paid orders are skipped.

    Handles:
    - checkout.session.completed  → confirm payment, decrease stock, clear cart, queue email
    - payment_intent.succeeded    → update payment record
    - payment_intent.payment_failed → mark order as failed
    """
    payload = request.get_data()
    sig_header = request.headers.get("Stripe-Signature", "")
    webhook_secret = current_app.config["STRIPE_WEBHOOK_SECRET"]

    # ------------------------------------------------------------------ #
    # 1. Verify signature
    # ------------------------------------------------------------------ #
    try:
        event = construct_webhook_event(payload, sig_header, webhook_secret)
    except stripe.error.SignatureVerificationError:
        logger.warning("Webhook signature verification failed")
        return jsonify({"success": False, "message": "Invalid signature", "error": "INVALID_SIGNATURE"}), 400
    except Exception as exc:
        logger.error("Webhook payload parsing error: %s", exc)
        return jsonify({"success": False, "message": "Invalid payload", "error": "INVALID_PAYLOAD"}), 400

    event_type = event["type"]
    logger.info("Stripe webhook received: %s", event_type)

    # ------------------------------------------------------------------ #
    # 2. Route event type
    # ------------------------------------------------------------------ #
    if event_type == "checkout.session.completed":
        _handle_checkout_completed(event["data"]["object"])

    elif event_type == "payment_intent.succeeded":
        _handle_payment_intent_succeeded(event["data"]["object"])

    elif event_type == "payment_intent.payment_failed":
        _handle_payment_intent_failed(event["data"]["object"])

    else:
        logger.debug("Unhandled webhook event type: %s", event_type)

    # Always return 200 to acknowledge receipt to Stripe
    return jsonify({"success": True, "message": "Webhook received"}), 200


# ------------------------------------------------------------------ #
# Webhook event handlers (private)
# ------------------------------------------------------------------ #

def _handle_checkout_completed(session_obj: dict) -> None:
    """Process a successful checkout.session.completed event.

    IDEMPOTENCY: If the order is already paid, we log and return immediately
    without performing any side-effects.
    """
    stripe_session_id = session_obj.get("id")
    metadata = session_obj.get("metadata", {})
    order_id = metadata.get("order_id")

    if not order_id:
        logger.error("checkout.session.completed missing order_id in metadata: %s", session_obj)
        return

    order = db.session.get(Order, int(order_id))
    if not order:
        logger.error("checkout.session.completed: order id=%s not found", order_id)
        return

    # ---- IDEMPOTENCY CHECK ----
    if order.is_paid:
        logger.info(
            "checkout.session.completed: order id=%s already paid — skipping duplicate webhook",
            order_id,
        )
        return

    payment_intent_id = session_obj.get("payment_intent")
    amount_total = session_obj.get("amount_total", order.total_amount_cents)
    currency = session_obj.get("currency", "usd")

    try:
        # ---- Decrease inventory (inside a transaction) ----
        decrease_stock_for_order(order)

        # ---- Mark order as paid ----
        order.mark_paid()
        order.stripe_session_id = stripe_session_id

        # ---- Create or update Payment record ----
        payment = Payment.query.filter_by(order_id=order.id).first()
        if not payment:
            payment = Payment(
                order_id=order.id,
                stripe_session_id=stripe_session_id,
                stripe_payment_intent_id=payment_intent_id,
                amount_cents=amount_total,
                currency=currency,
                status="succeeded",
            )
            db.session.add(payment)
        else:
            payment.stripe_session_id = stripe_session_id
            payment.stripe_payment_intent_id = payment_intent_id
            payment.amount_cents = amount_total
            payment.status = "succeeded"

        # ---- Clear user's cart ----
        cart = Cart.query.filter_by(user_id=order.user_id).first()
        if cart:
            CartItem.query.filter_by(cart_id=cart.id).delete()

        db.session.commit()
        logger.info("Order id=%s marked as PAID, inventory decreased, cart cleared", order.id)

        # ---- Queue confirmation email (non-blocking) ----
        send_order_confirmation_email.delay(order.id)
        logger.info("Confirmation email task queued for order id=%s", order.id)

    except ValueError as exc:
        db.session.rollback()
        logger.error(
            "Failed to process checkout.session.completed for order id=%s: %s",
            order_id, exc,
        )
    except Exception as exc:
        db.session.rollback()
        logger.exception(
            "Unexpected error processing checkout.session.completed for order id=%s",
            order_id,
        )


def _handle_payment_intent_succeeded(pi_obj: dict) -> None:
    """Update Payment record when payment_intent.succeeded fires."""
    pi_id = pi_obj.get("id")
    metadata = pi_obj.get("metadata", {})
    order_id = metadata.get("order_id")

    if not order_id:
        return

    payment = Payment.query.filter_by(order_id=int(order_id)).first()
    if payment and payment.status != "succeeded":
        payment.stripe_payment_intent_id = pi_id
        payment.status = "succeeded"
        db.session.commit()
        logger.info("Payment record updated to succeeded for order id=%s", order_id)


def _handle_payment_intent_failed(pi_obj: dict) -> None:
    """Mark order as failed when payment_intent.payment_failed fires."""
    metadata = pi_obj.get("metadata", {})
    order_id = metadata.get("order_id")

    if not order_id:
        return

    order = db.session.get(Order, int(order_id))
    if not order:
        return

    if order.status == "pending":
        order.mark_failed()

        payment = Payment.query.filter_by(order_id=order.id).first()
        if not payment:
            payment = Payment(
                order_id=order.id,
                stripe_session_id=None,
                stripe_payment_intent_id=pi_obj.get("id"),
                amount_cents=pi_obj.get("amount", 0),
                currency=pi_obj.get("currency", "usd"),
                status="failed",
            )
            db.session.add(payment)
        else:
            payment.status = "failed"

        db.session.commit()
        logger.info("Order id=%s marked as FAILED after payment_intent.payment_failed", order_id)
