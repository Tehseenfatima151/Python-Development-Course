"""
Tests for AuthManager — master password setup, hashing, and login verification.
"""

import json
import pytest
from pathlib import Path

from app.auth_manager import AuthManager, AuthError


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

VALID_PASSWORD = "TestPass1!"   # Meets all strength requirements


@pytest.fixture
def auth_file(tmp_path: Path) -> Path:
    """Return a temporary path for the auth file."""
    return tmp_path / "auth.json"


@pytest.fixture
def initialised_auth(auth_file: Path) -> AuthManager:
    """Return an AuthManager that has already been set up with VALID_PASSWORD."""
    mgr = AuthManager(auth_file)
    mgr.setup(VALID_PASSWORD)
    return mgr


# ---------------------------------------------------------------------------
# is_initialised
# ---------------------------------------------------------------------------

class TestIsInitialised:
    def test_false_when_no_file(self, auth_file: Path) -> None:
        mgr = AuthManager(auth_file)
        assert mgr.is_initialised() is False

    def test_true_after_setup(self, initialised_auth: AuthManager) -> None:
        assert initialised_auth.is_initialised() is True

    def test_false_on_empty_file(self, auth_file: Path) -> None:
        auth_file.write_text("")
        mgr = AuthManager(auth_file)
        assert mgr.is_initialised() is False

    def test_false_on_invalid_json(self, auth_file: Path) -> None:
        auth_file.write_text("not-json{{")
        mgr = AuthManager(auth_file)
        assert mgr.is_initialised() is False


# ---------------------------------------------------------------------------
# setup — password validation
# ---------------------------------------------------------------------------

class TestSetup:
    def test_setup_creates_auth_file(self, auth_file: Path) -> None:
        mgr = AuthManager(auth_file)
        mgr.setup(VALID_PASSWORD)
        assert auth_file.exists()

    def test_auth_file_contains_required_keys(self, auth_file: Path) -> None:
        mgr = AuthManager(auth_file)
        mgr.setup(VALID_PASSWORD)
        data = json.loads(auth_file.read_text())
        assert "password_hash" in data
        assert "auth_salt" in data
        assert "enc_salt" in data

    def test_password_not_stored_in_plaintext(self, auth_file: Path) -> None:
        mgr = AuthManager(auth_file)
        mgr.setup(VALID_PASSWORD)
        raw = auth_file.read_text()
        assert VALID_PASSWORD not in raw

    def test_rejects_weak_password_too_short(self, auth_file: Path) -> None:
        mgr = AuthManager(auth_file)
        with pytest.raises(AuthError):
            mgr.setup("Ab1!")   # Only 4 chars

    def test_rejects_no_uppercase(self, auth_file: Path) -> None:
        mgr = AuthManager(auth_file)
        with pytest.raises(AuthError):
            mgr.setup("testpass1!")

    def test_rejects_no_lowercase(self, auth_file: Path) -> None:
        mgr = AuthManager(auth_file)
        with pytest.raises(AuthError):
            mgr.setup("TESTPASS1!")

    def test_rejects_no_digit(self, auth_file: Path) -> None:
        mgr = AuthManager(auth_file)
        with pytest.raises(AuthError):
            mgr.setup("TestPass!!")

    def test_rejects_no_special(self, auth_file: Path) -> None:
        mgr = AuthManager(auth_file)
        with pytest.raises(AuthError):
            mgr.setup("TestPass11")

    def test_two_setups_produce_different_salts(self, tmp_path: Path) -> None:
        file_a = tmp_path / "auth_a.json"
        file_b = tmp_path / "auth_b.json"
        AuthManager(file_a).setup(VALID_PASSWORD)
        AuthManager(file_b).setup(VALID_PASSWORD)
        data_a = json.loads(file_a.read_text())
        data_b = json.loads(file_b.read_text())
        assert data_a["auth_salt"] != data_b["auth_salt"]


# ---------------------------------------------------------------------------
# verify — login
# ---------------------------------------------------------------------------

class TestVerify:
    def test_correct_password_returns_true(self, initialised_auth: AuthManager) -> None:
        assert initialised_auth.verify(VALID_PASSWORD) is True

    def test_wrong_password_returns_false(self, initialised_auth: AuthManager) -> None:
        assert initialised_auth.verify("WrongPass9@") is False

    def test_empty_password_returns_false(self, initialised_auth: AuthManager) -> None:
        assert initialised_auth.verify("") is False

    def test_partial_password_returns_false(self, initialised_auth: AuthManager) -> None:
        assert initialised_auth.verify(VALID_PASSWORD[:-1]) is False

    def test_verify_raises_if_not_initialised(self, auth_file: Path) -> None:
        mgr = AuthManager(auth_file)
        with pytest.raises(AuthError):
            mgr.verify(VALID_PASSWORD)


# ---------------------------------------------------------------------------
# get_enc_salt
# ---------------------------------------------------------------------------

class TestGetEncSalt:
    def test_returns_bytes(self, initialised_auth: AuthManager) -> None:
        salt = initialised_auth.get_enc_salt()
        assert isinstance(salt, bytes)
        assert len(salt) == 32

    def test_raises_if_not_initialised(self, auth_file: Path) -> None:
        mgr = AuthManager(auth_file)
        with pytest.raises(AuthError):
            mgr.get_enc_salt()
