"""
Automated Tests for PDF Generation and Text Formatters
"""
import os
import pypdf
import pytest
from datetime import date
from decimal import Decimal

from app.services.pdf_service import PDFService
from app.utils.formatters import format_currency, format_date, format_quantity_display
from app.utils.num_to_words import amount_to_words, convert_south_asian, convert_western
from app.utils.validators import validate_email, validate_decimal, validate_discount, validate_tax_rate


def test_pdf_generation_content(tmp_path):
    output_pdf = str(tmp_path / "test_invoice.pdf")
    
    invoice_data = {
        "invoice_number": "468",
        "manual_no": "818406",
        "dc_number_1": "466",
        "dc_number_2": "82087",
        "order_number": "",
        "invoice_date": date(2026, 8, 16),
        "delivered_to": "Ijaz Ahmad",
        "invoiced_to": "Same",
        "address": "Mian Chanu",
        "dispatch_info": "",
        "gross_amount": Decimal("151500.00"),
        "discount_amount": Decimal("0.00"),
        "invoice_amount": Decimal("151500.00"),
        "total_due": Decimal("151500.00"),
        "amount_in_words": "One Lac Fifty One Thousand Five Hundred",
    }

    items_data = [
        {"serial_no": 1, "product_name": "Medivit-C", "packing": "1kg", "quantity_value": 12, "quantity_unit": "kg", "unit_rate": 2250, "amount": 27000},
        {"serial_no": 2, "product_name": "Livocina", "packing": "5 liter", "quantity_value": 10, "quantity_unit": "liter", "unit_rate": 2250, "amount": 22500},
        {"serial_no": 3, "product_name": "Medi linco plus", "packing": "5kg", "quantity_value": 10, "quantity_unit": "kg", "unit_rate": 5500, "amount": 55000},
        {"serial_no": 4, "product_name": "Lincocina", "packing": "25kg", "quantity_value": 50, "quantity_unit": "kg", "unit_rate": 14000, "amount": 28000},
        {"serial_no": 5, "product_name": "Medi Tylosin", "packing": "25kg", "quantity_value": 25, "quantity_unit": "kg", "unit_rate": 19000, "amount": 19000},
    ]

    company_data = {
        "name": "POULTRY SMART TRADERS",
        "address": "23-A Gulshan Iqbal Alla Din Park, Karachi (Pak.)",
        "email": "poultrysmarttraders01@gmail.com",
        "sales_coordinator_name": "Dennis"
    }

    path = PDFService.generate_invoice_pdf(invoice_data, items_data, company_data, output_path=output_pdf)
    assert os.path.exists(path)
    assert os.path.getsize(path) > 1000

    # Verify extracted text
    reader = pypdf.PdfReader(path)
    assert len(reader.pages) >= 1
    page_text = reader.pages[0].extract_text()
    
    assert "POULTRY SMART TRADERS" in page_text
    assert "SALE INVOICE" in page_text
    assert "818406" in page_text
    assert "468" in page_text
    assert "466" in page_text
    assert "82087" in page_text
    assert "Ijaz Ahmad" in page_text
    assert "Medivit-C" in page_text
    assert "Livocina" in page_text
    assert "151,500" in page_text
    assert "One Lac Fifty One Thousand Five Hundred" in page_text
    assert "Dennis" in page_text
    assert "Sales Coordinator" in page_text


def test_amount_to_words():
    # Test South Asian Lakhs format
    assert convert_south_asian(151500) == "One Lac Fifty One Thousand Five Hundred"
    assert convert_south_asian(100000) == "One Lac"
    assert convert_south_asian(10000000) == "One Crore"
    assert convert_south_asian(27000) == "Twenty Seven Thousand"

    words = amount_to_words(151500, currency_name="Rupees", system="south_asian")
    assert words == "Rupees One Lac Fifty One Thousand Five Hundred"

    # Test Western format
    assert convert_western(1500000) == "One Million Five Hundred Thousand"


def test_formatters():
    assert format_currency(151500, decimals=0) == "151,500"
    assert format_currency(151500.5, decimals=2) == "151,500.50"
    assert format_currency(151500, symbol="Rs.", decimals=0) == "Rs. 151,500"
    assert format_quantity_display(12, "kg") == "12kg"
    assert format_quantity_display(10, "liter") == "10 liter"
    assert format_date("2026-08-16") == "16-08-2026"


def test_validators():
    assert validate_email("poultrysmarttraders01@gmail.com") is True
    assert validate_email("invalid-email") is False

    valid, val, _ = validate_decimal("151,500.00")
    assert valid is True
    assert val == Decimal("151500.00")

    disc_valid, _ = validate_discount(Decimal("15"), "percent")
    assert disc_valid is True
    disc_invalid, _ = validate_discount(Decimal("150"), "percent")
    assert disc_invalid is False

    tax_valid, _ = validate_tax_rate(Decimal("17.5"))
    assert tax_valid is True
