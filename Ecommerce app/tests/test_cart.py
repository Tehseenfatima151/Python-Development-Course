"""Tests for the cart system."""
import pytest

from app.extensions import db
from app.models.cart import Cart, CartItem


class TestCartOperations:
    def test_get_empty_cart(self, client, customer_headers):
        """Cart is auto-created and returned empty."""
        res = client.get("/api/cart", headers=customer_headers)
        data = res.get_json()
        assert res.status_code == 200
        assert data["data"]["cart"]["items"] == []
        assert data["data"]["cart"]["total"] == 0.0

    def test_add_item_to_cart(self, client, customer_headers, sample_product):
        res = client.post("/api/cart/items", json={
            "product_id": sample_product.id,
            "quantity": 2,
        }, headers=customer_headers)
        data = res.get_json()
        assert res.status_code == 200
        assert data["success"] is True
        items = data["data"]["cart"]["items"]
        assert len(items) == 1
        assert items[0]["quantity"] == 2
        assert items[0]["product_id"] == sample_product.id

    def test_add_same_product_increases_quantity(self, client, customer_headers, sample_product):
        """Adding the same product twice should merge, not duplicate."""
        client.post("/api/cart/items", json={"product_id": sample_product.id, "quantity": 2},
                    headers=customer_headers)
        res = client.post("/api/cart/items", json={"product_id": sample_product.id, "quantity": 3},
                          headers=customer_headers)
        data = res.get_json()
        assert res.status_code == 200
        items = data["data"]["cart"]["items"]
        assert len(items) == 1
        assert items[0]["quantity"] == 5

    def test_update_item_quantity(self, client, customer_headers, sample_product):
        client.post("/api/cart/items", json={"product_id": sample_product.id, "quantity": 2},
                    headers=customer_headers)
        res = client.put(f"/api/cart/items/{sample_product.id}",
                         json={"quantity": 7}, headers=customer_headers)
        data = res.get_json()
        assert res.status_code == 200
        assert data["data"]["cart"]["items"][0]["quantity"] == 7

    def test_remove_item(self, client, customer_headers, sample_product):
        client.post("/api/cart/items", json={"product_id": sample_product.id, "quantity": 1},
                    headers=customer_headers)
        res = client.delete(f"/api/cart/items/{sample_product.id}", headers=customer_headers)
        assert res.status_code == 200
        cart = res.get_json()["data"]["cart"]
        assert len(cart["items"]) == 0

    def test_clear_cart(self, client, customer_headers, sample_product, sample_product_2):
        client.post("/api/cart/items", json={"product_id": sample_product.id, "quantity": 1},
                    headers=customer_headers)
        client.post("/api/cart/items", json={"product_id": sample_product_2.id, "quantity": 2},
                    headers=customer_headers)
        res = client.delete("/api/cart", headers=customer_headers)
        assert res.status_code == 200
        assert res.get_json()["data"]["cart"]["items"] == []

    def test_cannot_exceed_stock(self, client, customer_headers, sample_product):
        """sample_product has stock=10, trying to add 15 should fail."""
        res = client.post("/api/cart/items", json={
            "product_id": sample_product.id,
            "quantity": 15,
        }, headers=customer_headers)
        assert res.status_code == 409
        assert res.get_json()["error"] == "INSUFFICIENT_STOCK"

    def test_cannot_add_nonexistent_product(self, client, customer_headers):
        res = client.post("/api/cart/items", json={
            "product_id": 999999, "quantity": 1,
        }, headers=customer_headers)
        assert res.status_code == 404

    def test_zero_quantity_rejected(self, client, customer_headers, sample_product):
        res = client.post("/api/cart/items", json={
            "product_id": sample_product.id, "quantity": 0,
        }, headers=customer_headers)
        assert res.status_code == 400

    def test_negative_quantity_rejected(self, client, customer_headers, sample_product):
        res = client.post("/api/cart/items", json={
            "product_id": sample_product.id, "quantity": -3,
        }, headers=customer_headers)
        assert res.status_code == 400

    def test_cart_requires_auth(self, client):
        res = client.get("/api/cart")
        assert res.status_code == 401

    def test_cart_total_calculated_server_side(self, client, customer_headers, sample_product):
        """Cart total should equal quantity × DB price, regardless of any client values."""
        client.post("/api/cart/items", json={
            "product_id": sample_product.id, "quantity": 3,
        }, headers=customer_headers)
        res = client.get("/api/cart", headers=customer_headers)
        cart = res.get_json()["data"]["cart"]
        expected_total = round(sample_product.price_cents * 3 / 100, 2)
        assert cart["total"] == pytest.approx(expected_total, rel=1e-4)
