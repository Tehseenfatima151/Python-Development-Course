"""Tests for product CRUD endpoints."""
import pytest


class TestPublicProductAccess:
    def test_list_products_public(self, client, sample_product):
        """Anyone can list products — no auth required."""
        res = client.get("/api/products")
        data = res.get_json()
        assert res.status_code == 200
        assert data["success"] is True
        assert len(data["data"]["products"]) >= 1

    def test_get_product_by_id_public(self, client, sample_product):
        res = client.get(f"/api/products/{sample_product.id}")
        data = res.get_json()
        assert res.status_code == 200
        assert data["data"]["product"]["name"] == "Test Laptop"

    def test_get_nonexistent_product(self, client):
        res = client.get("/api/products/999999")
        assert res.status_code == 404

    def test_search_products(self, client, sample_product, sample_product_2):
        res = client.get("/api/products?search=Laptop")
        data = res.get_json()
        names = [p["name"] for p in data["data"]["products"]]
        assert "Test Laptop" in names
        assert "Test Mouse" not in names

    def test_filter_by_category(self, client, sample_product):
        res = client.get("/api/products?category=Electronics")
        data = res.get_json()
        assert all(p["category"] == "Electronics" for p in data["data"]["products"])

    def test_pagination_structure(self, client, sample_product):
        res = client.get("/api/products?page=1&per_page=5")
        pager = res.get_json()["data"]["pagination"]
        assert "page" in pager
        assert "total" in pager
        assert "pages" in pager


class TestAdminProductManagement:
    def test_admin_creates_product(self, client, admin_headers):
        res = client.post("/api/products", json={
            "name": "New Widget",
            "price": 49.99,
            "stock": 100,
            "category": "Gadgets",
            "description": "A shiny new widget",
        }, headers=admin_headers)
        data = res.get_json()
        assert res.status_code == 201
        assert data["success"] is True
        assert data["data"]["product"]["name"] == "New Widget"
        assert data["data"]["product"]["price"] == 49.99

    def test_admin_updates_product(self, client, admin_headers, sample_product):
        res = client.put(f"/api/products/{sample_product.id}", json={
            "name": "Updated Laptop",
            "price": 1199.99,
        }, headers=admin_headers)
        data = res.get_json()
        assert res.status_code == 200
        assert data["data"]["product"]["name"] == "Updated Laptop"
        assert data["data"]["product"]["price"] == 1199.99

    def test_admin_deletes_product(self, client, admin_headers, sample_product):
        res = client.delete(f"/api/products/{sample_product.id}", headers=admin_headers)
        assert res.status_code == 200
        # Verify it's gone
        assert client.get(f"/api/products/{sample_product.id}").status_code == 404

    def test_customer_cannot_create_product(self, client, customer_headers):
        res = client.post("/api/products", json={
            "name": "Unauthorized Product",
            "price": 9.99,
            "stock": 10,
        }, headers=customer_headers)
        assert res.status_code == 403

    def test_customer_cannot_delete_product(self, client, customer_headers, sample_product):
        res = client.delete(f"/api/products/{sample_product.id}", headers=customer_headers)
        assert res.status_code == 403

    def test_unauthenticated_cannot_create_product(self, client):
        res = client.post("/api/products", json={
            "name": "Sneaky Product", "price": 9.99, "stock": 10,
        })
        assert res.status_code == 401

    def test_invalid_price_rejected(self, client, admin_headers):
        res = client.post("/api/products", json={
            "name": "Bad Price Product", "price": -5.00, "stock": 10,
        }, headers=admin_headers)
        assert res.status_code == 422
        assert "price" in res.get_json()["errors"]

    def test_zero_price_rejected(self, client, admin_headers):
        res = client.post("/api/products", json={
            "name": "Zero Price", "price": 0, "stock": 10,
        }, headers=admin_headers)
        assert res.status_code == 422

    def test_negative_stock_rejected(self, client, admin_headers):
        res = client.post("/api/products", json={
            "name": "Bad Stock", "price": 10.00, "stock": -1,
        }, headers=admin_headers)
        assert res.status_code == 422
        assert "stock" in res.get_json()["errors"]

    def test_missing_name_rejected(self, client, admin_headers):
        res = client.post("/api/products", json={
            "price": 10.00, "stock": 5,
        }, headers=admin_headers)
        assert res.status_code == 422
        assert "name" in res.get_json()["errors"]
