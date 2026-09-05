"""Tests for the inventory service and stock management."""
import pytest

from app.extensions import db
from app.models.product import Product
from app.models.order import Order, OrderItem
from app.services.inventory_service import decrease_stock_for_order


class TestInventoryService:
    def test_stock_decreases_correctly(self, app, pending_order, sample_product):
        original_stock = sample_product.stock  # 10, order has qty=2

        with app.app_context():
            order = Order.query.get(pending_order.id)
            decrease_stock_for_order(order)
            db.session.commit()

            product = Product.query.get(sample_product.id)
            assert product.stock == original_stock - 2

    def test_stock_cannot_go_negative(self, app, customer_user, db):
        """If the order quantity exceeds stock, the function must raise and rollback."""
        with app.app_context():
            # Product with only 1 unit
            p = Product(name="Scarce Item", stock=1)
            p.price = 10.00
            db.session.add(p)
            db.session.flush()

            # Order trying to buy 5
            order = Order(user_id=customer_user.id, status="pending")
            order.total_amount = 50.00
            db.session.add(order)
            db.session.flush()

            item = OrderItem(
                order_id=order.id,
                product_id=p.id,
                product_name=p.name,
                price_cents=p.price_cents,
                quantity=5,
                subtotal_cents=p.price_cents * 5,
            )
            db.session.add(item)
            db.session.commit()

            with pytest.raises(ValueError, match="[Ii]nsufficient"):
                decrease_stock_for_order(order)

            # Stock must remain unchanged
            fresh = Product.query.get(p.id)
            assert fresh.stock == 1

    def test_transaction_rolled_back_on_failure(self, app, customer_user, db, sample_product):
        """A failure mid-decrease must leave the entire transaction rolled back."""
        with app.app_context():
            # Create two products; second has 0 stock
            p_ok = Product(name="Ok Product", stock=10)
            p_ok.price = 10.00
            p_zero = Product(name="Zero Stock", stock=0)
            p_zero.price = 5.00
            db.session.add_all([p_ok, p_zero])
            db.session.flush()

            order = Order(user_id=customer_user.id, status="pending")
            order.total_amount = 15.00
            db.session.add(order)
            db.session.flush()

            item_ok = OrderItem(
                order_id=order.id, product_id=p_ok.id,
                product_name=p_ok.name, price_cents=p_ok.price_cents,
                quantity=1, subtotal_cents=p_ok.price_cents,
            )
            item_bad = OrderItem(
                order_id=order.id, product_id=p_zero.id,
                product_name=p_zero.name, price_cents=p_zero.price_cents,
                quantity=1, subtotal_cents=p_zero.price_cents,
            )
            db.session.add_all([item_ok, item_bad])
            db.session.commit()

            with pytest.raises(ValueError):
                decrease_stock_for_order(order)

            # The "ok" product's stock should NOT have changed (rollback)
            fresh_ok = Product.query.get(p_ok.id)
            assert fresh_ok.stock == 10

    def test_product_model_decrease_stock_helper(self, app, sample_product):
        with app.app_context():
            p = Product.query.get(sample_product.id)
            original = p.stock
            p.decrease_stock(3)
            assert p.stock == original - 3

    def test_product_model_cannot_go_below_zero(self, app, sample_product):
        with app.app_context():
            p = Product.query.get(sample_product.id)
            with pytest.raises(ValueError):
                p.decrease_stock(p.stock + 100)

    def test_admin_can_update_stock(self, client, admin_headers, sample_product):
        res = client.patch(
            f"/api/admin/products/{sample_product.id}/stock",
            json={"stock": 50},
            headers=admin_headers,
        )
        assert res.status_code == 200
        assert res.get_json()["data"]["product"]["stock"] == 50

    def test_admin_stock_update_negative_rejected(self, client, admin_headers, sample_product):
        res = client.patch(
            f"/api/admin/products/{sample_product.id}/stock",
            json={"stock": -10},
            headers=admin_headers,
        )
        assert res.status_code == 422

    def test_cart_prevents_over_stock_on_add(self, client, customer_headers, sample_product):
        """Cart route must enforce stock limit before order creation."""
        res = client.post("/api/cart/items", json={
            "product_id": sample_product.id,
            "quantity": sample_product.stock + 1,  # one more than available
        }, headers=customer_headers)
        assert res.status_code == 409
        assert res.get_json()["error"] == "INSUFFICIENT_STOCK"
