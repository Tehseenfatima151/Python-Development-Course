"""Campaign scheduler module using the `schedule` library.

Enables deferred campaign execution at a specific calendar date and time
or daily recurring time window with active countdown heartbeats.
"""

from __future__ import annotations

import logging
import time
from datetime import datetime
from typing import Callable, Optional
import schedule

logger = logging.getLogger("campaign_manager")


class CampaignScheduler:
    """Manages scheduled campaign execution using schedule library."""

    def __init__(
        self,
        target_time_str: str = "10:00",
        target_date_str: Optional[str] = None,
    ) -> None:
        self.target_time_str = target_time_str.strip()
        self.target_date_str = target_date_str.strip() if target_date_str else None
        self._target_datetime: Optional[datetime] = None
        self._parse_schedule()

    def _parse_schedule(self) -> None:
        """Parse date and time strings into datetime target."""
        time_parts = self.target_time_str.split(":")
        if len(time_parts) != 2:
            raise ValueError(f"Invalid SCHEDULED_TIME format: '{self.target_time_str}'. Expected 'HH:MM'.")

        hour, minute = int(time_parts[0]), int(time_parts[1])
        if not (0 <= hour <= 23 and 0 <= minute <= 59):
            raise ValueError(f"Time out of range: '{self.target_time_str}'.")

        now = datetime.now()
        if self.target_date_str:
            target_date = datetime.strptime(self.target_date_str, "%Y-%m-%d").date()
            self._target_datetime = datetime(
                year=target_date.year,
                month=target_date.month,
                day=target_date.day,
                hour=hour,
                minute=minute,
                second=0,
            )
        else:
            # If no date specified, schedule for today at target time; if passed, schedule tomorrow
            candidate = datetime(
                year=now.year,
                month=now.month,
                day=now.day,
                hour=hour,
                minute=minute,
                second=0,
            )
            if candidate <= now:
                # Target for tomorrow
                candidate = candidate.replace(day=now.day + 1)
            self._target_datetime = candidate

    @property
    def target_datetime(self) -> datetime:
        return self._target_datetime

    def run_scheduled_job(self, campaign_task: Callable[[], None]) -> None:
        """Wait until scheduled time arrives, then execute campaign_task once."""
        now = datetime.now()
        target = self._target_datetime

        if target is None:
            raise ValueError("Target datetime is not set.")

        time_remaining = (target - now).total_seconds()

        print("========================================")
        print("CAMPAIGN SCHEDULER ACTIVE")
        print(f"Current Local Time : {now.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Scheduled Launch   : {target.strftime('%Y-%m-%d %H:%M:%S')}")

        if time_remaining <= 0:
            print("[INFO] Scheduled time is in the past or right now. Initiating campaign immediately...")
            campaign_task()
            return

        hours = int(time_remaining // 3600)
        minutes = int((time_remaining % 3600) // 60)
        seconds = int(time_remaining % 60)
        print(f"Time Until Launch  : {hours}h {minutes}m {seconds}s")
        print("Waiting for scheduled launch time... (Press Ctrl+C to cancel)")
        print("========================================")

        job_executed = False

        def trigger() -> schedule.CancelJob:
            nonlocal job_executed
            current_dt = datetime.now()
            # If target date was specified, verify date matches
            if self.target_date_str and current_dt.date() < target.date():
                return None  # Wait for proper date
            logger.info("Triggering scheduled campaign execution at %s", current_dt)
            campaign_task()
            job_executed = True
            return schedule.CancelJob

        # Register schedule job every minute check
        schedule.every(10).seconds.do(lambda: (
            trigger() if datetime.now() >= target else None
        ))

        last_heartbeat = time.time()

        try:
            while not job_executed:
                schedule.run_pending()
                time.sleep(1)
                # Print periodic countdown heartbeat every 30 seconds
                if time.time() - last_heartbeat >= 30:
                    last_heartbeat = time.time()
                    diff = (target - datetime.now()).total_seconds()
                    if diff > 0:
                        h = int(diff // 3600)
                        m = int((diff % 3600) // 60)
                        s = int(diff % 60)
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] Countdown: {h:02d}h {m:02d}m {s:02d}s remaining until campaign dispatch...")
        except KeyboardInterrupt:
            print("\n[INFO] Campaign scheduler cancelled by user.")
            logger.info("Campaign scheduler cancelled by user interrupt.")
