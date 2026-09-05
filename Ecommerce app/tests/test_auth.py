"""Tests for authentication endpoints."""
import pytest


class TestRegister:
    def test_register_success(self, client):
        res = client.post("/api/auth/register", json={
            "name": "Alice",
            "email": "alice@example.com",
            "password": "securepass123",
        })
        data = res.get_json()
        assert res.status_code == 201
        assert data["success"] is True
        assert "access_token" in data["data"]
        assert data["data"]["user"]["email"] == "alice@example.com"
        assert data["data"]["user"]["role"] == "customer"
        # Password hash must never be returned
        assert "password_hash" not in data["data"]["user"]

    def test_register_duplicate_email(self, client, customer_user):
        res = client.post("/api/auth/register", json={
            "name": "Duplicate",
            "email": "customer@test.com",
            "password": "password123",
        })
        data = res.get_json()
        assert res.status_code == 409
        assert data["success"] is False
        assert data["error"] == "EMAIL_TAKEN"

    def test_register_invalid_email(self, client):
        res = client.post("/api/auth/register", json={
            "name": "Bob",
            "email": "not-an-email",
            "password": "password123",
        })
        assert res.status_code == 422
        data = res.get_json()
        assert "email" in data["errors"]

    def test_register_short_password(self, client):
        res = client.post("/api/auth/register", json={
            "name": "Bob",
            "email": "bob@example.com",
            "password": "short",
        })
        assert res.status_code == 422
        assert "password" in res.get_json()["errors"]

    def test_register_missing_name(self, client):
        res = client.post("/api/auth/register", json={
            "name": "",
            "email": "noname@example.com",
            "password": "password123",
        })
        assert res.status_code == 422
        assert "name" in res.get_json()["errors"]


class TestLogin:
    def test_login_success(self, client, customer_user):
        res = client.post("/api/auth/login", json={
            "email": "customer@test.com",
            "password": "password123",
        })
        data = res.get_json()
        assert res.status_code == 200
        assert data["success"] is True
        assert "access_token" in data["data"]

    def test_login_wrong_password(self, client, customer_user):
        res = client.post("/api/auth/login", json={
            "email": "customer@test.com",
            "password": "wrongpassword",
        })
        assert res.status_code == 401
        assert res.get_json()["error"] == "INVALID_CREDENTIALS"

    def test_login_nonexistent_email(self, client):
        res = client.post("/api/auth/login", json={
            "email": "nobody@example.com",
            "password": "password123",
        })
        assert res.status_code == 401
        # Generic message to prevent user enumeration
        assert res.get_json()["error"] == "INVALID_CREDENTIALS"

    def test_login_missing_fields(self, client):
        res = client.post("/api/auth/login", json={"email": "test@test.com"})
        assert res.status_code == 400


class TestProtectedEndpoints:
    def test_me_with_valid_token(self, client, customer_user, customer_headers):
        res = client.get("/api/auth/me", headers=customer_headers)
        data = res.get_json()
        assert res.status_code == 200
        assert data["data"]["user"]["email"] == "customer@test.com"
        assert "password_hash" not in data["data"]["user"]

    def test_me_without_token(self, client):
        res = client.get("/api/auth/me")
        assert res.status_code == 401

    def test_me_with_invalid_token(self, client):
        res = client.get("/api/auth/me", headers={"Authorization": "Bearer completely.invalid.token"})
        assert res.status_code == 401

    def test_logout(self, client, customer_headers):
        res = client.post("/api/auth/logout", headers=customer_headers)
        assert res.status_code == 200
        assert res.get_json()["success"] is True
