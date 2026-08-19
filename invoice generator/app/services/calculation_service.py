"""
Calculation Service for InvoicePro
High-precision Decimal calculations for line items, subtotals, discounts, taxes, totals, and words.
"""
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
from typing import List, Dict, Any, Union
from app.utils.num_to_words import amount_to_words


def to_decimal(val: Union[Decimal, float, int, str, None], default: str = "0.00") -> Decimal:
    """Safely converts any input value into a 2-decimal place Decimal."""
    if val is None or str(val).strip() == "":
        return Decimal(default)
    try:
        cleaned = str(val).replace(",", "").replace("$", "").replace("Rs.", "").replace("Rs", "").strip()
        return Decimal(cleaned).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    except (InvalidOperation, ValueError):
        return Decimal(default)


class CalculationService:
    @staticmethod
    def calculate_line_item(
        billing_quantity: Union[Decimal, float, int, str],
        unit_rate: Union[Decimal, float, int, str],
        discount_percent: Union[Decimal, float, int, str] = 0,
        tax_percent: Union[Decimal, float, int, str] = 0
    ) -> Decimal:
        """
        Calculates line item amount: (billing_quantity * unit_rate) - line_discount.
        Uses pure Decimal arithmetic.
        """
        qty = to_decimal(billing_quantity, "1.00")
        rate = to_decimal(unit_rate, "0.00")
        disc_pct = to_decimal(discount_percent, "0.00")

        base_amount = qty * rate
        disc_amount = (base_amount * disc_pct / Decimal("100.00")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        net_amount = (base_amount - disc_amount).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return max(Decimal("0.00"), net_amount)

    @staticmethod
    def calculate_invoice_totals(
        items: List[Dict[str, Any]],
        discount_type: str = "amount",
        discount_value: Union[Decimal, float, int, str] = 0,
        tax_rate: Union[Decimal, float, int, str] = 0,
        shipping_charges: Union[Decimal, float, int, str] = 0,
        other_charges: Union[Decimal, float, int, str] = 0,
        paid_amount: Union[Decimal, float, int, str] = 0,
        currency_name: str = "Rupees"
    ) -> Dict[str, Any]:
        """
        Calculates gross amount, discount amount, tax amount, invoice amount, total due, balance, and words.
        """
        # Calculate gross amount (sum of all line item amounts)
        gross_amount = Decimal("0.00")
        for itm in items:
            amt = to_decimal(itm.get("amount", 0))
            gross_amount += amt
        
        gross_amount = gross_amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        # Discount
        disc_val = to_decimal(discount_value, "0.00")
        if discount_type == "percent":
            discount_amount = (gross_amount * disc_val / Decimal("100.00")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        else:
            discount_amount = disc_val.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        discount_amount = min(gross_amount, max(Decimal("0.00"), discount_amount))
        discounted_subtotal = gross_amount - discount_amount

        # Tax
        tax_pct = to_decimal(tax_rate, "0.00")
        tax_amount = (discounted_subtotal * tax_pct / Decimal("100.00")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        # Additional Charges
        shipping = to_decimal(shipping_charges, "0.00")
        other = to_decimal(other_charges, "0.00")

        # Invoice Amount (Grand Total)
        invoice_amount = (discounted_subtotal + tax_amount + shipping + other).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        total_due = invoice_amount

        # Paid & Balance
        paid = to_decimal(paid_amount, "0.00")
        balance_due = max(Decimal("0.00"), total_due - paid)

        # Words representation
        words = amount_to_words(invoice_amount, currency_name="", system="south_asian")

        return {
            "subtotal": gross_amount,
            "gross_amount": gross_amount,
            "discount_type": discount_type,
            "discount_value": disc_val,
            "discount_amount": discount_amount,
            "tax_rate": tax_pct,
            "tax_amount": tax_amount,
            "shipping_charges": shipping,
            "other_charges": other,
            "total_amount": gross_amount,
            "invoice_amount": invoice_amount,
            "total_due": total_due,
            "paid_amount": paid,
            "balance_due": balance_due,
            "amount_in_words": words
        }
