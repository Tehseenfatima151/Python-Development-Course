"""Order creation service — all business logic lives here, not in routes."""
import logging
from decimal import Decimal

from ..extensions import db
from ..models.cart import Cart, CartItem
from ..models.order import Order, OrderItem
from ..models.product import Product

logger = logging.getLogger(__name__)


def create_order_from_cart(user_id: int) -> Order:
    """Create a pending Order from the user's current cart.

    Rules enforced here:
    - Cart must not be empty.
    - Every product must still exist.
    - Every product must have sufficient stock (re-verified at order creation).
    - Total is calculated server-side from current DB prices.
    - Product name and price are snapshotted into OrderItem.

    The cart is NOT cleared here — it is cleared only after payment confirmation.

    Raises:
        ValueError: on empty cart, missing product, or insufficient stock.
    """
    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart or not cart.items:
        raise ValueError("Cart is empty")

    total_cents = 0
    order_items = []

    for cart_item in cart.items:
        product = db.session.get(Product, cart_item.product_id)
        if not product:
            raise ValueError(f"Product id={cart_item.product_id} no longer exists")

        if cart_item.quantity > product.stock:
            raise ValueError(
                f"Insufficient stock for '{product.name}': "
                f"requested {cart_item.quantity}, available {product.stock}"
            )

        item_subtotal_cents = product.price_cents * cart_item.quantity
        total_cents += item_subtotal_cents

        order_items.append(OrderItem(
            product_id=product.id,
            product_name=product.name,        # snapshot
            price_cents=product.price_cents,  # snapshot
            quantity=cart_item.quantity,
            subtotal_cents=item_subtotal_cents,
        ))

    order = Order(
        user_id=user_id,
        total_amount_cents=total_cents,
        status="pending",
    )
    db.session.add(order)
    db.session.flush()  # get order.id before adding items

    for item in order_items:
        item.order_id = order.id
        db.session.add(item)

    db.session.commit()
    logger.info(
        "Order created: id=%s user_id=%s total=$%.2f",
        order.id, user_id, order.total_amount,
    )
    return order
