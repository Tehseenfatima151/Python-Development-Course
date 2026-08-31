"""
ClipboardManager — copies secrets to the clipboard and optionally clears them.

Uses pyperclip as the cross-platform clipboard backend.
If pyperclip is unavailable or the system clipboard is inaccessible the
manager degrades gracefully and reports the issue without crashing.
"""

import threading
import time

# Delay in seconds before the clipboard is automatically cleared
CLIPBOARD_CLEAR_DELAY = 30


class ClipboardError(Exception):
    """Raised when a clipboard operation fails."""


class ClipboardManager:
    """
    Provides clipboard copy functionality with optional automatic clearing.

    The auto-clear feature runs in a daemon thread so it does not block
    the main application. The thread is cancelled if another copy operation
    is performed before the delay elapses.
    """

    def __init__(self, clear_delay: int = CLIPBOARD_CLEAR_DELAY) -> None:
        """
        Args:
            clear_delay: Seconds after which the clipboard is automatically
                         cleared. Set to 0 to disable auto-clear.
        """
        self._clear_delay = clear_delay
        self._clear_timer: threading.Timer | None = None

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def copy(self, secret: str) -> None:
        """
        Copy *secret* to the system clipboard.

        Also schedules automatic clipboard clearing after *clear_delay*
        seconds (if clear_delay > 0).

        Args:
            secret: The plaintext value to copy.

        Raises:
            ClipboardError: If pyperclip is not installed or the clipboard
                            is not accessible on this system.
        """
        try:
            import pyperclip  # type: ignore
        except ImportError as exc:
            raise ClipboardError(
                "pyperclip is not installed. Run: pip install pyperclip"
            ) from exc

        try:
            pyperclip.copy(secret)
        except pyperclip.PyperclipException as exc:
            raise ClipboardError(
                f"Clipboard not accessible: {exc}\n"
                "On Linux, install xclip or xsel: sudo apt install xclip"
            ) from exc

        # Cancel any existing clear timer
        self._cancel_timer()

        if self._clear_delay > 0:
            self._clear_timer = threading.Timer(
                self._clear_delay, self._clear_clipboard
            )
            self._clear_timer.daemon = True
            self._clear_timer.start()

    def clear_now(self) -> None:
        """
        Immediately clear the clipboard and cancel any pending auto-clear.
        Silently ignores errors so it is safe to call on shutdown.
        """
        self._cancel_timer()
        self._clear_clipboard()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _clear_clipboard(self) -> None:
        """Overwrite the clipboard with an empty string."""
        try:
            import pyperclip  # type: ignore
            pyperclip.copy("")
        except Exception:
            pass  # Fail silently on cleanup

    def _cancel_timer(self) -> None:
        """Cancel a pending auto-clear timer if one exists."""
        if self._clear_timer is not None:
            self._clear_timer.cancel()
            self._clear_timer = None
