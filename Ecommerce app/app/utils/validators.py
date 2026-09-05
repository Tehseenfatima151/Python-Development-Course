"""Input validation helpers."""
import re
from decimal import Decimal, InvalidOperation


EMAIL_RE = re.compile(r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$")


def validate_email(email: str) -> bool:
    return bool(email and EMAIL_RE.match(email.strip()))


def validate_password(password: str) -> tuple[bool, str]:
    """Return (valid, reason). Password must be ≥ 8 chars."""
    if not password:
        return False, "Password is required"
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    return True, ""


def validate_price(value) -> tuple[bool, str]:
    """Ensure price is a positive decimal number."""
    try:
        d = Decimal(str(value))
        if d <= 0:
            return False, "Price must be greater than zero"
        return True, ""
    except (InvalidOperation, TypeError):
        return False, "Price must be a valid number"


def validate_stock(value) -> tuple[bool, str]:
    """Ensure stock is a non-negative integer."""
    try:
        i = int(value)
        if i < 0:
            return False, "Stock cannot be negative"
        return True, ""
    except (ValueError, TypeError):
        return False, "Stock must be an integer"


def validate_quantity(value) -> tuple[bool, str]:
    """Ensure quantity is a positive integer."""
    try:
        i = int(value)
        if i <= 0:
            return False, "Quantity must be greater than zero"
        return True, ""
    except (ValueError, TypeError):
        return False, "Quantity must be a positive integer"
