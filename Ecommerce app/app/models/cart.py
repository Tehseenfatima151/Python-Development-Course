"""Cart and CartItem models."""
from datetime import datetime, timezone
from decimal import Decimal

from ..extensions import db


class Cart(db.Model):
    __tablename__ = "carts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    user = db.relationship("User", back_populates="cart")
    items = db.relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")

    @property
    def total(self) -> Decimal:
        """Calculate cart total from current database prices (never from frontend)."""
        return sum(item.subtotal for item in self.items)

    def to_dict(self) -> dict:
        items = [item.to_dict() for item in self.items]
        return {
            "id": self.id,
            "user_id": self.user_id,
            "items": items,
            "total": float(self.total),
            "item_count": len(items),
            "updated_at": self.updated_at.isoformat(),
        }

    def __repr__(self) -> str:
        return f"<Cart user_id={self.user_id} items={len(self.items)}>"


class CartItem(db.Model):
    __tablename__ = "cart_items"

    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey("carts.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    # A product should only appear once per cart
    __table_args__ = (
        db.UniqueConstraint("cart_id", "product_id", name="uq_cart_item_cart_product"),
    )

    # Relationships
    cart = db.relationship("Cart", back_populates="items")
    product = db.relationship("Product", back_populates="cart_items")

    @property
    def subtotal(self) -> Decimal:
        """Subtotal calculated from current product price in the database."""
        return self.product.price * self.quantity

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "cart_id": self.cart_id,
            "product_id": self.product_id,
            "product_name": self.product.name,
            "product_image": self.product.image_url,
            "price": float(self.product.price),
            "quantity": self.quantity,
            "subtotal": float(self.subtotal),
            "stock_available": self.product.stock,
        }

    def __repr__(self) -> str:
        return f"<CartItem product_id={self.product_id} qty={self.quantity}>"
