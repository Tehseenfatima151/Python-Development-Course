"""Order routes."""
import logging

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..models.order import Order
from ..services.order_service import create_order_from_cart

logger = logging.getLogger(__name__)
orders_bp = Blueprint("orders", __name__)


def _get_user_id() -> int:
    """Return the current user's id as an integer from the JWT identity string."""
    return int(get_jwt_identity())


@orders_bp.route("", methods=["POST"])
@jwt_required()
def create_order():
    """POST /api/orders — create a pending order from the user's cart.

    The total is calculated server-side. Cart is NOT cleared here;
    it will be cleared by the webhook after payment confirmation.
    """
    user_id = _get_user_id()

    try:
        order = create_order_from_cart(user_id)
    except ValueError as exc:
        return jsonify({"success": False, "message": str(exc), "error": "ORDER_CREATION_FAILED"}), 400

    return jsonify({
        "success": True,
        "message": "Order created successfully",
        "data": {"order": order.to_dict()},
    }), 201


@orders_bp.route("", methods=["GET"])
@jwt_required()
def list_orders():
    """GET /api/orders — list the current user's orders, most recent first."""
    user_id = _get_user_id()
    orders = (
        Order.query
        .filter_by(user_id=user_id)
        .order_by(Order.created_at.desc())
        .all()
    )
    return jsonify({
        "success": True,
        "data": {"orders": [o.to_dict(include_items=False) for o in orders]},
    }), 200


@orders_bp.route("/<int:order_id>", methods=["GET"])
@jwt_required()
def get_order(order_id):
    """GET /api/orders/<id> — get full order details (user's own orders only)."""
    user_id = _get_user_id()
    order = Order.query.filter_by(id=order_id, user_id=user_id).first()
    if not order:
        return jsonify({"success": False, "message": "Order not found", "error": "NOT_FOUND"}), 404

    return jsonify({"success": True, "data": {"order": order.to_dict()}}), 200
