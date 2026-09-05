"""Payment model — records the Stripe payment result."""
from datetime import datetime, timezone
from decimal import Decimal

from ..extensions import db


class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False, unique=True)
    stripe_session_id = db.Column(db.String(255), nullable=True, index=True)
    stripe_payment_intent_id = db.Column(db.String(255), nullable=True, index=True)
    amount_cents = db.Column(db.Integer, nullable=False)
    currency = db.Column(db.String(10), nullable=False, default="usd")
    status = db.Column(db.String(30), nullable=False, default="pending")
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    order = db.relationship("Order", back_populates="payment")

    @property
    def amount(self) -> Decimal:
        return Decimal(self.amount_cents) / 100

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "order_id": self.order_id,
            "stripe_session_id": self.stripe_session_id,
            "stripe_payment_intent_id": self.stripe_payment_intent_id,
            "amount": float(self.amount),
            "currency": self.currency,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def __repr__(self) -> str:
        return f"<Payment order_id={self.order_id} status={self.status}>"
