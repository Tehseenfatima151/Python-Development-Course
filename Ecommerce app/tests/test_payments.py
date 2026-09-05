"""Tests for Stripe checkout session creation and API error handling."""
import pytest
from unittest.mock import patch, MagicMock


def _add_and_create_order(client, customer_headers, product_id):
    """Helper: add product to cart, then create an order."""
    client.post("/api/cart/items",
                json={"product_id": product_id, "quantity": 1},
                headers=customer_headers)
    res = client.post("/api/orders", headers=customer_headers)
    return res.get_json()["data"]["order"]["id"]


class TestCheckoutSessionCreation:
    def test_create_checkout_session_success(self, client, customer_headers, sample_product):
        """Should create a Stripe session and return a checkout URL."""
        mock_session = MagicMock()
        mock_session.id = "cs_test_mock_session_id"
        mock_session.url = "https://checkout.stripe.com/pay/cs_test_mock_session_id"

        with patch("app.routes.payments.create_checkout_session", return_value=mock_session):
            client.post("/api/cart/items",
                        json={"product_id": sample_product.id, "quantity": 1},
                        headers=customer_headers)
            res = client.post("/api/payments/create-checkout-session", headers=customer_headers)

        data = res.get_json()
        assert res.status_code == 200
        assert data["success"] is True
        assert "checkout_url" in data["data"]
        assert data["data"]["session_id"] == "cs_test_mock_session_id"
        assert data["data"]["order_id"] is not None

    def test_checkout_requires_auth(self, client):
        res = client.post("/api/payments/create-checkout-session")
        assert res.status_code == 401

    def test_checkout_with_empty_cart_rejected(self, client, customer_headers):
        res = client.post("/api/payments/create-checkout-session", headers=customer_headers)
        assert res.status_code == 400
        assert "empty" in res.get_json()["message"].lower()

    def test_stripe_api_failure_returns_502(self, client, customer_headers, sample_product):
        """If Stripe raises an error, the API should return 502 and not leave a dangling order."""
        import stripe

        with patch("app.routes.payments.create_checkout_session",
                   side_effect=stripe.error.StripeError("Network error")):
            client.post("/api/cart/items",
                        json={"product_id": sample_product.id, "quantity": 1},
                        headers=customer_headers)
            res = client.post("/api/payments/create-checkout-session", headers=customer_headers)

        assert res.status_code == 502
        assert res.get_json()["error"] == "STRIPE_ERROR"

    def test_order_created_with_pending_status(self, client, customer_headers, sample_product):
        """The order created during checkout must initially be 'pending'."""
        mock_session = MagicMock()
        mock_session.id = "cs_test_pending"
        mock_session.url = "https://checkout.stripe.com/pay/cs_test_pending"

        with patch("app.routes.payments.create_checkout_session", return_value=mock_session):
            client.post("/api/cart/items",
                        json={"product_id": sample_product.id, "quantity": 1},
                        headers=customer_headers)
            res = client.post("/api/payments/create-checkout-session", headers=customer_headers)

        order_id = res.get_json()["data"]["order_id"]
        order_res = client.get(f"/api/orders/{order_id}", headers=customer_headers)
        assert order_res.get_json()["data"]["order"]["status"] == "pending"
