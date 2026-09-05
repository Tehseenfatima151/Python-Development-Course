"""Product model."""
from datetime import datetime, timezone
from decimal import Decimal

from ..extensions import db


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    # Store price in cents (integer) to avoid floating-point issues.
    # All API inputs/outputs use decimal dollars; conversion happens in to_dict / from_price_dollars.
    price_cents = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    image_url = db.Column(db.String(512), nullable=True)
    category = db.Column(db.String(100), nullable=True, index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    cart_items = db.relationship("CartItem", back_populates="product")
    order_items = db.relationship("OrderItem", back_populates="product")

    # ------------------------------------------------------------------
    # Price helpers
    # ------------------------------------------------------------------

    @property
    def price(self) -> Decimal:
        """Return price as a Decimal in dollars."""
        return Decimal(self.price_cents) / 100

    @price.setter
    def price(self, value) -> None:
        """Accept dollars (float, str, or Decimal) and store as cents."""
        cents = int(round(Decimal(str(value)) * 100))
        if cents <= 0:
            raise ValueError("Price must be greater than zero")
        self.price_cents = cents

    # ------------------------------------------------------------------
    # Stock helpers
    # ------------------------------------------------------------------

    def decrease_stock(self, quantity: int) -> None:
        """Atomically decrease stock. Raises ValueError on insufficient stock."""
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        if self.stock < quantity:
            raise ValueError(
                f"Insufficient stock for product '{self.name}': "
                f"requested {quantity}, available {self.stock}"
            )
        self.stock -= quantity

    def increase_stock(self, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        self.stock += quantity

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": float(self.price),
            "stock": self.stock,
            "image_url": self.image_url,
            "category": self.category,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def __repr__(self) -> str:
        return f"<Product {self.id}: {self.name}>"
