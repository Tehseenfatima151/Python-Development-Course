"""
Validation Utilities for InvoicePro
Validates user inputs to guarantee data integrity.
"""
import re
from decimal import Decimal, InvalidOperation
from typing import Tuple, Optional


def validate_email(email: str) -> bool:
    if not email or not email.strip():
        return True  # Optional field
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(pattern, email.strip()))


def validate_decimal(value, min_val: Optional[Decimal] = None, max_val: Optional[Decimal] = None) -> Tuple[bool, Optional[Decimal], str]:
    if value is None or str(value).strip() == "":
        return True, Decimal("0.00"), ""
    try:
        # Clean currency symbols or commas
        cleaned = str(value).replace(",", "").replace("$", "").replace("Rs.", "").replace("Rs", "").strip()
        dec = Decimal(cleaned)
        if min_val is not None and dec < min_val:
            return False, None, f"Value cannot be less than {min_val}"
        if max_val is not None and dec > max_val:
            return False, None, f"Value cannot exceed {max_val}"
        return True, dec, ""
    except (InvalidOperation, ValueError):
        return False, None, "Please enter a valid numeric value"


def validate_required(value: str, field_name: str = "Field") -> Tuple[bool, str]:
    if not value or not str(value).strip():
        return False, f"{field_name} is required."
    return True, ""


def validate_discount(value: Decimal, discount_type: str = "percent") -> Tuple[bool, str]:
    if discount_type == "percent":
        if value < Decimal("0") or value > Decimal("100"):
            return False, "Discount percentage must be between 0 and 100."
    else:
        if value < Decimal("0"):
            return False, "Discount amount cannot be negative."
    return True, ""


def validate_tax_rate(rate: Decimal) -> Tuple[bool, str]:
    if rate < Decimal("0") or rate > Decimal("100"):
        return False, "Tax rate must be between 0% and 100%."
    return True, ""
