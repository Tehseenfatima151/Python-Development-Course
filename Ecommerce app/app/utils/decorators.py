"""Custom route decorators for authentication and authorization."""
from functools import wraps

from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

from ..extensions import db
from ..models.user import User


def admin_required(fn):
    """Decorator — requires a valid JWT and admin role."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        # JWT identity is stored as a string (PyJWT requires string sub claim);
        # convert back to int for the DB primary-key lookup.
        user_id = int(get_jwt_identity())
        user = db.session.get(User, user_id)
        if not user:
            return jsonify({"success": False, "message": "User not found", "error": "USER_NOT_FOUND"}), 404
        if not user.is_admin:
            return jsonify({"success": False, "message": "Admin privileges required", "error": "FORBIDDEN"}), 403
        return fn(*args, **kwargs)
    return wrapper


def get_current_user() -> User | None:
    """Return the current authenticated User object or None."""
    identity = get_jwt_identity()
    if identity is None:
        return None
    return db.session.get(User, int(identity))
