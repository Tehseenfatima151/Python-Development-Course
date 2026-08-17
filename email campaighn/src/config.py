"""Configuration module for Automated Bulk Email Campaign Manager.

Loads configuration parameters from environment variables and .env file.
Provides type safety, path resolution relative to project root, and secure
masking of sensitive credentials.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Base paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = PROJECT_ROOT / ".env"

# Load environment variables from .env if present
load_dotenv(dotenv_path=ENV_PATH)


@dataclass(frozen=True)
class AppConfig:
    """Immutable application configuration container."""

    # Project directories
    project_root: Path = field(default=PROJECT_ROOT)
    data_dir: Path = field(default=PROJECT_ROOT / "data")
    templates_dir: Path = field(default=PROJECT_ROOT / "templates")
    logs_dir: Path = field(default=PROJECT_ROOT / "logs")

    # File paths
    contacts_csv_path: Path = field(
        default_factory=lambda: PROJECT_ROOT / os.getenv("CONTACTS_CSV_PATH", "data/contacts.csv")
    )
    email_template_path: Path = field(
        default_factory=lambda: PROJECT_ROOT / os.getenv("EMAIL_TEMPLATE_PATH", "templates/email_template.html")
    )
    email_log_csv_path: Path = field(
        default_factory=lambda: PROJECT_ROOT / os.getenv("EMAIL_LOG_CSV_PATH", "logs/email_log.csv")
    )
    application_log_path: Path = field(
        default_factory=lambda: PROJECT_ROOT / os.getenv("APPLICATION_LOG_PATH", "logs/application.log")
    )

    # SMTP Server Settings
    smtp_host: str = field(default_factory=lambda: os.getenv("SMTP_HOST", "smtp.gmail.com"))
    smtp_port: int = field(default_factory=lambda: int(os.getenv("SMTP_PORT", "587")))
    smtp_email: str = field(default_factory=lambda: os.getenv("SMTP_EMAIL", "").strip())
    smtp_app_password: str = field(default_factory=lambda: os.getenv("SMTP_APP_PASSWORD", "").strip())
    sender_name: str = field(default_factory=lambda: os.getenv("SENDER_NAME", "Apex Marketing Solutions").strip())

    # Campaign Metadata
    campaign_id: str = field(default_factory=lambda: os.getenv("CAMPAIGN_ID", "campaign_2026_08_20").strip())
    campaign_subject: str = field(
        default_factory=lambda: os.getenv("CAMPAIGN_SUBJECT", "Exclusive Offer for {{name}}").strip()
    )

    # Rate Limiting & Retry Configuration
    max_emails_per_hour: int = field(default_factory=lambda: int(os.getenv("MAX_EMAILS_PER_HOUR", "50")))
    max_retries: int = field(default_factory=lambda: int(os.getenv("MAX_RETRIES", "2")))
    retry_delay_seconds: float = field(
        default_factory=lambda: float(os.getenv("RETRY_DELAY_SECONDS", "3.0"))
    )

    # Scheduler Settings
    scheduled_date: str = field(default_factory=lambda: os.getenv("SCHEDULED_DATE", "").strip())
    scheduled_time: str = field(default_factory=lambda: os.getenv("SCHEDULED_TIME", "10:00").strip())

    def validate_smtp_credentials(self) -> tuple[bool, Optional[str]]:
        """Validate presence of required SMTP credentials."""
        if not self.smtp_email:
            return False, "SMTP_EMAIL is missing or empty in environment / .env file."
        if not self.smtp_app_password:
            return False, "SMTP_APP_PASSWORD is missing or empty in environment / .env file."
        return True, None

    def get_sender_header(self) -> str:
        """Return formatted sender string: 'Sender Name <email@example.com>'."""
        if self.sender_name and self.smtp_email:
            return f"{self.sender_name} <{self.smtp_email}>"
        return self.smtp_email

    def to_safe_summary(self) -> dict[str, str]:
        """Return configuration dictionary with sanitized credentials for display/logs."""
        masked_pwd = "********" if self.smtp_app_password else "<NOT SET>"
        return {
            "SMTP Host": f"{self.smtp_host}:{self.smtp_port}",
            "SMTP Email": self.smtp_email or "<NOT SET>",
            "SMTP App Password": masked_pwd,
            "Campaign ID": self.campaign_id,
            "Campaign Subject": self.campaign_subject,
            "Rate Limit": f"{self.max_emails_per_hour} emails/hour",
            "Max Retries": str(self.max_retries),
            "Contacts CSV": str(self.contacts_csv_path),
            "Template HTML": str(self.email_template_path),
            "Email Log CSV": str(self.email_log_csv_path),
        }


# Singleton default config instance
def get_config() -> AppConfig:
    """Factory helper to obtain a fresh AppConfig instance."""
    return AppConfig()
