"""Application factory."""
import logging
import os

from flask import Flask, jsonify

from .config import get_config
from .extensions import db, migrate, jwt, cors, celery


def create_app(config_class=None):
    """Create and configure the Flask application."""
    app = Flask(__name__, static_folder="../frontend", static_url_path="")

    # Load configuration
    if config_class is None:
        config_class = get_config()
    app.config.from_object(config_class)

    # ------------------------------------------------------------------ #
    # Extensions
    # ------------------------------------------------------------------ #
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})

    # Configure Celery
    _init_celery(app)

    # ------------------------------------------------------------------ #
    # Logging
    # ------------------------------------------------------------------ #
    logging.basicConfig(
        level=logging.DEBUG if app.config.get("DEBUG") else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    # ------------------------------------------------------------------ #
    # Register blueprints
    # ------------------------------------------------------------------ #
    from .routes.auth import auth_bp
    from .routes.products import products_bp
    from .routes.cart import cart_bp
    from .routes.orders import orders_bp
    from .routes.payments import payments_bp
    from .routes.admin import admin_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(products_bp, url_prefix="/api/products")
    app.register_blueprint(cart_bp, url_prefix="/api/cart")
    app.register_blueprint(orders_bp, url_prefix="/api/orders")
    app.register_blueprint(payments_bp, url_prefix="/api/payments")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")

    # ------------------------------------------------------------------ #
    # JWT error handlers
    # ------------------------------------------------------------------ #
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"success": False, "message": "Token has expired", "error": "TOKEN_EXPIRED"}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"success": False, "message": "Invalid token", "error": "TOKEN_INVALID"}), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({"success": False, "message": "Authentication required", "error": "TOKEN_MISSING"}), 401

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify({"success": False, "message": "Token has been revoked", "error": "TOKEN_REVOKED"}), 401

    # ------------------------------------------------------------------ #
    # Global error handlers
    # ------------------------------------------------------------------ #
    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({"success": False, "message": str(e), "error": "BAD_REQUEST"}), 400

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"success": False, "message": "Resource not found", "error": "NOT_FOUND"}), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({"success": False, "message": "Method not allowed", "error": "METHOD_NOT_ALLOWED"}), 405

    @app.errorhandler(500)
    def internal_error(e):
        db.session.rollback()
        app.logger.error("Internal server error: %s", str(e))
        return jsonify({"success": False, "message": "Internal server error", "error": "INTERNAL_ERROR"}), 500

    # ------------------------------------------------------------------ #
    # Health check
    # ------------------------------------------------------------------ #
    @app.route("/api/health")
    def health():
        return jsonify({"success": True, "message": "OK", "data": {"status": "healthy"}})

    # Serve the frontend index for non-API routes
    @app.route("/")
    def index():
        return app.send_static_file("index.html")

    return app


def _init_celery(app: Flask):
    """Bind the global Celery instance to the Flask app context."""
    celery.conf.update(
        broker_url=app.config["CELERY_BROKER_URL"],
        result_backend=app.config["CELERY_RESULT_BACKEND"],
        task_always_eager=app.config.get("CELERY_TASK_ALWAYS_EAGER", False),
        task_eager_propagates=app.config.get("CELERY_TASK_EAGER_PROPAGATES", False),
        task_serializer="json",
        result_serializer="json",
        accept_content=["json"],
        timezone="UTC",
        enable_utc=True,
    )

    class ContextTask(celery.Task):
        """Ensure tasks run inside the Flask application context."""
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
