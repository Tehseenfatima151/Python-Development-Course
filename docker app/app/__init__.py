"""
Flask Application Factory

This module creates and configures the Flask application instance.
Using the application factory pattern allows for easier testing and
configuration management across different environments.
"""

from flask import Flask

from app.config import get_config
from app.routes import register_routes


def create_app(config_name: str | None = None) -> Flask:
    """
    Create and configure a Flask application instance.

    Args:
        config_name: Optional configuration environment name.
                     Defaults to the value of FLASK_ENV env var, or 'development'.

    Returns:
        Configured Flask application instance.
    """
    app = Flask(__name__)

    # Load configuration from the appropriate config class
    config = get_config(config_name)
    app.config.from_object(config)

    # Register all application routes
    register_routes(app)

    return app
