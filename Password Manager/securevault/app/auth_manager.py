"""
AuthManager — master password setup, hashing, and login verification.

The master password is NEVER stored in plaintext. Authentication is
performed by comparing PBKDF2-HMAC-SHA256 digests.

Storage format (auth.json):
{
    "password_hash": "<hex string>",
    "auth_salt":     "<hex string>",
    "enc_salt":      "<hex string>"
}

Two salts are maintained:
  - auth_salt : used solely for password verification hashing.
  - enc_salt  : used for Fernet key derivation (passed to EncryptionManager).
"""

import hashlib
import json
import os
from pathlib import Path

from app.password_generator import PasswordGenerator

# Authentication hashing parameters
AUTH_HASH_ITERATIONS = 600_000
AUTH_HASH_ALGORITHM = "sha256"
AUTH_SALT_SIZE = 32   # bytes
ENC_SALT_SIZE = 32    # bytes

MAX_LOGIN_ATTEMPTS = 3


class AuthError(Exception):
    """Raised for authentication-related failures."""


class AuthManager:
    """
    Manages master password lifecycle:
      - First-time setup: hash + salts generation + persistence.
      - Login: secure comparison of derived hashes.
      - Salt retrieval for the EncryptionManager.
    """

    def __init__(self, auth_file: Path) -> None:
        """
        Args:
            auth_file: Path to the JSON file that stores auth metadata.
        """
        self._auth_file = auth_file

    # ------------------------------------------------------------------
    # Setup & persistence
    # ------------------------------------------------------------------

    def is_initialised(self) -> bool:
        """Return True if the auth file exists and contains valid data."""
        if not self._auth_file.exists():
            return False
        try:
            data = self._load()
            return bool(data.get("password_hash") and data.get("auth_salt") and data.get("enc_salt"))
        except Exception:
            return False

    def setup(self, master_password: str) -> None:
        """
        Hash the master password and persist the auth metadata.

        Args:
            master_password: The validated plaintext master password.

        Raises:
            AuthError: If the password fails strength validation.
        """
        valid, errors = PasswordGenerator.validate_strength(master_password)
        if not valid:
            raise AuthError("Master password does not meet strength requirements:\n" + "\n".join(errors))

        auth_salt = os.urandom(AUTH_SALT_SIZE)
        enc_salt = os.urandom(ENC_SALT_SIZE)
        password_hash = self._hash_password(master_password, auth_salt)

        data = {
            "password_hash": password_hash.hex(),
            "auth_salt": auth_salt.hex(),
            "enc_salt": enc_salt.hex(),
        }
        self._save(data)

    # ------------------------------------------------------------------
    # Login
    # ------------------------------------------------------------------

    def verify(self, master_password: str) -> bool:
        """
        Verify the supplied master password against the stored hash.

        Args:
            master_password: The plaintext master password to check.

        Returns:
            True if the password matches, False otherwise.

        Raises:
            AuthError: If auth data cannot be loaded.
        """
        data = self._load()
        stored_hash = bytes.fromhex(data["password_hash"])
        auth_salt = bytes.fromhex(data["auth_salt"])
        candidate_hash = self._hash_password(master_password, auth_salt)
        # Constant-time comparison to prevent timing attacks
        return hmac_compare(candidate_hash, stored_hash)

    def get_enc_salt(self) -> bytes:
        """
        Return the encryption salt used to derive the Fernet key.

        Raises:
            AuthError: If auth data cannot be loaded.
        """
        data = self._load()
        return bytes.fromhex(data["enc_salt"])

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _hash_password(password: str, salt: bytes) -> bytes:
        """Derive a hash from the password using PBKDF2-HMAC-SHA256."""
        dk = hashlib.pbkdf2_hmac(
            AUTH_HASH_ALGORITHM,
            password.encode("utf-8"),
            salt,
            AUTH_HASH_ITERATIONS,
        )
        return dk

    def _load(self) -> dict:
        """Load and return the raw auth JSON data."""
        try:
            with open(self._auth_file, "r", encoding="utf-8") as fh:
                return json.load(fh)
        except FileNotFoundError as exc:
            raise AuthError("Authentication data not found. Please run first-time setup.") from exc
        except json.JSONDecodeError as exc:
            raise AuthError("Authentication data is corrupted.") from exc
        except OSError as exc:
            raise AuthError(f"Could not read authentication data: {exc}") from exc

    def _save(self, data: dict) -> None:
        """Persist auth data to disk using atomic write."""
        self._auth_file.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = self._auth_file.with_suffix(".tmp")
        try:
            with open(tmp_path, "w", encoding="utf-8") as fh:
                json.dump(data, fh, indent=2)
            tmp_path.replace(self._auth_file)
        except OSError as exc:
            raise AuthError(f"Could not save authentication data: {exc}") from exc
        finally:
            if tmp_path.exists():
                try:
                    tmp_path.unlink()
                except OSError:
                    pass


def hmac_compare(a: bytes, b: bytes) -> bool:
    """
    Constant-time bytes comparison to prevent timing side-channel attacks.
    Uses the same principle as hmac.compare_digest.
    """
    import hmac as _hmac
    return _hmac.compare_digest(a, b)
