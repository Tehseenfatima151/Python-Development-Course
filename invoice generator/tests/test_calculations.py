"""
Automated Tests for Calculation Service
Verifies Decimal arithmetic, line items, discounts, taxes, and grand totals.
"""
from decimal import Decimal
import pytest
from app.services.calculation_service import CalculationService, to_decimal


def test_to_decimal():
    assert to_decimal(150) == Decimal("150.00")
    assert to_decimal("2,250.50") == Decimal("2250.50")
    assert to_decimal("Rs. 151,500") == Decimal("151500.00")
    assert to_decimal(None) == Decimal("0.00")
    assert to_decimal("") == Decimal("0.00")


def test_calculate_line_item():
    # 12kg @ 2250 = 27,000
    amt1 = CalculationService.calculate_line_item(12, 2250)
    assert amt1 == Decimal("27000.00")

    # 10 liter @ 2250 = 22,500
    amt2 = CalculationService.calculate_line_item(10, 2250)
    assert amt2 == Decimal("22500.00")

    # 10kg @ 5500 = 55,000
    amt3 = CalculationService.calculate_line_item(10, 5500)
    assert amt3 == Decimal("55000.00")

    # 2 bags @ 14000 = 28,000
    amt4 = CalculationService.calculate_line_item(2, 14000)
    assert amt4 == Decimal("28000.00")

    # 1 bag @ 19000 = 19,000
    amt5 = CalculationService.calculate_line_item(1, 19000)
    assert amt5 == Decimal("19000.00")


def test_reference_demo_invoice_totals():
    items = [
        {"amount": Decimal("27000.00")},
        {"amount": Decimal("22500.00")},
        {"amount": Decimal("55000.00")},
        {"amount": Decimal("28000.00")},
        {"amount": Decimal("19000.00")}
    ]
    totals = CalculationService.calculate_invoice_totals(
        items=items,
        discount_type="amount",
        discount_value=0,
        tax_rate=0,
        shipping_charges=0,
        currency_name="Rupees"
    )
    assert totals["gross_amount"] == Decimal("151500.00")
    assert totals["discount_amount"] == Decimal("0.00")
    assert totals["tax_amount"] == Decimal("0.00")
    assert totals["invoice_amount"] == Decimal("151500.00")
    assert totals["total_due"] == Decimal("151500.00")
    assert "One Lac Fifty One Thousand Five Hundred" in totals["amount_in_words"]


def test_discount_and_tax_calculations():
    items = [
        {"amount": Decimal("10000.00")},
        {"amount": Decimal("5000.00")}
    ]
    # 10% discount on 15,000 = 1,500. Subtotal after discount = 13,500.
    # 5% tax on 13,500 = 675. Shipping = 500. Total = 14,675.
    totals = CalculationService.calculate_invoice_totals(
        items=items,
        discount_type="percent",
        discount_value=10,
        tax_rate=5,
        shipping_charges=500
    )
    assert totals["gross_amount"] == Decimal("15000.00")
    assert totals["discount_amount"] == Decimal("1500.00")
    assert totals["tax_amount"] == Decimal("675.00")
    assert totals["shipping_charges"] == Decimal("500.00")
    assert totals["invoice_amount"] == Decimal("14675.00")
    assert totals["total_due"] == Decimal("14675.00")


def test_empty_and_zero_items():
    totals = CalculationService.calculate_invoice_totals([])
    assert totals["gross_amount"] == Decimal("0.00")
    assert totals["invoice_amount"] == Decimal("0.00")
    assert totals["total_due"] == Decimal("0.00")
