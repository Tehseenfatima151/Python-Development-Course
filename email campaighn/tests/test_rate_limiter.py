"""Unit tests for sliding-window RateLimiter."""

import time
import unittest
from unittest.mock import MagicMock

from src.email_sender import RateLimiter


class TestRateLimiter(unittest.TestCase):
    """Test suite for rate limiting math and window enforcement."""

    def test_pacing_delay_invoked(self) -> None:
        mock_sleep = MagicMock()
        limiter = RateLimiter(max_per_hour=50, pacing_delay_seconds=1.5)

        waited = limiter.wait_if_needed(sleep_fn=mock_sleep)
        mock_sleep.assert_called_once_with(1.5)
        self.assertEqual(waited, 1.5)

    def test_hourly_limit_pause_triggered(self) -> None:
        mock_sleep = MagicMock()
        limiter = RateLimiter(max_per_hour=3, pacing_delay_seconds=0.0)

        # Pretend we sent 3 emails right now
        current_time = time.time()
        limiter.send_timestamps = [
            current_time - 100,
            current_time - 50,
            current_time - 10,
        ]

        # 4th email should trigger wait
        waited = limiter.wait_if_needed(sleep_fn=mock_sleep)
        self.assertGreater(waited, 3400.0)  # ~3500 seconds until oldest send is 1h old
        self.assertTrue(mock_sleep.called)

    def test_expired_timestamps_purged(self) -> None:
        mock_sleep = MagicMock()
        limiter = RateLimiter(max_per_hour=2, pacing_delay_seconds=0.0)

        # Timestamps older than 3600s
        old_time = time.time() - 4000
        limiter.send_timestamps = [old_time, old_time + 10]

        waited = limiter.wait_if_needed(sleep_fn=mock_sleep)
        # Should not wait because old timestamps are discarded
        self.assertEqual(waited, 0.0)
        self.assertEqual(len(limiter.send_timestamps), 0)


if __name__ == "__main__":
    unittest.main()
