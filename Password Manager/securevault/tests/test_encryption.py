"""
Tests for EncryptionManager — key derivation, encrypt, decrypt.
"""

import pytest

from app.encryption_manager import EncryptionManager, EncryptionError

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

MASTER_PASSWORD = "TestPass1!"


@pytest.fixture
def enc() -> EncryptionManager:
    """Return an initialised EncryptionManager."""
    manager = EncryptionManager()
    salt = EncryptionManager.generate_salt()
    manager.initialise(MASTER_PASSWORD, salt)
    return manager


@pytest.fixture
def salt() -> bytes:
    return EncryptionManager.generate_salt()


# ---------------------------------------------------------------------------
# generate_salt
# ---------------------------------------------------------------------------

class TestGenerateSalt:
    def test_returns_bytes(self) -> None:
        s = EncryptionManager.generate_salt()
        assert isinstance(s, bytes)

    def test_correct_length(self) -> None:
        s = EncryptionManager.generate_salt()
        assert len(s) == 32

    def test_unique_each_call(self) -> None:
        salts = {EncryptionManager.generate_salt() for _ in range(20)}
        assert len(salts) == 20


# ---------------------------------------------------------------------------
# derive_key
# ---------------------------------------------------------------------------

class TestDeriveKey:
    def test_returns_bytes_of_length_32(self, salt: bytes) -> None:
        key = EncryptionManager.derive_key(MASTER_PASSWORD, salt)
        assert isinstance(key, bytes)
        assert len(key) == 32

    def test_deterministic_with_same_inputs(self, salt: bytes) -> None:
        k1 = EncryptionManager.derive_key(MASTER_PASSWORD, salt)
        k2 = EncryptionManager.derive_key(MASTER_PASSWORD, salt)
        assert k1 == k2

    def test_different_password_gives_different_key(self, salt: bytes) -> None:
        k1 = EncryptionManager.derive_key(MASTER_PASSWORD, salt)
        k2 = EncryptionManager.derive_key("OtherPass9#", salt)
        assert k1 != k2

    def test_different_salt_gives_different_key(self) -> None:
        s1 = EncryptionManager.generate_salt()
        s2 = EncryptionManager.generate_salt()
        k1 = EncryptionManager.derive_key(MASTER_PASSWORD, s1)
        k2 = EncryptionManager.derive_key(MASTER_PASSWORD, s2)
        assert k1 != k2

    def test_key_is_not_equal_to_password_bytes(self, salt: bytes) -> None:
        key = EncryptionManager.derive_key(MASTER_PASSWORD, salt)
        assert key != MASTER_PASSWORD.encode("utf-8")


# ---------------------------------------------------------------------------
# initialise / clear / is_ready
# ---------------------------------------------------------------------------

class TestInitialise:
    def test_is_ready_after_initialise(self) -> None:
        mgr = EncryptionManager()
        salt = EncryptionManager.generate_salt()
        mgr.initialise(MASTER_PASSWORD, salt)
        assert mgr.is_ready is True

    def test_not_ready_before_initialise(self) -> None:
        mgr = EncryptionManager()
        assert mgr.is_ready is False

    def test_not_ready_after_clear(self, enc: EncryptionManager) -> None:
        enc.clear()
        assert enc.is_ready is False


# ---------------------------------------------------------------------------
# encrypt
# ---------------------------------------------------------------------------

class TestEncrypt:
    def test_encrypt_returns_string(self, enc: EncryptionManager) -> None:
        token = enc.encrypt("my-secret-password")
        assert isinstance(token, str)

    def test_ciphertext_differs_from_plaintext(self, enc: EncryptionManager) -> None:
        plaintext = "my-secret-password"
        ciphertext = enc.encrypt(plaintext)
        assert ciphertext != plaintext

    def test_encrypt_twice_gives_different_tokens(self, enc: EncryptionManager) -> None:
        # Fernet tokens are non-deterministic (include timestamp + nonce)
        ct1 = enc.encrypt("same-password")
        ct2 = enc.encrypt("same-password")
        assert ct1 != ct2

    def test_encrypt_raises_if_not_initialised(self) -> None:
        mgr = EncryptionManager()
        with pytest.raises(EncryptionError):
            mgr.encrypt("secret")

    def test_plaintext_not_present_in_ciphertext(self, enc: EncryptionManager) -> None:
        plaintext = "super-secret-123"
        ciphertext = enc.encrypt(plaintext)
        assert plaintext not in ciphertext


# ---------------------------------------------------------------------------
# decrypt
# ---------------------------------------------------------------------------

class TestDecrypt:
    def test_decrypt_returns_original_plaintext(self, enc: EncryptionManager) -> None:
        plaintext = "correct-horse-battery"
        ciphertext = enc.encrypt(plaintext)
        assert enc.decrypt(ciphertext) == plaintext

    def test_decrypt_raises_on_invalid_token(self, enc: EncryptionManager) -> None:
        with pytest.raises(EncryptionError):
            enc.decrypt("not-a-valid-fernet-token")

    def test_decrypt_raises_with_wrong_key(self) -> None:
        salt1 = EncryptionManager.generate_salt()
        salt2 = EncryptionManager.generate_salt()

        enc1 = EncryptionManager()
        enc1.initialise(MASTER_PASSWORD, salt1)
        ciphertext = enc1.encrypt("secret-value")

        enc2 = EncryptionManager()
        enc2.initialise(MASTER_PASSWORD, salt2)  # Different salt → different key
        with pytest.raises(EncryptionError):
            enc2.decrypt(ciphertext)

    def test_decrypt_raises_if_not_initialised(self) -> None:
        mgr = EncryptionManager()
        with pytest.raises(EncryptionError):
            mgr.decrypt("anything")

    def test_roundtrip_unicode(self, enc: EncryptionManager) -> None:
        plaintext = "pässwörD_日本語_123!"
        assert enc.decrypt(enc.encrypt(plaintext)) == plaintext

    def test_roundtrip_empty_string(self, enc: EncryptionManager) -> None:
        plaintext = ""
        assert enc.decrypt(enc.encrypt(plaintext)) == plaintext
