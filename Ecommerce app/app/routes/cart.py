"""Cart routes — all require authentication."""
import logging

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..extensions import db
from ..models.cart import Cart, CartItem
from ..models.product import Product
from ..utils.validators import validate_quantity

logger = logging.getLogger(__name__)
cart_bp = Blueprint("cart", __name__)


def _get_user_id() -> int:
    """Return the current user's id as an integer from the JWT identity string."""
    return int(get_jwt_identity())


def _get_or_create_cart(user_id: int) -> Cart:
    """Return the user's cart, creating one if it does not exist."""
    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        cart = Cart(user_id=user_id)
        db.session.add(cart)
        db.session.flush()
    return cart


@cart_bp.route("", methods=["GET"])
@jwt_required()
def get_cart():
    """GET /api/cart — return current user's cart."""
    user_id = _get_user_id()
    cart = _get_or_create_cart(user_id)
    db.session.commit()
    return jsonify({"success": True, "data": {"cart": cart.to_dict()}}), 200


@cart_bp.route("/items", methods=["POST"])
@jwt_required()
def add_item():
    """POST /api/cart/items — add a product to the cart.

    If the product already exists in the cart the quantities are summed.
    Price is always read from the database — never from the request.
    """
    user_id = _get_user_id()
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"success": False, "message": "Request body must be JSON", "error": "INVALID_JSON"}), 400

    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)

    # Validate quantity
    valid, msg = validate_quantity(quantity)
    if not valid:
        return jsonify({"success": False, "message": msg, "error": "INVALID_QUANTITY"}), 400

    quantity = int(quantity)

    # Validate product exists
    product = db.session.get(Product, product_id)
    if not product:
        return jsonify({"success": False, "message": "Product not found", "error": "PRODUCT_NOT_FOUND"}), 404

    cart = _get_or_create_cart(user_id)

    # Check if item already in cart
    existing = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
    new_quantity = (existing.quantity if existing else 0) + quantity

    # Validate stock
    if new_quantity > product.stock:
        return jsonify({
            "success": False,
            "message": f"Insufficient stock. Available: {product.stock}",
            "error": "INSUFFICIENT_STOCK",
        }), 409

    if existing:
        existing.quantity = new_quantity
    else:
        item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity)
        db.session.add(item)

    db.session.commit()
    # Reload cart to get fresh totals
    db.session.refresh(cart)

    return jsonify({"success": True, "message": "Item added to cart", "data": {"cart": cart.to_dict()}}), 200


@cart_bp.route("/items/<int:product_id>", methods=["PUT"])
@jwt_required()
def update_item(product_id):
    """PUT /api/cart/items/<product_id> — set absolute quantity for a cart item."""
    user_id = _get_user_id()
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"success": False, "message": "Request body must be JSON", "error": "INVALID_JSON"}), 400

    quantity = data.get("quantity")
    valid, msg = validate_quantity(quantity)
    if not valid:
        return jsonify({"success": False, "message": msg, "error": "INVALID_QUANTITY"}), 400

    quantity = int(quantity)

    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        return jsonify({"success": False, "message": "Cart is empty", "error": "CART_EMPTY"}), 404

    item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
    if not item:
        return jsonify({"success": False, "message": "Item not in cart", "error": "ITEM_NOT_FOUND"}), 404

    product = db.session.get(Product, product_id)
    if quantity > product.stock:
        return jsonify({
            "success": False,
            "message": f"Insufficient stock. Available: {product.stock}",
            "error": "INSUFFICIENT_STOCK",
        }), 409

    item.quantity = quantity
    db.session.commit()
    db.session.refresh(cart)

    return jsonify({"success": True, "message": "Cart updated", "data": {"cart": cart.to_dict()}}), 200


@cart_bp.route("/items/<int:product_id>", methods=["DELETE"])
@jwt_required()
def remove_item(product_id):
    """DELETE /api/cart/items/<product_id> — remove a specific item from the cart."""
    user_id = _get_user_id()

    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        return jsonify({"success": False, "message": "Cart is empty", "error": "CART_EMPTY"}), 404

    item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
    if not item:
        return jsonify({"success": False, "message": "Item not in cart", "error": "ITEM_NOT_FOUND"}), 404

    db.session.delete(item)
    db.session.commit()
    db.session.refresh(cart)

    return jsonify({"success": True, "message": "Item removed from cart", "data": {"cart": cart.to_dict()}}), 200


@cart_bp.route("", methods=["DELETE"])
@jwt_required()
def clear_cart():
    """DELETE /api/cart — remove all items from the cart."""
    user_id = _get_user_id()

    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        return jsonify({"success": True, "message": "Cart is already empty"}), 200

    CartItem.query.filter_by(cart_id=cart.id).delete()
    db.session.commit()

    return jsonify({"success": True, "message": "Cart cleared", "data": {"cart": cart.to_dict()}}), 200
