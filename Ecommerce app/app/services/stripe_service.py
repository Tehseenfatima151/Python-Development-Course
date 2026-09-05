"""Stripe integration service.

All Stripe API calls are encapsulated here so routes stay thin and
the service layer is independently testable with mocks.
"""
import logging

import stripe
from flask import current_app

from ..models.order import Order

logger = logging.getLogger(__name__)


def get_stripe_client():
    """Return a configured stripe module (sets api_key as side-effect)."""
    stripe.api_key = current_app.config["STRIPE_SECRET_KEY"]
    return stripe


def create_checkout_session(order: Order, success_url: str, cancel_url: str) -> stripe.checkout.Session:
    """Create a Stripe Checkout Session for the given order.

    Line items are built from the order's snapshotted OrderItems so prices
    always match what was committed to the database — never from the frontend.
    """
    client = get_stripe_client()

    line_items = []
    for item in order.items:
        line_items.append({
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": item.product_name,
                },
                # Stripe expects amounts in the smallest currency unit (cents)
                "unit_amount": item.price_cents,
            },
            "quantity": item.quantity,
        })

    session = client.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        mode="payment",
        success_url=success_url,
        cancel_url=cancel_url,
        metadata={
            "order_id": str(order.id),
            "user_id": str(order.user_id),
        },
        # Attach order reference to the payment intent as well
        payment_intent_data={
            "metadata": {
                "order_id": str(order.id),
                "user_id": str(order.user_id),
            }
        },
    )

    logger.info(
        "Stripe Checkout Session created: session_id=%s order_id=%s",
        session.id, order.id,
    )
    return session


def construct_webhook_event(payload: bytes, sig_header: str, webhook_secret: str):
    """Verify and parse an incoming Stripe webhook event.

    Raises stripe.error.SignatureVerificationError if the signature is invalid.
    """
    client = get_stripe_client()
    return client.Webhook.construct_event(payload, sig_header, webhook_secret)
