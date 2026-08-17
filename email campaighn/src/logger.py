"""Logging system for delivery auditing and application diagnostics.

Maintains two distinct logs:
1. logs/email_log.csv: Structured CSV audit trail for every recipient attempt.
2. logs/application.log: Detailed technical and debugging log with rotating file handler.

Enforces strict redaction of sensitive credentials.
"""

from __future__ import annotations

import csv
import logging
import re
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any, Optional
import pandas as pd


# Redaction patterns for sensitive data in text logs
PASSWORD_PATTERN = re.compile(r"(password|pass|pwd|app_password)\s*[:=]\s*['\"]?([^\s'\"]+)['\"]?", re.IGNORECASE)


class SensitiveDataFilter(logging.Filter):
    """Logging filter to redact credentials from application log output."""

    def filter(self, record: logging.LogRecord) -> bool:
        if isinstance(record.msg, str):
            record.msg = PASSWORD_PATTERN.sub(r"\1=********", record.msg)
        if record.args and isinstance(record.args, dict):
            redacted_args = {}
            for k, v in record.args.items():
                if any(sec in k.lower() for sec in ("password", "pass", "secret", "token")):
                    redacted_args[k] = "********"
                else:
                    redacted_args[k] = v
            record.args = redacted_args
        return True


def setup_application_logger(
    log_file_path: Path | str,
    log_level: int = logging.INFO,
    console_output: bool = False,
) -> logging.Logger:
    """Configure and return the root application logger."""
    path = Path(log_file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("campaign_manager")
    logger.setLevel(log_level)
    logger.propagate = False

    # Avoid duplicate handlers if already configured
    if logger.hasHandlers():
        logger.handlers.clear()

    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] [%(name)s:%(lineno)d] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    sensitive_filter = SensitiveDataFilter()

    # Rotating File Handler (5 MB max, 3 backups)
    file_handler = RotatingFileHandler(
        filename=path,
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    file_handler.addFilter(sensitive_filter)
    logger.addHandler(file_handler)

    if console_output:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.addFilter(sensitive_filter)
        logger.addHandler(console_handler)

    return logger


class EmailAuditLogger:
    """Manages the structured delivery audit CSV log."""

    CSV_HEADER = ["timestamp", "campaign_id", "name", "email", "subject", "status", "error"]

    def __init__(self, csv_log_path: Path | str) -> None:
        self.log_path = Path(csv_log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_header()

    def _ensure_header(self) -> None:
        """Create the CSV file with headers if it does not exist."""
        if not self.log_path.exists() or self.log_path.stat().st_size == 0:
            with open(self.log_path, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(self.CSV_HEADER)

    def log_event(
        self,
        campaign_id: str,
        name: str,
        email: str,
        subject: str,
        status: str,
        error: Optional[str] = None,
        timestamp: Optional[str] = None,
    ) -> None:
        """Record an email delivery attempt to email_log.csv."""
        if timestamp is None:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Sanitize error message to prevent commas breaking CSV representation
        clean_error = (error or "").replace("\r", " ").replace("\n", " ").strip()

        with open(self.log_path, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                timestamp,
                campaign_id,
                name,
                email,
                subject,
                status,
                clean_error,
            ])

    def get_previously_sent_emails(self, campaign_id: str) -> set[str]:
        """Return a set of lowercased emails that have already been 'Sent' for this campaign."""
        if not self.log_path.exists() or self.log_path.stat().st_size == 0:
            return set()

        sent_emails: set[str] = set()
        try:
            df = pd.read_csv(self.log_path, dtype=str)
            if df.empty or "campaign_id" not in df.columns or "status" not in df.columns:
                return set()

            # Filter rows for this campaign where status == 'Sent'
            mask = (df["campaign_id"] == campaign_id) & (df["status"].str.strip().str.lower() == "sent")
            sent_df = df[mask]
            if "email" in sent_df.columns:
                sent_emails = set(sent_df["email"].dropna().str.strip().str.lower())
        except Exception:
            # Fallback to direct CSV reader if pandas encounters an edge-case format
            with open(self.log_path, mode="r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if (
                        row.get("campaign_id") == campaign_id
                        and (row.get("status") or "").strip().lower() == "sent"
                    ):
                        email = (row.get("email") or "").strip().lower()
                        if email:
                            sent_emails.add(email)

        return sent_emails

    def get_campaign_statistics(self) -> dict[str, Any]:
        """Parse email_log.csv and return aggregated statistics per campaign."""
        if not self.log_path.exists() or self.log_path.stat().st_size == 0:
            return {}

        try:
            df = pd.read_csv(self.log_path, dtype=str)
            if df.empty:
                return {}

            stats: dict[str, Any] = {}
            for campaign_id, group in df.groupby("campaign_id"):
                status_counts = group["status"].value_counts().to_dict()
                stats[str(campaign_id)] = {
                    "total_attempts": len(group),
                    "sent": int(status_counts.get("Sent", 0)),
                    "failed": int(status_counts.get("Failed", 0)),
                    "skipped": int(status_counts.get("Skipped", 0)),
                    "first_activity": str(group["timestamp"].min()),
                    "last_activity": str(group["timestamp"].max()),
                }
            return stats
        except Exception:
            return {}
