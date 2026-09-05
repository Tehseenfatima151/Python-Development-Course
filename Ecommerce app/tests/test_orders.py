"""Tests for order creation and retrieval."""
import pytest
from decimal import Decimal

from app.extensions import db
from app.models.cart import Cart, CartItem
from app.models.order import Order


class TestOrderCreation:
    def _add_to_cart(self, client, headers, product_id, quantity):
        return client.post("/api/cart/items",
                           json={"product_id": product_id, "quantity": quantity},
                           headers=headers)

    def test_create_order_from_cart(self, client, customer_headers, sample_product):
        self._add_to_cart(client, customer_headers, sample_product.id, 2)
        res = client.post("/api/orders", headers=customer_headers)
        data = res.get_json()
        assert res.status_code == 201
        assert data["success"] is True
        order = data["data"]["order"]
        assert order["status"] == "pending"
        assert len(order["items"]) == 1

    def test_order_total_is_calculated_server_side(self, client, customer_headers, sample_product):
        """Total must be server-calculated from DB prices, not from any client value."""
        self._add_to_cart(client, customer_headers, sample_product.id, 3)
        res = client.post("/api/orders", headers=customer_headers)
        order = res.get_json()["data"]["order"]
        expected_total = round(sample_product.price_cents * 3 / 100, 2)
        assert order["total_amount"] == pytest.approx(expected_total, rel=1e-4)

    def test_order_stores_price_snapshot(self, client, customer_headers, sample_product, app):
        """OrderItem must snapshot the product name and price at time of order."""
        self._add_to_cart(client, customer_headers, sample_product.id, 1)
        res = client.post("/api/orders", headers=customer_headers)
        order = res.get_json()["data"]["order"]
        item = order["items"][0]
        assert item["product_name"] == sample_product.name
        assert item["price"] == pytest.approx(float(sample_product.price), rel=1e-4)

    def test_snapshot_survives_product_update(self, client, customer_headers, admin_headers, sample_product):
        """Updating the product price after order creation must not change the order total."""
        self._add_to_cart(client, customer_headers, sample_product.id, 1)
        order_res = client.post("/api/orders", headers=customer_headers)
        original_total = order_res.get_json()["data"]["order"]["total_amount"]

        # Admin updates the price
        client.put(f"/api/products/{sample_product.id}",
                   json={"price": 1.00}, headers=admin_headers)

        # Re-fetch the order
        order_id = order_res.get_json()["data"]["order"]["id"]
        refetched = client.get(f"/api/orders/{order_id}", headers=customer_headers)
        assert refetched.get_json()["data"]["order"]["total_amount"] == pytest.approx(original_total)

    def test_empty_cart_rejected(self, client, customer_headers):
        res = client.post("/api/orders", headers=customer_headers)
        assert res.status_code == 400
        assert "empty" in res.get_json()["message"].lower()

    def test_order_requires_auth(self, client):
        res = client.post("/api/orders")
        assert res.status_code == 401

    def test_list_orders(self, client, customer_headers, sample_product):
        self._add_to_cart(client, customer_headers, sample_product.id, 1)
        client.post("/api/orders", headers=customer_headers)
        res = client.get("/api/orders", headers=customer_headers)
        data = res.get_json()
        assert res.status_code == 200
        assert len(data["data"]["orders"]) == 1

    def test_get_order_detail(self, client, customer_headers, sample_product):
        self._add_to_cart(client, customer_headers, sample_product.id, 1)
        order_res = client.post("/api/orders", headers=customer_headers)
        order_id = order_res.get_json()["data"]["order"]["id"]

        res = client.get(f"/api/orders/{order_id}", headers=customer_headers)
        assert res.status_code == 200
        assert res.get_json()["data"]["order"]["id"] == order_id

    def test_cannot_view_other_users_order(self, client, customer_headers, admin_headers, sample_product, admin_user):
        """A customer should not be able to view another user's order."""
        self._add_to_cart(client, customer_headers, sample_product.id, 1)
        order_res = client.post("/api/orders", headers=customer_headers)
        order_id = order_res.get_json()["data"]["order"]["id"]

        # admin_user tries to access customer's order via /api/orders (user-scoped)
        res = client.get(f"/api/orders/{order_id}", headers=admin_headers)
        assert res.status_code == 404  # admin not the owner

    def test_multi_item_order_total(self, client, customer_headers, sample_product, sample_product_2):
        self._add_to_cart(client, customer_headers, sample_product.id, 2)
        self._add_to_cart(client, customer_headers, sample_product_2.id, 3)
        res = client.post("/api/orders", headers=customer_headers)
        order = res.get_json()["data"]["order"]
        expected = round(
            (sample_product.price_cents * 2 + sample_product_2.price_cents * 3) / 100, 2
        )
        assert order["total_amount"] == pytest.approx(expected, rel=1e-4)
        assert len(order["items"]) == 2
