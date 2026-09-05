"""Shared pytest fixtures for the entire test suite."""
import json
import pytest

from app import create_app
from app.config import TestingConfig
from app.extensions import db as _db
from app.models.user import User
from app.models.product import Product
from app.models.cart import Cart, CartItem
from app.models.order import Order, OrderItem
from app.models.payment import Payment


# ------------------------------------------------------------------ #
# App / DB fixtures
# ------------------------------------------------------------------ #

@pytest.fixture(scope="session")
def app():
    """Create a test application using in-memory SQLite."""
    application = create_app(TestingConfig)
    return application


@pytest.fixture(scope="function")
def db(app):
    """Provide a fresh database for every test function."""
    with app.app_context():
        _db.create_all()
        yield _db
        _db.session.remove()
        _db.drop_all()


@pytest.fixture(scope="function")
def client(app, db):
    """Flask test client bound to a clean database."""
    return app.test_client()


# ------------------------------------------------------------------ #
# Helper: make authenticated requests
# ------------------------------------------------------------------ #

@pytest.fixture(scope="function")
def auth_headers(client):
    """Return a function that logs in and gives back JWT headers."""
    def _make(email, password):
        res = client.post(
            "/api/auth/login",
            json={"email": email, "password": password},
        )
        token = res.get_json()["data"]["access_token"]
        return {"Authorization": f"Bearer {token}"}
    return _make


# ------------------------------------------------------------------ #
# User fixtures
# ------------------------------------------------------------------ #

@pytest.fixture(scope="function")
def customer_user(db, app):
    with app.app_context():
        u = User(name="Test Customer", email="customer@test.com", role="customer")
        u.set_password("password123")
        db.session.add(u)
        db.session.commit()
        db.session.refresh(u)
        return u


@pytest.fixture(scope="function")
def admin_user(db, app):
    with app.app_context():
        u = User(name="Admin User", email="admin@test.com", role="admin")
        u.set_password("adminpass123")
        db.session.add(u)
        db.session.commit()
        db.session.refresh(u)
        return u


@pytest.fixture(scope="function")
def customer_token(client, customer_user):
    res = client.post(
        "/api/auth/login",
        json={"email": "customer@test.com", "password": "password123"},
    )
    return res.get_json()["data"]["access_token"]


@pytest.fixture(scope="function")
def admin_token(client, admin_user):
    res = client.post(
        "/api/auth/login",
        json={"email": "admin@test.com", "password": "adminpass123"},
    )
    return res.get_json()["data"]["access_token"]


@pytest.fixture(scope="function")
def customer_headers(customer_token):
    return {"Authorization": f"Bearer {customer_token}"}


@pytest.fixture(scope="function")
def admin_headers(admin_token):
    return {"Authorization": f"Bearer {admin_token}"}


# ------------------------------------------------------------------ #
# Product fixtures
# ------------------------------------------------------------------ #

@pytest.fixture(scope="function")
def sample_product(db, app):
    with app.app_context():
        p = Product(
            name="Test Laptop",
            description="A powerful test laptop",
            category="Electronics",
            image_url="https://example.com/laptop.jpg",
            stock=10,
        )
        p.price = 999.99
        db.session.add(p)
        db.session.commit()
        db.session.refresh(p)
        return p


@pytest.fixture(scope="function")
def sample_product_2(db, app):
    with app.app_context():
        p = Product(
            name="Test Mouse",
            description="An ergonomic test mouse",
            category="Electronics",
            stock=5,
        )
        p.price = 29.99
        db.session.add(p)
        db.session.commit()
        db.session.refresh(p)
        return p


# ------------------------------------------------------------------ #
# Cart fixture
# ------------------------------------------------------------------ #

@pytest.fixture(scope="function")
def cart_with_item(db, app, customer_user, sample_product):
    with app.app_context():
        cart = Cart(user_id=customer_user.id)
        db.session.add(cart)
        db.session.flush()
        item = CartItem(cart_id=cart.id, product_id=sample_product.id, quantity=2)
        db.session.add(item)
        db.session.commit()
        db.session.refresh(cart)
        return cart


# ------------------------------------------------------------------ #
# Order fixtures
# ------------------------------------------------------------------ #

@pytest.fixture(scope="function")
def pending_order(db, app, customer_user, sample_product):
    with app.app_context():
        order = Order(
            user_id=customer_user.id,
            status="pending",
            stripe_session_id="cs_test_pending_session",
        )
        order.total_amount = 1999.98
        db.session.add(order)
        db.session.flush()
        item = OrderItem(
            order_id=order.id,
            product_id=sample_product.id,
            product_name=sample_product.name,
            price_cents=sample_product.price_cents,
            quantity=2,
            subtotal_cents=sample_product.price_cents * 2,
        )
        db.session.add(item)
        db.session.commit()
        db.session.refresh(order)
        # Eagerly materialise items so the collection is populated in Python memory.
        # This lets tests access order.items[n].product_id without hitting a
        # lazy-load that would raise DetachedInstanceError once the session closes.
        loaded_items = [
            {"id": i.id, "product_id": i.product_id, "quantity": i.quantity,
             "product_name": i.product_name, "price_cents": i.price_cents}
            for i in order.items
        ]
        # Attach as a plain list so tests that only need the ids can use it
        # without an active session.
        order._loaded_item_dicts = loaded_items
        return order
