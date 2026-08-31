"""
EncryptionManager — key derivation and Fernet encryption/decryption.

Architecture:
  Master Password + Salt  →  PBKDF2HMAC  →  32-byte key  →  base64url  →  Fernet
"""

import base64
import os

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

# KDF parameters
PBKDF2_ITERATIONS = 600_000   # NIST SP 800-132 recommended minimum (2023)
SALT_SIZE = 32                 # bytes


class EncryptionError(Exception):
    """Raised when an encryption or decryption operation fails."""


class EncryptionManager:
    """
    Handles all cryptographic operations for SecureVault.

    Responsibilities:
      - Deriving a Fernet-compatible key from the master password via PBKDF2HMAC.
      - Encrypting plaintext passwords before they are written to disk.
      - Decrypting ciphertext passwords after successful authentication.
      - Generating new random salts for key derivation.

    The derived key and the Fernet instance are held only in memory and
    are discarded when the session ends.
    """

    def __init__(self) -> None:
        self._fernet: Fernet | None = None

    # ------------------------------------------------------------------
    # Salt management
    # ------------------------------------------------------------------

    @staticmethod
    def generate_salt() -> bytes:
        """Generate and return a cryptographically secure random salt."""
        return os.urandom(SALT_SIZE)

    # ------------------------------------------------------------------
    # Key derivation
    # ------------------------------------------------------------------

    @staticmethod
    def derive_key(master_password: str, salt: bytes) -> bytes:
        """
        Derive a 32-byte key from the master password and salt using
        PBKDF2-HMAC-SHA256.

        Args:
            master_password: The plaintext master password (not stored).
            salt: A random salt (stored alongside the encrypted data).

        Returns:
            A 32-byte derived key suitable for use with Fernet after
            base64url encoding.
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=PBKDF2_ITERATIONS,
        )
        return kdf.derive(master_password.encode("utf-8"))

    # ------------------------------------------------------------------
    # Session initialisation
    # ------------------------------------------------------------------

    def initialise(self, master_password: str, salt: bytes) -> None:
        """
        Derive the Fernet key from the master password and salt, then
        initialise the internal Fernet instance.

        Must be called after successful authentication before any
        encrypt/decrypt operations.

        Args:
            master_password: The plaintext master password.
            salt: The salt associated with this vault.
        """
        raw_key = self.derive_key(master_password, salt)
        fernet_key = base64.urlsafe_b64encode(raw_key)
        self._fernet = Fernet(fernet_key)

    def clear(self) -> None:
        """
        Destroy the in-memory Fernet instance and key material.
        Called on logout or session expiry.
        """
        self._fernet = None

    @property
    def is_ready(self) -> bool:
        """Return True if the Fernet instance has been initialised."""
        return self._fernet is not None

    # ------------------------------------------------------------------
    # Encrypt / Decrypt
    # ------------------------------------------------------------------

    def encrypt(self, plaintext: str) -> str:
        """
        Encrypt a plaintext string and return the ciphertext as a
        UTF-8 string suitable for JSON storage.

        Args:
            plaintext: The password (or other secret) to encrypt.

        Returns:
            A base64url-encoded Fernet token as a string.

        Raises:
            EncryptionError: If the Fernet instance is not initialised.
        """
        self._require_fernet()
        try:
            token = self._fernet.encrypt(plaintext.encode("utf-8"))  # type: ignore[union-attr]
            return token.decode("utf-8")
        except Exception as exc:
            raise EncryptionError("Encryption failed.") from exc

    def decrypt(self, ciphertext: str) -> str:
        """
        Decrypt a Fernet token and return the original plaintext.

        Args:
            ciphertext: A base64url-encoded Fernet token (as stored in JSON).

        Returns:
            The decrypted plaintext string.

        Raises:
            EncryptionError: If decryption fails (wrong key, corrupted data, etc.).
        """
        self._require_fernet()
        try:
            plaintext = self._fernet.decrypt(ciphertext.encode("utf-8"))  # type: ignore[union-attr]
            return plaintext.decode("utf-8")
        except InvalidToken as exc:
            raise EncryptionError(
                "Decryption failed. The data may be corrupted or the key is incorrect."
            ) from exc
        except Exception as exc:
            raise EncryptionError("Decryption failed.") from exc

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _require_fernet(self) -> None:
        """Raise EncryptionError if the Fernet instance is not ready."""
        if self._fernet is None:
            raise EncryptionError(
                "Encryption manager is not initialised. Please authenticate first."
            )
