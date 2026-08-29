"""
Automated Tests for Database and Repositories
"""
import pytest
from datetime import date
from decimal import Decimal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.models import Base, Company, Customer, Invoice, InvoiceItem
from app.database.repositories import CompanyRepository, CustomerRepository, InvoiceRepository
from app.services.invoice_service import InvoiceService


@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


def test_company_crud(db_session):
    company = CompanyRepository.update_company(db_session, {
        "name": "POULTRY SMART TRADERS",
        "email": "poultrysmarttraders01@gmail.com",
        "next_invoice_number": 468
    })
    assert company.id is not None
    assert company.name == "POULTRY SMART TRADERS"
    assert company.next_invoice_number == 468

    next_num = CompanyRepository.increment_invoice_number(db_session)
    assert next_num == 468
    assert company.next_invoice_number == 469


def test_customer_crud(db_session):
    cust = CustomerRepository.create(db_session, {
        "name": "Ijaz Ahmad",
        "company_name": "Ijaz Ahmad Poultry",
        "city": "Mian Chanu"
    })
    assert cust.id is not None
    assert cust.name == "Ijaz Ahmad"

    fetched = CustomerRepository.get_by_id(db_session, cust.id)
    assert fetched.city == "Mian Chanu"

    results = CustomerRepository.get_all(db_session, search="Ijaz")
    assert len(results) == 1

    deleted = CustomerRepository.delete(db_session, cust.id)
    assert deleted is True
    assert CustomerRepository.get_by_id(db_session, cust.id) is None


def test_invoice_creation_and_cascade(db_session):
    CompanyRepository.update_company(db_session, {"name": "POULTRY SMART TRADERS", "next_invoice_number": 468})
    cust = CustomerRepository.create(db_session, {"name": "Ijaz Ahmad"})

    inv_data = {
        "invoice_number": "468",
        "manual_no": "818406",
        "dc_number_1": "466",
        "dc_number_2": "82087",
        "invoice_date": date(2026, 8, 16),
        "delivered_to": "Ijaz Ahmad",
        "customer_id": cust.id,
        "status": "paid"
    }

    items_data = [
        {"product_name": "Medivit-C", "packing": "1kg", "quantity_value": 12, "unit_rate": 2250},
        {"product_name": "Livocina", "packing": "5 liter", "quantity_value": 10, "unit_rate": 2250},
    ]

    success, inv, msg = InvoiceService.create_invoice(db_session, inv_data, items_data, generate_pdf=False)
    assert success is True
    assert inv is not None
    assert inv.invoice_number == "468"
    assert len(inv.items) == 2
    assert inv.invoice_amount == Decimal("49500.00")

    # Duplicate invoice (generates unique number e.g. 469)
    dup_success, dup_inv, dup_msg = InvoiceService.duplicate_invoice(db_session, inv.id, generate_pdf=False)
    assert dup_success is True
    assert dup_inv is not None
    assert dup_inv.id != inv.id
    assert dup_inv.invoice_number != inv.invoice_number
    assert len(dup_inv.items) == 2

    # Cascade delete original
    InvoiceRepository.delete(db_session, inv.id)
    assert InvoiceRepository.get_by_id(db_session, inv.id) is None
