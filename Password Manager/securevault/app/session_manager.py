"""
SessionManager — tracks user activity and enforces inactivity timeout.
"""

import time

# Configurable session timeout in seconds (5 minutes)
SESSION_TIMEOUT = 300


class SessionManager:
    """
    Tracks the timestamp of the last user activity and determines
    whether the session has expired due to inactivity.
    """

    def __init__(self, timeout: int = SESSION_TIMEOUT) -> None:
        """
        Initialise the session manager.

        Args:
            timeout: Number of seconds of inactivity before the session expires.
        """
        self._timeout: int = timeout
        self._last_activity: float = time.time()
        self._active: bool = True

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def reset(self) -> None:
        """Record the current time as the most recent activity timestamp."""
        self._last_activity = time.time()

    def is_expired(self) -> bool:
        """
        Return True if the session has been inactive longer than the
        configured timeout, or if the session has been explicitly ended.
        """
        if not self._active:
            return True
        return (time.time() - self._last_activity) >= self._timeout

    def end(self) -> None:
        """
        Explicitly end the session (e.g. on logout).
        Clears the last-activity timestamp to prevent timing side-channels.
        """
        self._active = False
        self._last_activity = 0.0

    def start(self) -> None:
        """
        (Re-)start the session and reset the activity timer.
        Called after successful authentication.
        """
        self._active = True
        self.reset()

    @property
    def seconds_remaining(self) -> float:
        """Return how many seconds remain before the session expires."""
        elapsed = time.time() - self._last_activity
        remaining = self._timeout - elapsed
        return max(remaining, 0.0)
