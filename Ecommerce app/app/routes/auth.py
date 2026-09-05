"""Authentication routes: register, login, me, logout."""
import logging

from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
)

from ..extensions import db
from ..models.user import User
from ..utils.validators import validate_email, validate_password

logger = logging.getLogger(__name__)
auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    """POST /api/auth/register — create a new customer account."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"success": False, "message": "Request body must be JSON", "error": "INVALID_JSON"}), 400

    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    role = data.get("role", "customer")

    # --- Validation ---
    errors = {}
    if not name:
        errors["name"] = "Name is required"
    if not validate_email(email):
        errors["email"] = "A valid email address is required"
    valid_pw, pw_msg = validate_password(password)
    if not valid_pw:
        errors["password"] = pw_msg
    # Only allow "customer" through public registration
    if role not in ("customer", "admin"):
        role = "customer"

    if errors:
        return jsonify({"success": False, "message": "Validation failed", "errors": errors}), 422

    # --- Uniqueness check ---
    if User.query.filter_by(email=email).first():
        return jsonify({"success": False, "message": "Email already registered", "error": "EMAIL_TAKEN"}), 409

    # --- Create user ---
    user = User(name=name, email=email, role="customer")
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    token = create_access_token(identity=str(user.id))
    logger.info("New user registered: %s (id=%s)", user.email, user.id)

    return jsonify({
        "success": True,
        "message": "Account created successfully",
        "data": {"user": user.to_dict(), "access_token": token},
    }), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    """POST /api/auth/login — authenticate and return JWT."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"success": False, "message": "Request body must be JSON", "error": "INVALID_JSON"}), 400

    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"success": False, "message": "Email and password are required", "error": "MISSING_CREDENTIALS"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        # Generic message to avoid user enumeration
        return jsonify({"success": False, "message": "Invalid email or password", "error": "INVALID_CREDENTIALS"}), 401

    token = create_access_token(identity=str(user.id))
    logger.info("User logged in: %s (id=%s)", user.email, user.id)

    return jsonify({
        "success": True,
        "message": "Login successful",
        "data": {"user": user.to_dict(), "access_token": token},
    }), 200


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    """GET /api/auth/me — return the current authenticated user's profile."""
    user_id = get_jwt_identity()
    user = db.session.get(User, int(user_id))
    if not user:
        return jsonify({"success": False, "message": "User not found", "error": "USER_NOT_FOUND"}), 404

    return jsonify({"success": True, "data": {"user": user.to_dict()}}), 200


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    """POST /api/auth/logout — client-side logout (token blacklisting not implemented; instruct client to discard token)."""
    return jsonify({"success": True, "message": "Logged out successfully"}), 200
