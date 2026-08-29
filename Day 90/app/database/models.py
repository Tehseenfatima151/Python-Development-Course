"""
Database Models for InvoicePro
SQLAlchemy ORM models defining Companies, Customers, Invoices, Invoice Items, and Settings.
"""
from datetime import datetime, date
from decimal import Decimal
from sqlalchemy import (
    Column, Integer, String, Text, Date, DateTime, Numeric, Boolean, ForeignKey, event
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False, default="POULTRY SMART TRADERS")
    tagline = Column(String(255), nullable=True, default="")
    address = Column(String(300), nullable=True, default="23-A Gulshan Iqbal Alla Din Park, Karachi (Pak.)")
    phone = Column(String(100), nullable=True, default="")
    email = Column(String(150), nullable=True, default="poultrysmarttraders01@gmail.com")
    website = Column(String(150), nullable=True, default="")
    tax_id = Column(String(100), nullable=True, default="")
    reg_no = Column(String(100), nullable=True, default="")
    
    bank_name = Column(String(150), nullable=True, default="")
    bank_account = Column(String(100), nullable=True, default="")
    iban = Column(String(100), nullable=True, default="")
    payment_instructions = Column(Text, nullable=True, default="")

    default_currency = Column(String(20), default="Rs.")
    default_tax_rate = Column(Numeric(5, 2), default=Decimal("0.00"))
    invoice_prefix = Column(String(20), default="")
    next_invoice_number = Column(Integer, default=468)

    logo_path = Column(String(500), nullable=True)
    stamp_path = Column(String(500), nullable=True)
    signature_path = Column(String(500), nullable=True)
    sales_coordinator_name = Column(String(100), default="Dennis")
    footer_note = Column(String(255), default="")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    company_name = Column(String(200), nullable=True, default="")
    address = Column(String(300), nullable=True, default="")
    city = Column(String(100), nullable=True, default="")
    phone = Column(String(50), nullable=True, default="")
    email = Column(String(150), nullable=True, default="")
    tax_id = Column(String(100), nullable=True, default="")
    notes = Column(Text, nullable=True, default="")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    invoices = relationship("Invoice", back_populates="customer", cascade="all, delete-orphan")


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True)
    invoice_number = Column(String(50), nullable=False, unique=True, index=True)
    manual_no = Column(String(50), nullable=True, default="")
    dc_number_1 = Column(String(50), nullable=True, default="")
    dc_number_2 = Column(String(50), nullable=True, default="")
    order_number = Column(String(50), nullable=True, default="")

    invoice_date = Column(Date, nullable=False, default=date.today)
    due_date = Column(Date, nullable=True)

    delivered_to = Column(String(200), nullable=False, default="")
    invoiced_to = Column(String(200), nullable=True, default="Same")
    address = Column(String(300), nullable=True, default="")
    dispatch_info = Column(Text, nullable=True, default="")

    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    status = Column(String(30), default="paid", index=True)  # draft, sent, paid, pending, overdue, cancelled

    subtotal = Column(Numeric(14, 2), default=Decimal("0.00"))
    discount_type = Column(String(20), default="amount")  # amount, percent
    discount_value = Column(Numeric(14, 2), default=Decimal("0.00"))
    discount_amount = Column(Numeric(14, 2), default=Decimal("0.00"))
    
    tax_rate = Column(Numeric(5, 2), default=Decimal("0.00"))
    tax_amount = Column(Numeric(14, 2), default=Decimal("0.00"))
    shipping_charges = Column(Numeric(14, 2), default=Decimal("0.00"))
    other_charges = Column(Numeric(14, 2), default=Decimal("0.00"))

    total_amount = Column(Numeric(14, 2), default=Decimal("0.00"))  # Gross Amount
    invoice_amount = Column(Numeric(14, 2), default=Decimal("0.00")) # After discount + taxes
    total_due = Column(Numeric(14, 2), default=Decimal("0.00"))
    paid_amount = Column(Numeric(14, 2), default=Decimal("0.00"))
    balance_due = Column(Numeric(14, 2), default=Decimal("0.00"))

    amount_in_words = Column(String(300), nullable=True, default="")
    notes = Column(Text, nullable=True, default="")
    payment_terms = Column(Text, nullable=True, default="")
    pdf_path = Column(String(500), nullable=True)
    is_draft = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    customer = relationship("Customer", back_populates="invoices")
    items = relationship("InvoiceItem", back_populates="invoice", cascade="all, delete-orphan", order_by="InvoiceItem.serial_no")


class InvoiceItem(Base):
    __tablename__ = "invoice_items"

    id = Column(Integer, primary_key=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id", ondelete="CASCADE"), nullable=False)
    serial_no = Column(Integer, nullable=False, default=1)

    product_name = Column(String(255), nullable=False)
    packing = Column(String(100), nullable=True, default="")
    quantity_value = Column(Numeric(10, 2), nullable=False, default=Decimal("1.00"))
    quantity_unit = Column(String(50), nullable=True, default="")
    billing_quantity = Column(Numeric(10, 2), nullable=False, default=Decimal("1.00"))
    bonus = Column(String(100), nullable=True, default="")

    unit_rate = Column(Numeric(14, 2), nullable=False, default=Decimal("0.00"))
    discount_percent = Column(Numeric(5, 2), default=Decimal("0.00"))
    tax_percent = Column(Numeric(5, 2), default=Decimal("0.00"))
    amount = Column(Numeric(14, 2), nullable=False, default=Decimal("0.00"))

    # Relationship
    invoice = relationship("Invoice", back_populates="items")


class Setting(Base):
    __tablename__ = "settings"

    key = Column(String(100), primary_key=True)
    value = Column(Text, nullable=True)
