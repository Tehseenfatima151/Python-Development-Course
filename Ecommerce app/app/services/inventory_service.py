"""Inventory management service.

Strategy:
- Stock is only decreased AFTER verified Stripe payment confirmation.
- All decrements happen inside a single database transaction.
- We re-verify stock at the time of decrement to handle race conditions.
- If any product has insufficient stock at payment time, we log the error
  and raise so the webhook handler can keep the database consistent.
- SELECT … FOR UPDATE is used to lock the product row during the decrement
  (effective with PostgreSQL; SQLite silently ignores it).
"""
import logging

from sqlalchemy import select

from ..extensions import db
from ..models.order import Order
from ..models.product import Product

logger = logging.getLogger(__name__)


def decrease_stock_for_order(order: Order) -> None:
    """Decrease product stock for each OrderItem in the given paid order.

    Uses SELECT FOR UPDATE to prevent concurrent double-decrements on
    PostgreSQL. Rolls back and raises if stock is insufficient for any item.
    """
    try:
        for item in order.items:
            # Lock the product row for this transaction (SQLAlchemy 2.x style).
            product = db.session.execute(
                select(Product)
                .where(Product.id == item.product_id)
                .with_for_update()
            ).scalar_one_or_none()

            if not product:
                logger.error(
                    "Product id=%s not found during stock decrease for order id=%s",
                    item.product_id, order.id,
                )
                raise ValueError(f"Product id={item.product_id} not found")

            if product.stock < item.quantity:
                logger.error(
                    "Insufficient stock for product '%s' (id=%s) during order id=%s: "
                    "need %s, have %s",
                    product.name, product.id, order.id, item.quantity, product.stock,
                )
                raise ValueError(
                    f"Insufficient stock for '{product.name}': "
                    f"need {item.quantity}, have {product.stock}"
                )

            product.stock -= item.quantity
            logger.debug(
                "Stock decreased: product_id=%s name=%s qty=%s remaining=%s",
                product.id, product.name, item.quantity, product.stock,
            )

        db.session.flush()
        logger.info("Stock decreased successfully for order id=%s", order.id)

    except Exception:
        db.session.rollback()
        logger.exception(
            "Stock decrease failed for order id=%s — transaction rolled back", order.id
        )
        raise
