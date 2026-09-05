"""Celery background tasks for transactional emails."""
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import current_app

from ..extensions import celery, db
from ..models.order import Order

logger = logging.getLogger(__name__)


@celery.task(bind=True, max_retries=3, default_retry_delay=60)
def send_order_confirmation_email(self, order_id: int) -> dict:
    """Send an HTML order confirmation email for the given order_id.

    Retries up to 3 times with a 60-second delay on transient SMTP errors.
    """
    try:
        order = db.session.get(Order, order_id)
        if not order:
            logger.error("send_order_confirmation_email: order id=%s not found", order_id)
            return {"success": False, "reason": "order_not_found"}

        user = order.user
        if not user:
            logger.error(
                "send_order_confirmation_email: user not found for order id=%s", order_id
            )
            return {"success": False, "reason": "user_not_found"}

        subject = f"Order Confirmation #{order.id} — Thank you for your purchase!"
        html_body = _build_email_html(order, user)
        text_body = _build_email_text(order, user)

        _send_email(
            to_address=user.email,
            to_name=user.name,
            subject=subject,
            html_body=html_body,
            text_body=text_body,
        )

        logger.info(
            "Order confirmation email sent: order_id=%s to=%s", order_id, user.email
        )
        return {"success": True, "order_id": order_id, "email": user.email}

    except smtplib.SMTPException as exc:
        logger.warning(
            "SMTP error sending confirmation for order id=%s: %s — retrying",
            order_id, exc,
        )
        raise self.retry(exc=exc)
    except Exception as exc:
        logger.exception(
            "Unexpected error sending confirmation for order id=%s", order_id
        )
        raise self.retry(exc=exc)


# ------------------------------------------------------------------ #
# Email builders
# ------------------------------------------------------------------ #

def _build_email_html(order, user) -> str:
    items_rows = ""
    for item in order.items:
        items_rows += f"""
        <tr>
            <td style="padding:8px;border-bottom:1px solid #eee;">{item.product_name}</td>
            <td style="padding:8px;border-bottom:1px solid #eee;text-align:center;">{item.quantity}</td>
            <td style="padding:8px;border-bottom:1px solid #eee;text-align:right;">${item.price:.2f}</td>
            <td style="padding:8px;border-bottom:1px solid #eee;text-align:right;">${item.subtotal:.2f}</td>
        </tr>"""

    return f"""
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>Order Confirmation</title></head>
<body style="font-family:Arial,sans-serif;background:#f9f9f9;margin:0;padding:0;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f9f9f9;padding:40px 0;">
    <tr><td align="center">
      <table width="600" cellpadding="0" cellspacing="0" style="background:#fff;border-radius:8px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,.1);">
        <tr>
          <td style="background:#4f46e5;padding:30px;text-align:center;">
            <h1 style="color:#fff;margin:0;font-size:24px;">Order Confirmed!</h1>
          </td>
        </tr>
        <tr>
          <td style="padding:30px;">
            <p style="font-size:16px;">Hi <strong>{user.name}</strong>,</p>
            <p>Thank you for your order. Here are your order details:</p>
            <table width="100%" cellpadding="0" cellspacing="0" style="border:1px solid #eee;border-radius:4px;margin:20px 0;">
              <thead>
                <tr style="background:#f3f4f6;">
                  <th style="padding:10px;text-align:left;">Product</th>
                  <th style="padding:10px;text-align:center;">Qty</th>
                  <th style="padding:10px;text-align:right;">Price</th>
                  <th style="padding:10px;text-align:right;">Subtotal</th>
                </tr>
              </thead>
              <tbody>{items_rows}</tbody>
            </table>
            <table width="100%" cellpadding="0" cellspacing="0">
              <tr>
                <td><strong>Order ID:</strong></td><td>#{order.id}</td>
              </tr>
              <tr>
                <td><strong>Date:</strong></td><td>{order.created_at.strftime('%B %d, %Y')}</td>
              </tr>
              <tr>
                <td><strong>Status:</strong></td>
                <td style="color:#16a34a;font-weight:bold;">{order.status.upper()}</td>
              </tr>
              <tr>
                <td><strong>Total:</strong></td>
                <td style="font-size:20px;font-weight:bold;color:#4f46e5;">${order.total_amount:.2f}</td>
              </tr>
            </table>
            <p style="margin-top:30px;color:#6b7280;font-size:14px;">
              If you have any questions, reply to this email.<br>
              Thank you for shopping with us!
            </p>
          </td>
        </tr>
        <tr>
          <td style="background:#f3f4f6;padding:20px;text-align:center;color:#9ca3af;font-size:12px;">
            &copy; 2026 E-Commerce Store. All rights reserved.
          </td>
        </tr>
      </table>
    </td></tr>
  </table>
</body>
</html>
"""


def _build_email_text(order, user) -> str:
    lines = [
        f"Order Confirmation #{order.id}",
        "=" * 40,
        f"Hi {user.name},",
        "",
        "Thank you for your order!",
        "",
        f"Order ID   : #{order.id}",
        f"Date       : {order.created_at.strftime('%B %d, %Y')}",
        f"Status     : {order.status.upper()}",
        "",
        "Items:",
        "-" * 40,
    ]
    for item in order.items:
        lines.append(
            f"  {item.product_name} x{item.quantity}  @ ${item.price:.2f} = ${item.subtotal:.2f}"
        )
    lines += [
        "-" * 40,
        f"  TOTAL: ${order.total_amount:.2f}",
        "",
        "Thank you for shopping with us!",
    ]
    return "\n".join(lines)


# ------------------------------------------------------------------ #
# SMTP sender
# ------------------------------------------------------------------ #

def _send_email(
    to_address: str, to_name: str, subject: str, html_body: str, text_body: str
) -> None:
    """Send a multipart HTML+text email via SMTP."""
    cfg = current_app.config

    smtp_host = cfg["SMTP_HOST"]
    smtp_port = cfg["SMTP_PORT"]
    smtp_user = cfg["SMTP_USERNAME"]
    smtp_pass = cfg["SMTP_PASSWORD"]
    from_email = cfg["SMTP_FROM_EMAIL"]

    if not smtp_user or not smtp_pass:
        logger.warning(
            "SMTP credentials not configured — skipping email send for %s", to_address
        )
        return

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"E-Commerce Store <{from_email}>"
    msg["To"] = f"{to_name} <{to_address}>"

    msg.attach(MIMEText(text_body, "plain"))
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.ehlo()
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail(from_email, to_address, msg.as_string())
