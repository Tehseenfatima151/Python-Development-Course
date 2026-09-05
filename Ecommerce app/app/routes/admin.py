"""Admin routes — all require admin role."""
import logging

from flask import Blueprint, request, jsonify

from ..extensions import db
from ..models.order import Order
from ..models.product import Product
from ..models.user import User
from ..utils.decorators import admin_required
from ..utils.validators import validate_price, validate_stock

logger = logging.getLogger(__name__)
admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/orders", methods=["GET"])
@admin_required
def list_all_orders():
    """GET /api/admin/orders — paginated list of all orders."""
    page = max(1, int(request.args.get("page", 1)))
    per_page = min(100, max(1, int(request.args.get("per_page", 20))))
    status = request.args.get("status", "").strip()

    query = Order.query
    if status:
        query = query.filter_by(status=status)
    query = query.order_by(Order.created_at.desc())

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "success": True,
        "data": {
            "orders": [o.to_dict() for o in pagination.items],
            "pagination": {
                "page": pagination.page,
                "per_page": pagination.per_page,
                "total": pagination.total,
                "pages": pagination.pages,
            },
        },
    }), 200


@admin_bp.route("/orders/<int:order_id>", methods=["GET"])
@admin_required
def get_order(order_id):
    """GET /api/admin/orders/<id> — full order detail."""
    order = db.session.get(Order, order_id)
    if not order:
        return jsonify({"success": False, "message": "Order not found", "error": "NOT_FOUND"}), 404
    return jsonify({"success": True, "data": {"order": order.to_dict()}}), 200


@admin_bp.route("/products/<int:product_id>/stock", methods=["PATCH"])
@admin_required
def update_stock(product_id):
    """PATCH /api/admin/products/<id>/stock — set absolute stock value."""
    product = db.session.get(Product, product_id)
    if not product:
        return jsonify({"success": False, "message": "Product not found", "error": "NOT_FOUND"}), 404

    data = request.get_json(silent=True)
    if not data or "stock" not in data:
        return jsonify({"success": False, "message": "stock field is required", "error": "MISSING_FIELD"}), 400

    valid, msg = validate_stock(data["stock"])
    if not valid:
        return jsonify({"success": False, "message": msg, "error": "INVALID_STOCK"}), 422

    old_stock = product.stock
    product.stock = int(data["stock"])
    db.session.commit()

    logger.info("Stock updated: product_id=%s %s→%s", product_id, old_stock, product.stock)
    return jsonify({
        "success": True,
        "message": "Stock updated",
        "data": {"product": product.to_dict()},
    }), 200


@admin_bp.route("/users", methods=["GET"])
@admin_required
def list_users():
    """GET /api/admin/users — list all users."""
    users = User.query.order_by(User.created_at.desc()).all()
    return jsonify({
        "success": True,
        "data": {"users": [u.to_dict() for u in users]},
    }), 200


@admin_bp.route("/stats", methods=["GET"])
@admin_required
def stats():
    """GET /api/admin/stats — dashboard summary stats."""
    from sqlalchemy import func

    total_products = Product.query.count()
    total_orders = Order.query.count()
    paid_orders = Order.query.filter_by(status="paid").count()
    total_users = User.query.count()

    revenue_cents = (
        db.session.query(func.sum(Order.total_amount_cents))
        .filter_by(status="paid")
        .scalar()
        or 0
    )

    return jsonify({
        "success": True,
        "data": {
            "total_products": total_products,
            "total_orders": total_orders,
            "paid_orders": paid_orders,
            "total_users": total_users,
            "total_revenue": revenue_cents / 100,
        },
    }), 200
