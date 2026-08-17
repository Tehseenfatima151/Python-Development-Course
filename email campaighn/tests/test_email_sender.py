"""Unit tests for EmailSender and MIME construction using mock SMTP."""

import smtplib
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock

from src.config import AppConfig
from src.email_sender import DeliveryResult, EmailSender
from src.logger import EmailAuditLogger
from src.template_engine import TemplateEngine
from src.validator import ContactRecord


class TestEmailSender(unittest.TestCase):
    """Test suite for email message building, retry mechanisms, and mock SMTP delivery."""

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)

        # Setup dummy template
        self.template_file = self.temp_path / "template.html"
        self.template_file.write_text("<p>Hello {{name}}, welcome to our campaign.</p>", encoding="utf-8")

        # Setup audit log
        self.log_file = self.temp_path / "test_log.csv"
        self.audit_logger = EmailAuditLogger(self.log_file)
        self.template_engine = TemplateEngine(self.template_file)

        self.config = AppConfig(
            smtp_host="smtp.gmail.com",
            smtp_port=587,
            smtp_email="test_sender@gmail.com",
            smtp_app_password="test_app_password",
            campaign_id="test_campaign_01",
            campaign_subject="Hello {{name}} - Special Offer",
            max_emails_per_hour=100,
            max_retries=2,
            retry_delay_seconds=0.01,
            email_log_csv_path=self.log_file,
            email_template_path=self.template_file,
        )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_build_message_headers_and_parts(self) -> None:
        sender = EmailSender(self.config, self.audit_logger, self.template_engine)
        contact = ContactRecord(row_index=2, name="Ali", email="ali@example.com", is_valid=True)

        msg = sender.build_message(contact)

        self.assertEqual(str(msg["Subject"]), "Hello Ali - Special Offer")
        self.assertIn("ali@example.com", msg["To"])
        self.assertIn("test_sender@gmail.com", msg["From"])

        # Check payload parts (plain text fallback + HTML)
        payload = msg.get_payload()
        self.assertEqual(len(payload), 2)
        self.assertEqual(payload[0].get_content_type(), "text/plain")
        self.assertEqual(payload[1].get_content_type(), "text/html")
        self.assertIn("Hello Ali", payload[1].get_payload(decode=True).decode("utf-8"))

    def test_send_single_email_success_with_mock_smtp(self) -> None:
        mock_smtp = MagicMock(spec=smtplib.SMTP)
        sender = EmailSender(self.config, self.audit_logger, self.template_engine)
        sender.rate_limiter.pacing_delay_seconds = 0.0

        contact = ContactRecord(row_index=2, name="Sara", email="sara@example.com", is_valid=True)
        result: DeliveryResult = sender.send_single_email(contact, smtp_server=mock_smtp)

        self.assertEqual(result.status, "Sent")
        self.assertEqual(result.retries_used, 0)
        mock_smtp.send_message.assert_called_once()

        # Check that audit log recorded the send
        previously_sent = self.audit_logger.get_previously_sent_emails("test_campaign_01")
        self.assertIn("sara@example.com", previously_sent)

    def test_duplicate_send_prevention(self) -> None:
        mock_smtp = MagicMock(spec=smtplib.SMTP)
        sender = EmailSender(self.config, self.audit_logger, self.template_engine)
        sender.rate_limiter.pacing_delay_seconds = 0.0

        contact = ContactRecord(row_index=2, name="Ahmed", email="ahmed@example.com", is_valid=True)

        # First send
        res1 = sender.send_single_email(contact, smtp_server=mock_smtp)
        self.assertEqual(res1.status, "Sent")
        self.assertEqual(mock_smtp.send_message.call_count, 1)

        # Second send without allow_resend -> should be Skipped
        res2 = sender.send_single_email(contact, smtp_server=mock_smtp, allow_resend=False)
        self.assertEqual(res2.status, "Skipped")
        self.assertEqual(mock_smtp.send_message.call_count, 1)  # send_message was not called again

    def test_retry_on_transient_failure(self) -> None:
        mock_smtp = MagicMock(spec=smtplib.SMTP)
        # Fail on attempt 1, succeed on attempt 2
        mock_smtp.send_message.side_effect = [
            smtplib.SMTPServerDisconnected("Connection reset"),
            None,
        ]

        sender = EmailSender(self.config, self.audit_logger, self.template_engine)
        sender.rate_limiter.pacing_delay_seconds = 0.0

        contact = ContactRecord(row_index=2, name="Fatima", email="fatima@example.com", is_valid=True)
        result = sender.send_single_email(contact, smtp_server=mock_smtp)

        self.assertEqual(result.status, "Sent")
        self.assertEqual(result.retries_used, 1)
        self.assertEqual(mock_smtp.send_message.call_count, 2)

    def test_failure_after_exhausting_retries(self) -> None:
        mock_smtp = MagicMock(spec=smtplib.SMTP)
        # Always fail
        mock_smtp.send_message.side_effect = smtplib.SMTPException("Permanent SMTP error")

        sender = EmailSender(self.config, self.audit_logger, self.template_engine)
        sender.rate_limiter.pacing_delay_seconds = 0.0

        contact = ContactRecord(row_index=2, name="Bilal", email="bilal@example.com", is_valid=True)
        result = sender.send_single_email(contact, smtp_server=mock_smtp)

        self.assertEqual(result.status, "Failed")
        # 1 initial attempt + 2 retries = 3 attempts total
        self.assertEqual(mock_smtp.send_message.call_count, 3)
        self.assertIn("Permanent SMTP error", result.error)

    def test_reconnect_via_factory_on_retry(self) -> None:
        mock_conn_1 = MagicMock(spec=smtplib.SMTP)
        mock_conn_1.send_message.side_effect = smtplib.SMTPServerDisconnected("Lost connection")
        mock_conn_2 = MagicMock(spec=smtplib.SMTP)
        mock_conn_2.send_message.return_value = None

        connections = [mock_conn_1, mock_conn_2]
        factory = MagicMock(side_effect=lambda: connections.pop(0))

        sender = EmailSender(
            self.config,
            self.audit_logger,
            self.template_engine,
            smtp_client_factory=factory,
        )
        sender.rate_limiter.pacing_delay_seconds = 0.0

        contact = ContactRecord(row_index=2, name="Zainab", email="zainab@example.com", is_valid=True)
        result = sender.send_single_email(contact)

        self.assertEqual(result.status, "Sent")
        self.assertEqual(result.retries_used, 1)
        self.assertEqual(factory.call_count, 2)


if __name__ == "__main__":
    unittest.main()

