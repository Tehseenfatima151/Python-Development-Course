"""Order and OrderItem models."""
from datetime import datetime, timezone
from decimal import Decimal

from ..extensions import db


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    # Total stored in cents to avoid floating-point issues
    total_amount_cents = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="pending")
    stripe_session_id = db.Column(db.String(255), unique=True, nullable=True, index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    user = db.relationship("User", back_populates="orders")
    items = db.relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    payment = db.relationship("Payment", back_populates="order", uselist=False, cascade="all, delete-orphan")

    # Valid status transitions
    VALID_STATUSES = ("pending", "paid", "cancelled", "failed")

    @property
    def total_amount(self) -> Decimal:
        return Decimal(self.total_amount_cents) / 100

    @total_amount.setter
    def total_amount(self, value) -> None:
        self.total_amount_cents = int(round(Decimal(str(value)) * 100))

    def mark_paid(self) -> None:
        self.status = "paid"

    def mark_cancelled(self) -> None:
        self.status = "cancelled"

    def mark_failed(self) -> None:
        self.status = "failed"

    @property
    def is_paid(self) -> bool:
        return self.status == "paid"

    def to_dict(self, include_items: bool = True) -> dict:
        data = {
            "id": self.id,
            "user_id": self.user_id,
            "total_amount": float(self.total_amount),
            "status": self.status,
            "stripe_session_id": self.stripe_session_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
        if include_items:
            data["items"] = [item.to_dict() for item in self.items]
        return data

    def __repr__(self) -> str:
        return f"<Order {self.id} status={self.status}>"


class OrderItem(db.Model):
    __tablename__ = "order_items"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=True)
    # Snapshot of product details at time of purchase — important for order history correctness
    product_name = db.Column(db.String(255), nullable=False)
    price_cents = db.Column(db.Integer, nullable=False)   # snapshot price in cents
    quantity = db.Column(db.Integer, nullable=False)
    subtotal_cents = db.Column(db.Integer, nullable=False)

    # Relationships
    order = db.relationship("Order", back_populates="items")
    product = db.relationship("Product", back_populates="order_items")

    @property
    def price(self) -> Decimal:
        return Decimal(self.price_cents) / 100

    @property
    def subtotal(self) -> Decimal:
        return Decimal(self.subtotal_cents) / 100

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "order_id": self.order_id,
            "product_id": self.product_id,
            "product_name": self.product_name,
            "price": float(self.price),
            "quantity": self.quantity,
            "subtotal": float(self.subtotal),
        }

    def __repr__(self) -> str:
        return f"<OrderItem {self.product_name} x{self.quantity}>"
