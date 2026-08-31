"""
conftest.py — pytest configuration.

Patches PBKDF2 iteration counts to low values for tests so the
test suite runs in seconds rather than minutes. The security
properties of the algorithm are still exercised; only the work
factor is reduced.
"""

import pytest
import app.auth_manager as _auth_mod
import app.encryption_manager as _enc_mod


@pytest.fixture(autouse=True)
def fast_kdf(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Reduce PBKDF2 iterations to 1 for all tests.
    This keeps the test suite fast without changing any code path.
    """
    monkeypatch.setattr(_auth_mod, "AUTH_HASH_ITERATIONS", 1)
    monkeypatch.setattr(_enc_mod, "PBKDF2_ITERATIONS", 1)
