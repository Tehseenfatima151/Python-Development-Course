"""Product routes — public read, admin write."""
import logging

from flask import Blueprint, request, jsonify

from ..extensions import db
from ..models.product import Product
from ..utils.decorators import admin_required
from ..utils.validators import validate_price, validate_stock

logger = logging.getLogger(__name__)
products_bp = Blueprint("products", __name__)


@products_bp.route("", methods=["GET"])
def list_products():
    """GET /api/products — public; supports search, category, pagination, sorting."""
    search = request.args.get("search", "").strip()
    category = request.args.get("category", "").strip()
    sort_by = request.args.get("sort_by", "created_at")
    order = request.args.get("order", "desc")
    page = max(1, int(request.args.get("page", 1)))
    per_page = min(100, max(1, int(request.args.get("per_page", 12))))

    query = Product.query

    if search:
        query = query.filter(
            db.or_(
                Product.name.ilike(f"%{search}%"),
                Product.description.ilike(f"%{search}%"),
            )
        )
    if category:
        query = query.filter(Product.category.ilike(category))

    # Sorting
    sort_column_map = {
        "name": Product.name,
        "price": Product.price_cents,
        "created_at": Product.created_at,
        "stock": Product.stock,
    }
    sort_col = sort_column_map.get(sort_by, Product.created_at)
    query = query.order_by(sort_col.desc() if order == "desc" else sort_col.asc())

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "success": True,
        "data": {
            "products": [p.to_dict() for p in pagination.items],
            "pagination": {
                "page": pagination.page,
                "per_page": pagination.per_page,
                "total": pagination.total,
                "pages": pagination.pages,
                "has_next": pagination.has_next,
                "has_prev": pagination.has_prev,
            },
        },
    }), 200


@products_bp.route("/<int:product_id>", methods=["GET"])
def get_product(product_id):
    """GET /api/products/<id> — public."""
    product = db.session.get(Product, product_id)
    if not product:
        return jsonify({"success": False, "message": "Product not found", "error": "NOT_FOUND"}), 404
    return jsonify({"success": True, "data": {"product": product.to_dict()}}), 200


@products_bp.route("", methods=["POST"])
@admin_required
def create_product():
    """POST /api/products — admin only."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"success": False, "message": "Request body must be JSON", "error": "INVALID_JSON"}), 400

    errors = _validate_product_data(data, is_update=False)
    if errors:
        return jsonify({"success": False, "message": "Validation failed", "errors": errors}), 422

    product = Product(
        name=data["name"].strip(),
        description=data.get("description", ""),
        image_url=data.get("image_url", ""),
        category=data.get("category", ""),
    )
    product.price = data["price"]
    product.stock = int(data.get("stock", 0))

    db.session.add(product)
    db.session.commit()
    logger.info("Product created: id=%s name=%s", product.id, product.name)

    return jsonify({
        "success": True,
        "message": "Product created successfully",
        "data": {"product": product.to_dict()},
    }), 201


@products_bp.route("/<int:product_id>", methods=["PUT"])
@admin_required
def update_product(product_id):
    """PUT /api/products/<id> — admin only."""
    product = db.session.get(Product, product_id)
    if not product:
        return jsonify({"success": False, "message": "Product not found", "error": "NOT_FOUND"}), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"success": False, "message": "Request body must be JSON", "error": "INVALID_JSON"}), 400

    errors = _validate_product_data(data, is_update=True)
    if errors:
        return jsonify({"success": False, "message": "Validation failed", "errors": errors}), 422

    if "name" in data:
        product.name = data["name"].strip()
    if "description" in data:
        product.description = data["description"]
    if "price" in data:
        product.price = data["price"]
    if "stock" in data:
        product.stock = int(data["stock"])
    if "image_url" in data:
        product.image_url = data["image_url"]
    if "category" in data:
        product.category = data["category"]

    db.session.commit()
    logger.info("Product updated: id=%s", product.id)

    return jsonify({
        "success": True,
        "message": "Product updated successfully",
        "data": {"product": product.to_dict()},
    }), 200


@products_bp.route("/<int:product_id>", methods=["DELETE"])
@admin_required
def delete_product(product_id):
    """DELETE /api/products/<id> — admin only."""
    product = db.session.get(Product, product_id)
    if not product:
        return jsonify({"success": False, "message": "Product not found", "error": "NOT_FOUND"}), 404

    db.session.delete(product)
    db.session.commit()
    logger.info("Product deleted: id=%s", product_id)

    return jsonify({"success": True, "message": "Product deleted successfully"}), 200


# ------------------------------------------------------------------ #
# Helpers
# ------------------------------------------------------------------ #

def _validate_product_data(data: dict, is_update: bool) -> dict:
    errors = {}

    name = data.get("name")
    if not is_update or name is not None:
        if not name or not str(name).strip():
            errors["name"] = "Product name is required"

    price = data.get("price")
    if not is_update or price is not None:
        valid, msg = validate_price(price)
        if not valid:
            errors["price"] = msg

    stock = data.get("stock")
    if stock is not None:
        valid, msg = validate_stock(stock)
        if not valid:
            errors["stock"] = msg

    return errors
