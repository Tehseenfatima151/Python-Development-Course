"""
Database Connection & Initialization
Initializes SQLite database engine, session factory, tables, and reference demo seed data.
"""
import logging
from datetime import date, datetime
from decimal import Decimal
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, scoped_session
from app.config import DATABASE_URL
from app.database.models import Base, Company, Customer, Invoice, InvoiceItem, Setting

logger = logging.getLogger(__name__)

# Create engine with foreign keys enabled in SQLite
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False
)


@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.close()


SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


def get_db():
    """Context manager / dependency for DB sessions."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Creates database tables and loads initial seed data if DB is empty."""
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        # Check if company exists
        company = session.query(Company).first()
        if not company:
            company = Company(
                name="POULTRY SMART TRADERS",
                tagline="",
                address="23-A Gulshan Iqbal Alla Din Park, Karachi (Pak.)",
                phone="",
                email="poultrysmarttraders01@gmail.com",
                website="",
                tax_id="",
                default_currency="Rs.",
                default_tax_rate=Decimal("0.00"),
                invoice_prefix="",
                next_invoice_number=469,
                sales_coordinator_name="Dennis",
                footer_note=""
            )
            session.add(company)
            session.commit()
            logger.info("Initialized default Company profile.")

        # Check if customer exists
        customer = session.query(Customer).first()
        if not customer:
            customer = Customer(
                name="Ijaz Ahmad",
                company_name="Ijaz Ahmad Poultry",
                address="Mian Chanu",
                city="Mian Chanu",
                phone="",
                email="",
                notes="Primary customer account"
            )
            session.add(customer)
            session.commit()
            logger.info("Initialized default Customer.")

        # Check if demo reference invoice exists
        demo_invoice = session.query(Invoice).filter_by(invoice_number="468").first()
        if not demo_invoice:
            demo_invoice = Invoice(
                invoice_number="468",
                manual_no="818406",
                dc_number_1="466",
                dc_number_2="82087",
                order_number="",
                invoice_date=date(2026, 8, 16),
                delivered_to="Ijaz Ahmad",
                invoiced_to="Same",
                address="Mian Chanu",
                dispatch_info="",
                customer_id=customer.id if customer else None,
                status="paid",
                subtotal=Decimal("151500.00"),
                discount_type="amount",
                discount_value=Decimal("0.00"),
                discount_amount=Decimal("0.00"),
                tax_rate=Decimal("0.00"),
                tax_amount=Decimal("0.00"),
                shipping_charges=Decimal("0.00"),
                other_charges=Decimal("0.00"),
                total_amount=Decimal("151500.00"),
                invoice_amount=Decimal("151500.00"),
                total_due=Decimal("151500.00"),
                paid_amount=Decimal("151500.00"),
                balance_due=Decimal("0.00"),
                amount_in_words="One Lac Fifty One Thousand Five Hundred",
                is_draft=False
            )
            session.add(demo_invoice)
            session.flush()

            # Add reference products
            items_data = [
                {
                    "serial_no": 1,
                    "product_name": "Medivit-C",
                    "packing": "1kg",
                    "quantity_value": Decimal("12.00"),
                    "quantity_unit": "kg",
                    "billing_quantity": Decimal("12.00"),
                    "bonus": "",
                    "unit_rate": Decimal("2250.00"),
                    "amount": Decimal("27000.00")
                },
                {
                    "serial_no": 2,
                    "product_name": "Livocina",
                    "packing": "5 liter",
                    "quantity_value": Decimal("10.00"),
                    "quantity_unit": "liter",
                    "billing_quantity": Decimal("10.00"),
                    "bonus": "",
                    "unit_rate": Decimal("2250.00"),
                    "amount": Decimal("22500.00")
                },
                {
                    "serial_no": 3,
                    "product_name": "Medi linco plus",
                    "packing": "5kg",
                    "quantity_value": Decimal("10.00"),
                    "quantity_unit": "kg",
                    "billing_quantity": Decimal("10.00"),
                    "bonus": "",
                    "unit_rate": Decimal("5500.00"),
                    "amount": Decimal("55000.00")
                },
                {
                    "serial_no": 4,
                    "product_name": "Lincocina",
                    "packing": "25kg",
                    "quantity_value": Decimal("50.00"),
                    "quantity_unit": "kg",
                    "billing_quantity": Decimal("2.00"),  # 50kg / 25kg = 2 bags
                    "bonus": "",
                    "unit_rate": Decimal("14000.00"),
                    "amount": Decimal("28000.00")
                },
                {
                    "serial_no": 5,
                    "product_name": "Medi Tylosin",
                    "packing": "25kg",
                    "quantity_value": Decimal("25.00"),
                    "quantity_unit": "kg",
                    "billing_quantity": Decimal("1.00"),  # 25kg / 25kg = 1 bag
                    "bonus": "",
                    "unit_rate": Decimal("19000.00"),
                    "amount": Decimal("19000.00")
                }
            ]

            for item_data in items_data:
                item = InvoiceItem(invoice_id=demo_invoice.id, **item_data)
                session.add(item)

            session.commit()
            logger.info("Initialized reference demo invoice #468.")

    except Exception as e:
        session.rollback()
        logger.error(f"Database initialization error: {e}")
        raise
    finally:
        session.close()
