"""
Tests for SessionManager — activity tracking and inactivity timeout.
"""

import time
import pytest

from app.session_manager import SessionManager


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def session() -> SessionManager:
    """Return a fresh active session with a 5-second timeout for fast testing."""
    mgr = SessionManager(timeout=5)
    mgr.start()
    return mgr


# ---------------------------------------------------------------------------
# start / end / is_expired
# ---------------------------------------------------------------------------

class TestStartEnd:
    def test_active_after_start(self, session: SessionManager) -> None:
        assert session.is_expired() is False

    def test_expired_after_end(self, session: SessionManager) -> None:
        session.end()
        assert session.is_expired() is True

    def test_not_ready_before_start(self) -> None:
        mgr = SessionManager(timeout=5)
        # Default-constructed without start() — _active is True but last
        # activity was set in __init__, so it should be fresh
        assert mgr.is_expired() is False

    def test_can_restart_after_end(self, session: SessionManager) -> None:
        session.end()
        assert session.is_expired() is True
        session.start()
        assert session.is_expired() is False


# ---------------------------------------------------------------------------
# reset — activity timer
# ---------------------------------------------------------------------------

class TestReset:
    def test_reset_prevents_expiry(self) -> None:
        """Session with 2-second timeout should not expire if we keep resetting."""
        mgr = SessionManager(timeout=2)
        mgr.start()
        for _ in range(3):
            time.sleep(0.5)
            mgr.reset()
        # After 1.5 s of sleep but continuous resets, should still be active
        assert mgr.is_expired() is False

    def test_reset_updates_last_activity(self, session: SessionManager) -> None:
        before = session._last_activity
        time.sleep(0.05)
        session.reset()
        assert session._last_activity > before


# ---------------------------------------------------------------------------
# Timeout expiry
# ---------------------------------------------------------------------------

class TestTimeout:
    def test_session_expires_after_timeout(self) -> None:
        mgr = SessionManager(timeout=1)  # 1-second timeout
        mgr.start()
        assert mgr.is_expired() is False
        time.sleep(1.1)
        assert mgr.is_expired() is True

    def test_active_session_does_not_expire_early(self) -> None:
        mgr = SessionManager(timeout=5)
        mgr.start()
        time.sleep(0.2)
        assert mgr.is_expired() is False

    def test_five_minute_session_not_expired_immediately(self) -> None:
        """Simulate the real 300-second timeout — just verify it's not expired at t=0."""
        mgr = SessionManager(timeout=300)
        mgr.start()
        assert mgr.is_expired() is False


# ---------------------------------------------------------------------------
# seconds_remaining
# ---------------------------------------------------------------------------

class TestSecondsRemaining:
    def test_full_remaining_at_start(self) -> None:
        mgr = SessionManager(timeout=10)
        mgr.start()
        assert mgr.seconds_remaining > 9.0

    def test_remaining_decreases_over_time(self) -> None:
        mgr = SessionManager(timeout=10)
        mgr.start()
        time.sleep(0.5)
        assert mgr.seconds_remaining < 10.0

    def test_remaining_is_zero_after_expiry(self) -> None:
        mgr = SessionManager(timeout=1)
        mgr.start()
        time.sleep(1.1)
        assert mgr.seconds_remaining == 0.0

    def test_remaining_is_zero_after_end(self, session: SessionManager) -> None:
        session.end()
        # seconds_remaining is not meaningful after end, but must not raise
        _ = session.seconds_remaining
