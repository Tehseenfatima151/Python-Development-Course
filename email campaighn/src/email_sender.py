"""Email sender module with Gmail SMTP, TLS, rate limiting, and retry handling.

Constructs RFC-compliant MIME messages, enforces hourly rate limits via a
sliding window, handles duplicate campaign prevention, and provides robust
error recovery with configurable retries.
"""

from __future__ import annotations

import email.utils
import logging
import smtplib
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any, Callable, Optional

from src.config import AppConfig
from src.logger import EmailAuditLogger
from src.template_engine import TemplateEngine
from src.validator import ContactRecord


logger = logging.getLogger("campaign_manager")


@dataclass
class DeliveryResult:
    """Outcome of an email delivery attempt."""

    contact: ContactRecord
    subject: str
    status: str  # "Sent", "Failed", "Skipped"
    error: Optional[str] = None
    retries_used: int = 0
    duration_seconds: float = 0.0


class RateLimiter:
    """Sliding-window rate limiter ensuring compliance with max emails per hour."""

    def __init__(self, max_per_hour: int = 50, pacing_delay_seconds: float = 1.0) -> None:
        self.max_per_hour = max(1, max_per_hour)
        self.pacing_delay_seconds = pacing_delay_seconds
        self.send_timestamps: list[float] = []

    def record_send(self) -> None:
        """Record the timestamp of an email send."""
        self.send_timestamps.append(time.time())

    def wait_if_needed(self, sleep_fn: Callable[[float], None] = time.sleep) -> float:
        """Wait if sending now would exceed the hourly rate limit.

        Returns:
            The number of seconds waited (0.0 if no limit hit).
        """
        now = time.time()
        one_hour_ago = now - 3600.0

        # Purge timestamps older than 1 hour (sliding window)
        self.send_timestamps = [t for t in self.send_timestamps if t > one_hour_ago]

        total_waited = 0.0

        if len(self.send_timestamps) >= self.max_per_hour:
            # Need to wait until the oldest timestamp in the current window is 3600s old
            oldest_in_window = self.send_timestamps[0]
            wait_time = max(0.1, (oldest_in_window + 3600.0) - now + 0.5)
            logger.warning(
                "Hourly rate limit reached (%d/%d). Pausing campaign for %.1f seconds...",
                len(self.send_timestamps),
                self.max_per_hour,
                wait_time,
            )
            sleep_fn(wait_time)
            total_waited += wait_time
            # Re-clean after waking up
            now = time.time()
            one_hour_ago = now - 3600.0
            self.send_timestamps = [t for t in self.send_timestamps if t > one_hour_ago]

        # Minimum polite pacing delay between individual dispatches
        if self.pacing_delay_seconds > 0:
            sleep_fn(self.pacing_delay_seconds)
            total_waited += self.pacing_delay_seconds

        return total_waited


class EmailSender:
    """Handles MIME assembly, SMTP connections, retry logic, and campaign dispatch."""

    def __init__(
        self,
        config: AppConfig,
        audit_logger: EmailAuditLogger,
        template_engine: TemplateEngine,
        smtp_client_factory: Optional[Callable[[], Any]] = None,
    ) -> None:
        self.config = config
        self.audit_logger = audit_logger
        self.template_engine = template_engine
        self.rate_limiter = RateLimiter(
            max_per_hour=config.max_emails_per_hour,
            pacing_delay_seconds=1.0,
        )
        self._smtp_client_factory = smtp_client_factory
        self._active_smtp: Optional[smtplib.SMTP] = None

    def build_message(self, contact: ContactRecord, extra_context: Optional[dict[str, Any]] = None) -> MIMEMultipart:
        """Construct a personalized multipart MIME email message."""
        context = {
            "name": contact.name,
            "email": contact.email,
            "campaign_id": self.config.campaign_id,
            "date": datetime.now().strftime("%B %d, %Y"),
        }
        if contact.extra_fields:
            context.update(contact.extra_fields)
        if extra_context:
            context.update(extra_context)

        # Render personalized subject
        rendered_subject = self.template_engine.render_subject(self.config.campaign_subject, context)

        # Render HTML body
        html_body = self.template_engine.render_html(context)

        # Fallback plain text representation
        plain_text = (
            f"Hello {contact.name},\n\n"
            f"You have received an update from {self.config.sender_name}.\n"
            f"Please view this email in an HTML-compatible email client for full content.\n\n"
            f"--\n{self.config.sender_name}"
        )

        msg = MIMEMultipart("alternative")
        msg["Subject"] = Header(rendered_subject, "utf-8")
        msg["From"] = self.config.get_sender_header()
        msg["To"] = email.utils.formataddr((contact.name, contact.email))
        msg["Date"] = email.utils.formatdate(localtime=True)
        msg["Message-ID"] = email.utils.make_msgid(domain=self.config.smtp_host)

        # Attach text/plain first, text/html second (RFC standard for alternative)
        part_plain = MIMEText(plain_text, "plain", "utf-8")
        part_html = MIMEText(html_body, "html", "utf-8")

        msg.attach(part_plain)
        msg.attach(part_html)

        return msg

    def connect_smtp(self) -> smtplib.SMTP:
        """Establish TLS encrypted connection to SMTP server and authenticate."""
        if self._smtp_client_factory is not None:
            return self._smtp_client_factory()

        valid, err = self.config.validate_smtp_credentials()
        if not valid:
            raise ValueError(f"SMTP Credential Error: {err}")

        logger.info(
            "Connecting to SMTP server %s:%d...",
            self.config.smtp_host,
            self.config.smtp_port,
        )

        server = smtplib.SMTP(self.config.smtp_host, self.config.smtp_port, timeout=30)
        try:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(self.config.smtp_email, self.config.smtp_app_password)
            logger.info("Successfully authenticated with SMTP server.")
            return server
        except Exception:
            try:
                server.close()
            except Exception:
                pass
            raise

    def send_single_email(
        self,
        contact: ContactRecord,
        smtp_server: Optional[smtplib.SMTP] = None,
        allow_resend: bool = False,
    ) -> DeliveryResult:
        """Deliver an email to a single contact with duplicate checks and retry handling."""
        start_time = time.time()

        # 1. Check for Duplicate Campaign Send
        if not allow_resend:
            already_sent = self.audit_logger.get_previously_sent_emails(self.config.campaign_id)
            if contact.email.lower() in already_sent:
                reason = f"Duplicate skipped: '{contact.email}' already received campaign '{self.config.campaign_id}'."
                logger.info(reason)
                self.audit_logger.log_event(
                    campaign_id=self.config.campaign_id,
                    name=contact.name,
                    email=contact.email,
                    subject=self.config.campaign_subject,
                    status="Skipped",
                    error="Already sent in this campaign",
                )
                return DeliveryResult(
                    contact=contact,
                    subject=self.config.campaign_subject,
                    status="Skipped",
                    error="Already sent in this campaign",
                    duration_seconds=time.time() - start_time,
                )

        # 2. Build MIME message
        try:
            msg = self.build_message(contact)
            subject = str(msg["Subject"])
        except Exception as e:
            err_msg = f"Failed to construct email: {e}"
            logger.error(err_msg)
            self.audit_logger.log_event(
                campaign_id=self.config.campaign_id,
                name=contact.name,
                email=contact.email,
                subject=self.config.campaign_subject,
                status="Failed",
                error=err_msg,
            )
            return DeliveryResult(
                contact=contact,
                subject=self.config.campaign_subject,
                status="Failed",
                error=err_msg,
                duration_seconds=time.time() - start_time,
            )

        # 3. Enforce Rate Limit before dispatch
        self.rate_limiter.wait_if_needed()

        # 4. Dispatch with Retry Mechanism
        attempts = 0
        last_error = None
        server = smtp_server if smtp_server is not None else self._active_smtp

        while attempts <= self.config.max_retries:
            attempts += 1
            try:
                # Ensure active connection
                if server is None:
                    server = self.connect_smtp()
                    self._active_smtp = server

                server.send_message(msg)
                self.rate_limiter.record_send()

                self.audit_logger.log_event(
                    campaign_id=self.config.campaign_id,
                    name=contact.name,
                    email=contact.email,
                    subject=subject,
                    status="Sent",
                    error="",
                )
                return DeliveryResult(
                    contact=contact,
                    subject=subject,
                    status="Sent",
                    retries_used=attempts - 1,
                    duration_seconds=time.time() - start_time,
                )

            except (smtplib.SMTPException, OSError, TimeoutError) as e:
                last_error = str(e)
                logger.warning(
                    "Attempt %d/%d failed for %s (%s): %s",
                    attempts,
                    self.config.max_retries + 1,
                    contact.name,
                    contact.email,
                    last_error,
                )
                # Reconnect if we have a factory or active connection; otherwise keep provided mock server
                if smtp_server is None or self._smtp_client_factory is not None:
                    try:
                        if server:
                            server.close()
                    except Exception:
                        pass
                    server = None
                    self._active_smtp = None

                if attempts <= self.config.max_retries:
                    time.sleep(self.config.retry_delay_seconds)
            except Exception as e:
                # Non-retryable critical exception
                last_error = f"Fatal delivery error: {e}"
                logger.error(last_error)
                break

        # If we reach here, all retries were exhausted
        err_msg = f"Delivery failed after {attempts} attempts: {last_error}"
        self.audit_logger.log_event(
            campaign_id=self.config.campaign_id,
            name=contact.name,
            email=contact.email,
            subject=subject,
            status="Failed",
            error=err_msg,
        )
        return DeliveryResult(
            contact=contact,
            subject=subject,
            status="Failed",
            error=err_msg,
            retries_used=attempts - 1,
            duration_seconds=time.time() - start_time,
        )

    def close(self) -> None:
        """Gracefully terminate active SMTP connection."""
        if self._active_smtp is not None:
            try:
                self._active_smtp.quit()
            except Exception:
                try:
                    self._active_smtp.close()
                except Exception:
                    pass
            finally:
                self._active_smtp = None
