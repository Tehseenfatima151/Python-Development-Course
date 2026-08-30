"""
Automated Tests for the Flask Application

Uses Flask's built-in test client — no running server is required.
All tests execute against the 'testing' configuration so debug output
and test helpers are enabled while secrets remain safe fixed values.

Run the suite with:
    pytest
or for verbose output:
    pytest -v
"""

import json
import pytest

from app import create_app


@pytest.fixture
def client():
    """
    Provide a Flask test client configured for the testing environment.

    The fixture creates a fresh application instance per test function,
    ensuring tests remain isolated from one another.
    """
    app = create_app("testing")
    app.config["TESTING"] = True

    with app.test_client() as test_client:
        yield test_client


# ---------------------------------------------------------------------------
# Root endpoint tests
# ---------------------------------------------------------------------------


class TestRootEndpoint:
    """Tests for GET /"""

    def test_root_returns_200(self, client):
        """Root endpoint should respond with HTTP 200."""
        response = client.get("/")
        assert response.status_code == 200

    def test_root_returns_json(self, client):
        """Root endpoint should return a JSON content-type header."""
        response = client.get("/")
        assert response.content_type == "application/json"

    def test_root_has_application_field(self, client):
        """Response body must include the 'application' key."""
        response = client.get("/")
        data = json.loads(response.data)
        assert "application" in data

    def test_root_has_status_field(self, client):
        """Response body must include the 'status' key."""
        response = client.get("/")
        data = json.loads(response.data)
        assert "status" in data

    def test_root_status_is_running(self, client):
        """The 'status' field must equal 'running'."""
        response = client.get("/")
        data = json.loads(response.data)
        assert data["status"] == "running"

    def test_root_has_environment_field(self, client):
        """Response body must include the 'environment' key."""
        response = client.get("/")
        data = json.loads(response.data)
        assert "environment" in data

    def test_root_environment_is_testing(self, client):
        """The 'environment' field must reflect the active config (testing)."""
        response = client.get("/")
        data = json.loads(response.data)
        assert data["environment"] == "testing"

    def test_root_has_message_field(self, client):
        """Response body must include the 'message' key."""
        response = client.get("/")
        data = json.loads(response.data)
        assert "message" in data

    def test_root_message_is_not_empty(self, client):
        """The 'message' field must not be empty."""
        response = client.get("/")
        data = json.loads(response.data)
        assert data["message"]


# ---------------------------------------------------------------------------
# Health check endpoint tests
# ---------------------------------------------------------------------------


class TestHealthEndpoint:
    """Tests for GET /health"""

    def test_health_returns_200(self, client):
        """Health endpoint must return HTTP 200."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_returns_json(self, client):
        """Health endpoint should return a JSON content-type header."""
        response = client.get("/health")
        assert response.content_type == "application/json"

    def test_health_has_status_field(self, client):
        """Health response body must include the 'status' key."""
        response = client.get("/health")
        data = json.loads(response.data)
        assert "status" in data

    def test_health_status_is_healthy(self, client):
        """The 'status' field must equal 'healthy'."""
        response = client.get("/health")
        data = json.loads(response.data)
        assert data["status"] == "healthy"

    def test_health_only_status_key(self, client):
        """Health endpoint should return exactly one key to stay lightweight."""
        response = client.get("/health")
        data = json.loads(response.data)
        assert list(data.keys()) == ["status"]


# ---------------------------------------------------------------------------
# 404 handling
# ---------------------------------------------------------------------------


class TestNotFound:
    """Verify Flask's default 404 behaviour for unknown routes."""

    def test_unknown_route_returns_404(self, client):
        """An unregistered path must return HTTP 404."""
        response = client.get("/this-route-does-not-exist")
        assert response.status_code == 404
