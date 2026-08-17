"""Automated Bulk Email Campaign Manager - CLI Entrypoint.

Provides commands for contact validation, email dry-runs, immediate dispatch,
scheduled launches, and campaign deliverability statistics.
"""

from __future__ import annotations

import argparse
import sys
import time
from datetime import datetime
from pathlib import Path

# Add project root to sys.path if running as script directly
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import AppConfig, get_config
from src.email_sender import DeliveryResult, EmailSender
from src.logger import EmailAuditLogger, setup_application_logger
from src.scheduler import CampaignScheduler
from src.template_engine import TemplateEngine
from src.validator import ContactValidator, ValidationReport


def print_banner(title: str = "AUTOMATED EMAIL CAMPAIGN MANAGER") -> None:
    """Print standard styled terminal header."""
    print("=" * 44)
    print(f" {title.center(42)} ")
    print("=" * 44)


def run_validation(config: AppConfig) -> tuple[bool, ValidationReport | None]:
    """Validate contacts CSV and HTML email template without sending."""
    print_banner("VALIDATING CAMPAIGN ASSETS")

    # 1. Validate Template
    print(f"Checking HTML Template: {config.email_template_path.name}")
    try:
        engine = TemplateEngine(config.email_template_path)
        template_content = engine.load_template()
        print(f"  [OK] HTML Template loaded successfully ({len(template_content):,} bytes).")
    except Exception as e:
        print(f"  [ERROR] Template Error: {e}")
        return False, None

    # 2. Validate Contacts CSV
    print(f"\nChecking Contacts File: {config.contacts_csv_path.name}")
    try:
        validator = ContactValidator(config.contacts_csv_path)
        df, report = validator.validate()
    except Exception as e:
        print(f"  [ERROR] CSV Validation Error: {e}")
        return False, None

    print(f"  Total Records in CSV : {report.total_rows}")
    print(f"  Valid Deliverable     : {report.valid_count}")
    print(f"  Invalid / Skipped     : {report.invalid_count}")

    if report.invalid_contacts:
        print("\nSkipped / Invalid Records Summary:")
        for inv in report.invalid_contacts:
            print(f"  - {inv.error_reason}")

    if report.valid_count == 0:
        print("\n[WARNING] No valid contacts found to send.")
        return False, report

    print("\n[SUCCESS] Validation passed! Ready for campaign dispatch.")
    return True, report


def run_dry_run(config: AppConfig) -> None:
    """Simulate email generation and personalization without SMTP network traffic."""
    print_banner("CAMPAIGN DRY RUN (SIMULATION)")
    print(f"Campaign ID      : {config.campaign_id}")
    print(f"Subject Template : {config.campaign_subject}")
    print(f"Rate Limit       : {config.max_emails_per_hour} emails/hour (simulated)\n")

    try:
        validator = ContactValidator(config.contacts_csv_path)
        df, report = validator.validate()
    except Exception as e:
        print(f"[ERROR] Failed to load contacts: {e}")
        sys.exit(1)

    try:
        engine = TemplateEngine(config.email_template_path)
        engine.load_template()
    except Exception as e:
        print(f"[ERROR] Failed to load template: {e}")
        sys.exit(1)

    audit_logger = EmailAuditLogger(config.email_log_csv_path)
    already_sent = audit_logger.get_previously_sent_emails(config.campaign_id)

    if report.invalid_contacts:
        print(f"[NOTE] {len(report.invalid_contacts)} invalid contact(s) will be automatically skipped.")

    print(f"\nRendering {report.valid_count} personalized emails:\n" + "-" * 44)

    for idx, contact in enumerate(report.valid_contacts, start=1):
        context = {
            "name": contact.name,
            "email": contact.email,
            "campaign_id": config.campaign_id,
            "date": datetime.now().strftime("%B %d, %Y"),
        }
        if contact.extra_fields:
            context.update(contact.extra_fields)

        rendered_subject = engine.render_subject(config.campaign_subject, context)
        is_duplicate = contact.email.lower() in already_sent
        status = "Ready (Duplicate - Will be skipped unless --allow-resend)" if is_duplicate else "Ready"

        print(f"[{idx}/{report.valid_count}] [DRY RUN]")
        print(f"  Recipient : {contact.name}")
        print(f"  Email     : {contact.email}")
        print(f"  Subject   : {rendered_subject}")
        print(f"  Status    : {status}")
        print("-" * 44)

    print("\n[DRY RUN COMPLETED] No emails were transmitted to SMTP server.")


def run_campaign_send(config: AppConfig, allow_resend: bool = False) -> None:
    """Execute live campaign dispatch via Gmail SMTP."""
    start_total_time = time.time()
    logger = setup_application_logger(config.application_log_path)
    logger.info("Initiating campaign dispatch (ID: %s)", config.campaign_id)

    print("========================================")
    print("AUTOMATED EMAIL CAMPAIGN MANAGER")
    print("Loading contacts...")

    try:
        validator = ContactValidator(config.contacts_csv_path)
        df, report = validator.validate()
    except Exception as e:
        print(f"[ERROR] Failed to load contacts CSV: {e}")
        logger.error("Contacts validation failed: %s", e)
        sys.exit(1)

    print("Validating contacts...")
    print(f"Found {report.valid_count} valid contact(s), {report.invalid_count} invalid contact(s).")

    if report.valid_count == 0:
        print("[ERROR] No valid recipients to process. Aborting campaign.")
        sys.exit(1)

    print("Loading email template...")
    try:
        template_engine = TemplateEngine(config.email_template_path)
        template_engine.load_template()
    except Exception as e:
        print(f"[ERROR] Failed to load email template: {e}")
        logger.error("Template loading failed: %s", e)
        sys.exit(1)

    print("Connecting to Gmail SMTP...")
    audit_logger = EmailAuditLogger(config.email_log_csv_path)
    sender = EmailSender(
        config=config,
        audit_logger=audit_logger,
        template_engine=template_engine,
    )

    try:
        smtp_conn = sender.connect_smtp()
    except Exception as e:
        print(f"\n[ERROR] SMTP Connection/Authentication Failed: {e}")
        print("Please check your SMTP_EMAIL and SMTP_APP_PASSWORD settings in .env")
        logger.error("SMTP connection error: %s", e)
        sys.exit(1)

    total_recipients = report.valid_count
    print(f"Campaign: {config.campaign_id}")
    print(f"Recipients: {total_recipients}")
    print(f"Rate Limit: {config.max_emails_per_hour} emails/hour")
    print("Sending...")

    sent_count = 0
    failed_count = 0
    skipped_count = report.invalid_count

    # Log initial invalid contacts as Skipped in audit log
    for inv in report.invalid_contacts:
        audit_logger.log_event(
            campaign_id=config.campaign_id,
            name=inv.name or "N/A",
            email=inv.email or "N/A",
            subject=config.campaign_subject,
            status="Skipped",
            error=inv.error_reason or "Invalid contact record",
        )

    # Deliver to each valid contact
    for idx, contact in enumerate(report.valid_contacts, start=1):
        result: DeliveryResult = sender.send_single_email(
            contact=contact,
            smtp_server=smtp_conn,
            allow_resend=allow_resend,
        )

        if result.status == "Sent":
            sent_count += 1
            print(f"[{idx}/{total_recipients}] {contact.name} -> Sent")
        elif result.status == "Skipped":
            skipped_count += 1
            print(f"[{idx}/{total_recipients}] {contact.name} -> Skipped ({result.error})")
        else:
            failed_count += 1
            print(f"[{idx}/{total_recipients}] {contact.name} -> Failed ({result.error})")

    sender.close()
    elapsed = time.time() - start_total_time

    print("========================================")
    print("CAMPAIGN COMPLETED")
    print(f"Total: {report.total_rows}")
    print(f"Sent: {sent_count}")
    print(f"Failed: {failed_count}")
    print(f"Skipped: {skipped_count}")
    print(f"Execution Time: {elapsed:.2f} seconds")
    print(f"Check {config.email_log_csv_path} for details.")
    print("========================================")

    logger.info(
        "Campaign finished. Total: %d, Sent: %d, Failed: %d, Skipped: %d in %.2fs",
        report.total_rows,
        sent_count,
        failed_count,
        skipped_count,
        elapsed,
    )


def show_statistics(config: AppConfig) -> None:
    """Display summary analytics from logs/email_log.csv."""
    print_banner("CAMPAIGN AUDIT & DELIVERY STATISTICS")
    audit_logger = EmailAuditLogger(config.email_log_csv_path)
    stats = audit_logger.get_campaign_statistics()

    if not stats:
        print(f"No delivery logs found in: {config.email_log_csv_path}")
        print("Run a campaign with --send-now to record delivery activity.")
        return

    print(f"Log File: {config.email_log_csv_path}\n")
    for campaign_id, data in stats.items():
        print(f"Campaign ID       : {campaign_id}")
        print(f"  Total Attempts  : {data['total_attempts']}")
        print(f"  Successfully Sent: {data['sent']}")
        print(f"  Failed          : {data['failed']}")
        print(f"  Skipped         : {data['skipped']}")
        print(f"  Activity Window : {data['first_activity']} -> {data['last_activity']}")
        print("-" * 44)


def main() -> None:
    """Main CLI entrypoint parser."""
    parser = argparse.ArgumentParser(
        description="Automated Bulk Email Campaign Manager for Marketing Agencies.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--validate",
        action="store_true",
        help="Validate contacts CSV schema, email formats, and template integrity without sending.",
    )
    group.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate the campaign, render personalized emails, and verify pipeline without SMTP connection.",
    )
    group.add_argument(
        "--send-now",
        action="store_true",
        help="Connect to Gmail SMTP and immediately dispatch personalized emails with rate limiting.",
    )
    group.add_argument(
        "--schedule",
        action="store_true",
        help="Wait until the date/time configured in .env (SCHEDULED_DATE & SCHEDULED_TIME) to start sending.",
    )
    group.add_argument(
        "--stats",
        action="store_true",
        help="Display historical deliverability statistics and metrics from email_log.csv.",
    )
    parser.add_argument(
        "--allow-resend",
        action="store_true",
        help="Allow re-sending to contacts that have already been sent this campaign ID.",
    )

    args = parser.parse_args()
    config = get_config()

    if args.validate:
        run_validation(config)
    elif args.dry_run:
        run_dry_run(config)
    elif args.send_now:
        run_campaign_send(config, allow_resend=args.allow_resend)
    elif args.schedule:
        # Validate assets first before entering waiting state
        valid, _ = run_validation(config)
        if not valid:
            print("[ERROR] Pre-flight validation failed. Scheduled launch aborted.")
            sys.exit(1)

        scheduler = CampaignScheduler(
            target_time_str=config.scheduled_time,
            target_date_str=config.scheduled_date or None,
        )
        scheduler.run_scheduled_job(lambda: run_campaign_send(config, allow_resend=args.allow_resend))
    elif args.stats:
        show_statistics(config)
    else:
        parser.print_help()
        print("\n[NOTE] Safe mode: No emails are sent without specifying --send-now or --schedule.")


if __name__ == "__main__":
    main()
