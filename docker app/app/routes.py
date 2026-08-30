"""
Application Routes

Registers all URL rules and view functions on the Flask application.
Keeping routes in a dedicated module (rather than inline in the factory)
makes them easier to read, test, and extend.
"""

from flask import Flask, jsonify
from flask.wrappers import Response


def register_routes(app: Flask) -> None:
    """
    Attach all route handlers to *app*.

    Args:
        app: The Flask application instance created by the factory.
    """

    @app.get("/")
    def index() -> tuple[Response, int]:
        """
        Root endpoint.

        Returns a JSON payload that confirms the application is running,
        along with the active environment label and a short status message.
        This is the primary endpoint visitors and monitoring tools hit first.
        """
        payload = {
            "application": app.config["APP_NAME"],
            "status": "running",
            "environment": app.config["FLASK_ENV"],
            "message": "Application is running successfully",
        }
        return jsonify(payload), 200

    @app.get("/health")
    def health() -> tuple[Response, int]:
        """
        Health check endpoint.

        Intentionally lightweight — no database calls or heavy computation.
        Used by Docker HEALTHCHECK, Render health probes, and CI/CD pipelines
        to verify the container is alive and accepting requests.
        """
        return jsonify({"status": "healthy"}), 200
