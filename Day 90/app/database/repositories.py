"""
Database Repositories
Encapsulates CRUD queries, transactions, searching, and filtering.
"""
from datetime import date
from decimal import Decimal
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, desc, func
from app.database.models import Company, Customer, Invoice, InvoiceItem, Setting


class CompanyRepository:
    @staticmethod
    def get_company(session: Session) -> Optional[Company]:
        return session.query(Company).first()

    @staticmethod
    def update_company(session: Session, data: Dict[str, Any]) -> Company:
        company = session.query(Company).first()
        if not company:
            company = Company()
            session.add(company)
        
        for key, value in data.items():
            if hasattr(company, key):
                setattr(company, key, value)
        
        session.commit()
        session.refresh(company)
        return company

    @staticmethod
    def get_next_available_invoice_number(session: Session) -> str:
        company = session.query(Company).first()
        prefix = company.invoice_prefix if company else ""
        current_no = (company.next_invoice_number if company else 468) or 1

        # Check if number already exists in invoices, if so increment until unique
        while True:
            candidate = f"{prefix}{current_no}" if prefix else str(current_no)
            existing = session.query(Invoice).filter(Invoice.invoice_number == candidate).first()
            if not existing:
                break
            current_no += 1

        if company:
            company.next_invoice_number = current_no + 1
            session.commit()
        
        return candidate

    @staticmethod
    def increment_invoice_number(session: Session) -> int:
        company = session.query(Company).first()
        if company:
            current_no = company.next_invoice_number or 1
            company.next_invoice_number = current_no + 1
            session.commit()
            return current_no
        return 1


class CustomerRepository:
    @staticmethod
    def get_all(session: Session, search: str = "") -> List[Customer]:
        query = session.query(Customer)
        if search:
            s = f"%{search.strip()}%"
            query = query.filter(or_(
                Customer.name.ilike(s),
                Customer.company_name.ilike(s),
                Customer.phone.ilike(s),
                Customer.email.ilike(s),
                Customer.city.ilike(s)
            ))
        return query.order_by(Customer.name.asc()).all()

    @staticmethod
    def get_by_id(session: Session, customer_id: int) -> Optional[Customer]:
        return session.query(Customer).filter(Customer.id == customer_id).first()

    @staticmethod
    def create(session: Session, data: Dict[str, Any]) -> Customer:
        customer = Customer(**data)
        session.add(customer)
        session.commit()
        session.refresh(customer)
        return customer

    @staticmethod
    def update(session: Session, customer_id: int, data: Dict[str, Any]) -> Optional[Customer]:
        customer = session.query(Customer).filter(Customer.id == customer_id).first()
        if not customer:
            return None
        for key, value in data.items():
            if hasattr(customer, key):
                setattr(customer, key, value)
        session.commit()
        session.refresh(customer)
        return customer

    @staticmethod
    def delete(session: Session, customer_id: int) -> bool:
        customer = session.query(Customer).filter(Customer.id == customer_id).first()
        if customer:
            session.delete(customer)
            session.commit()
            return True
        return False

    @staticmethod
    def get_customer_stats(session: Session, customer_id: int) -> Dict[str, Any]:
        invoices = session.query(Invoice).filter(Invoice.customer_id == customer_id).all()
        total_invoices = len(invoices)
        total_spent = sum((inv.invoice_amount or Decimal("0.00")) for inv in invoices if inv.status != "cancelled")
        total_paid = sum((inv.paid_amount or Decimal("0.00")) for inv in invoices if inv.status != "cancelled")
        total_due = sum((inv.balance_due or Decimal("0.00")) for inv in invoices if inv.status not in ("cancelled", "draft"))
        return {
            "invoice_count": total_invoices,
            "total_spent": total_spent,
            "total_paid": total_paid,
            "total_due": total_due,
            "invoices": invoices
        }


class InvoiceRepository:
    @staticmethod
    def get_all(
        session: Session,
        search: str = "",
        status: str = "all",
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        limit: Optional[int] = None
    ) -> List[Invoice]:
        query = session.query(Invoice).options(joinedload(Invoice.items), joinedload(Invoice.customer))
        
        if search:
            s = f"%{search.strip()}%"
            query = query.filter(or_(
                Invoice.invoice_number.ilike(s),
                Invoice.manual_no.ilike(s),
                Invoice.delivered_to.ilike(s),
                Invoice.address.ilike(s),
                Invoice.dc_number_1.ilike(s),
                Invoice.dc_number_2.ilike(s)
            ))
        
        if status and status.lower() != "all":
            query = query.filter(Invoice.status == status.lower())

        if start_date:
            query = query.filter(Invoice.invoice_date >= start_date)
        if end_date:
            query = query.filter(Invoice.invoice_date <= end_date)

        query = query.order_by(desc(Invoice.invoice_date), desc(Invoice.id))
        if limit:
            query = query.limit(limit)
        return query.all()

    @staticmethod
    def get_by_id(session: Session, invoice_id: int) -> Optional[Invoice]:
        return session.query(Invoice).options(
            joinedload(Invoice.items),
            joinedload(Invoice.customer)
        ).filter(Invoice.id == invoice_id).first()

    @staticmethod
    def get_by_number(session: Session, invoice_number: str) -> Optional[Invoice]:
        return session.query(Invoice).options(
            joinedload(Invoice.items),
            joinedload(Invoice.customer)
        ).filter(Invoice.invoice_number == invoice_number).first()

    @staticmethod
    def create(session: Session, invoice_data: Dict[str, Any], items_data: List[Dict[str, Any]]) -> Invoice:
        invoice = Invoice(**invoice_data)
        session.add(invoice)
        session.flush()

        for idx, item_data in enumerate(items_data, 1):
            clean_item = dict(item_data)
            clean_item["serial_no"] = clean_item.get("serial_no", idx)
            item = InvoiceItem(invoice_id=invoice.id, **clean_item)
            session.add(item)

        session.commit()
        session.refresh(invoice)
        return invoice

    @staticmethod
    def update(session: Session, invoice_id: int, invoice_data: Dict[str, Any], items_data: List[Dict[str, Any]]) -> Optional[Invoice]:
        invoice = session.query(Invoice).filter(Invoice.id == invoice_id).first()
        if not invoice:
            return None

        for key, value in invoice_data.items():
            if hasattr(invoice, key):
                setattr(invoice, key, value)

        session.query(InvoiceItem).filter(InvoiceItem.invoice_id == invoice_id).delete()
        session.flush()

        for idx, item_data in enumerate(items_data, 1):
            clean_item = dict(item_data)
            clean_item.pop("id", None)
            clean_item.pop("invoice_id", None)
            clean_item["serial_no"] = clean_item.get("serial_no", idx)
            item = InvoiceItem(invoice_id=invoice.id, **clean_item)
            session.add(item)

        session.commit()
        session.refresh(invoice)
        return invoice

    @staticmethod
    def delete(session: Session, invoice_id: int) -> bool:
        invoice = session.query(Invoice).filter(Invoice.id == invoice_id).first()
        if invoice:
            session.delete(invoice)
            session.commit()
            return True
        return False

    @staticmethod
    def get_dashboard_metrics(session: Session) -> Dict[str, Any]:
        invoices = session.query(Invoice).all()
        total_invoices = len(invoices)
        paid_invoices = len([i for i in invoices if i.status == "paid"])
        pending_invoices = len([i for i in invoices if i.status in ("pending", "sent", "overdue")])
        draft_invoices = len([i for i in invoices if i.status == "draft"])

        total_revenue = sum((i.invoice_amount or Decimal("0.00")) for i in invoices if i.status != "cancelled")
        
        today = date.today()
        this_month_invoices = [
            i for i in invoices 
            if i.invoice_date and i.invoice_date.year == today.year and i.invoice_date.month == today.month and i.status != "cancelled"
        ]
        this_month_revenue = sum((i.invoice_amount or Decimal("0.00")) for i in this_month_invoices)

        return {
            "total_invoices": total_invoices,
            "paid_invoices": paid_invoices,
            "pending_invoices": pending_invoices,
            "draft_invoices": draft_invoices,
            "total_revenue": total_revenue,
            "this_month_revenue": this_month_revenue,
            "recent_invoices": InvoiceRepository.get_all(session, limit=8)
        }
