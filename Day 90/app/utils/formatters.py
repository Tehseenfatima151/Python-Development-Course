"""
Formatting Utilities for InvoicePro
Formats currency amounts, dates, serial numbers, and physical quantities consistently.
"""
from datetime import datetime, date
from decimal import Decimal, ROUND_HALF_UP
from typing import Union


def format_currency(amount: Union[Decimal, float, int, str, None], symbol: str = "", decimals: int = 0) -> str:
    """
    Formats a numeric amount with commas and optional currency symbol.
    If decimals=0, numbers like 151500 are formatted as '151,500'.
    If decimals=2, formatted as '151,500.00'.
    """
    if amount is None or amount == "":
        return f"{symbol} 0" if symbol else "0"
    
    try:
        dec = Decimal(str(amount).replace(",", "").strip())
        if decimals == 0:
            formatted_num = f"{int(dec.quantize(Decimal('1'), rounding=ROUND_HALF_UP)):,}"
        else:
            formatted_num = f"{dec.quantize(Decimal('0.' + '0' * decimals), rounding=ROUND_HALF_UP):,}"
        
        if symbol:
            return f"{symbol} {formatted_num}".strip()
        return formatted_num
    except Exception:
        return str(amount)


def format_date(d: Union[date, datetime, str, None], fmt: str = "%d-%m-%Y") -> str:
    """
    Formats date objects or ISO strings into the target format (e.g. 16-08-2026).
    """
    if not d:
        return ""
    if isinstance(d, (date, datetime)):
        return d.strftime(fmt)
    if isinstance(d, str):
        for parse_fmt in ("%Y-%m-%d", "%d-%m-%Y", "%Y/%m/%d", "%d/%m/%Y", "%Y-%m-%dT%H:%M:%S"):
            try:
                dt = datetime.strptime(d.strip(), parse_fmt)
                return dt.strftime(fmt)
            except ValueError:
                continue
        return d
    return str(d)


def format_invoice_number(prefix: str, number: int, padding: int = 3) -> str:
    """
    Formats invoice number with prefix and padding (e.g. '468' or 'INV-00468').
    """
    if not prefix:
        return str(number)
    return f"{prefix}{str(number).zfill(padding)}"


def format_quantity_display(value: Union[Decimal, float, int, str, None], unit: str = "") -> str:
    """
    Formats a quantity value with its unit (e.g. '12kg' or '10 liter').
    """
    if value is None or str(value).strip() == "":
        return ""
    try:
        dec = Decimal(str(value))
        # Drop trailing zero if integer
        if dec == dec.to_integral():
            val_str = str(int(dec))
        else:
            val_str = str(dec.normalize())
    except Exception:
        val_str = str(value)
    
    unit_clean = unit.strip()
    if unit_clean:
        if unit_clean.lower() in ("kg", "g", "mg", "l", "ml"):
            return f"{val_str}{unit_clean}"
        return f"{val_str} {unit_clean}"
    return val_str
