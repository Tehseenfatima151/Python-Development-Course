"""
Invoice Service for InvoicePro
Handles high-level business logic for invoices: creation, updating, draft saving,
status transitions, duplication, searching, and PDF generation linking.
"""
import os
import logging
from datetime import date
from decimal import Decimal
from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy.orm import Session

from app.database.models import Invoice, Company
from app.database.repositories import InvoiceRepository, CompanyRepository, CustomerRepository
from app.services.calculation_service import CalculationService, to_decimal
from app.services.pdf_service import PDFService
from app.utils.formatters import format_invoice_number

logger = logging.getLogger(__name__)


class InvoiceService:
    @staticmethod
    def create_invoice(
        session: Session,
        invoice_form_data: Dict[str, Any],
        items_form_data: List[Dict[str, Any]],
        generate_pdf: bool = True
    ) -> Tuple[bool, Optional[Invoice], str]:
        try:
            company = CompanyRepository.get_company(session)
            comp_data = {
                "name": company.name if company else "POULTRY SMART TRADERS",
                "address": company.address if company else "",
                "email": company.email if company else "",
                "phone": company.phone if company else "",
                "logo_path": company.logo_path if company else None,
                "stamp_path": company.stamp_path if company else None,
                "signature_path": company.signature_path if company else None,
                "sales_coordinator_name": company.sales_coordinator_name if company else "Dennis"
            }

            # Check invoice number or generate new one
            inv_number = invoice_form_data.get("invoice_number", "").strip()
            if not inv_number:
                inv_number = CompanyRepository.get_next_available_invoice_number(session)
                invoice_form_data["invoice_number"] = inv_number

            # Check if invoice number already exists
            existing = InvoiceRepository.get_by_number(session, inv_number)
            if existing:
                return False, None, f"Invoice number '{inv_number}' already exists."

            # Calculate line items
            calculated_items = []
            for idx, raw_item in enumerate(items_form_data, 1):
                prod_name = raw_item.get("product_name", "").strip()
                if not prod_name:
                    continue
                
                qty_val = to_decimal(raw_item.get("quantity_value", 1))
                billing_qty = to_decimal(raw_item.get("billing_quantity") or qty_val)
                unit_rate = to_decimal(raw_item.get("unit_rate", 0))
                disc_pct = to_decimal(raw_item.get("discount_percent", 0))
                tax_pct = to_decimal(raw_item.get("tax_percent", 0))

                amt = CalculationService.calculate_line_item(billing_qty, unit_rate, disc_pct, tax_pct)

                calculated_items.append({
                    "serial_no": raw_item.get("serial_no", idx),
                    "product_name": prod_name,
                    "packing": raw_item.get("packing", ""),
                    "quantity_value": qty_val,
                    "quantity_unit": raw_item.get("quantity_unit", ""),
                    "billing_quantity": billing_qty,
                    "bonus": raw_item.get("bonus", ""),
                    "unit_rate": unit_rate,
                    "discount_percent": disc_pct,
                    "tax_percent": tax_pct,
                    "amount": amt
                })

            # Calculate overall invoice totals
            disc_type = invoice_form_data.get("discount_type", "amount")
            disc_val = to_decimal(invoice_form_data.get("discount_value", 0))
            tax_rate = to_decimal(invoice_form_data.get("tax_rate", 0))
            shipping = to_decimal(invoice_form_data.get("shipping_charges", 0))
            other = to_decimal(invoice_form_data.get("other_charges", 0))
            paid = to_decimal(invoice_form_data.get("paid_amount", 0))

            totals = CalculationService.calculate_invoice_totals(
                calculated_items,
                discount_type=disc_type,
                discount_value=disc_val,
                tax_rate=tax_rate,
                shipping_charges=shipping,
                other_charges=other,
                paid_amount=paid,
                currency_name=company.default_currency if company else "Rupees"
            )

            # Merge computed totals into invoice data
            invoice_record_data = dict(invoice_form_data)
            invoice_record_data.update({
                "subtotal": totals["subtotal"],
                "discount_amount": totals["discount_amount"],
                "tax_amount": totals["tax_amount"],
                "total_amount": totals["total_amount"],
                "invoice_amount": totals["invoice_amount"],
                "total_due": totals["total_due"],
                "paid_amount": totals["paid_amount"],
                "balance_due": totals["balance_due"],
                "amount_in_words": totals["amount_in_words"],
            })

            # Create in Database
            invoice = InvoiceRepository.create(session, invoice_record_data, calculated_items)

            # Generate PDF
            if generate_pdf:
                pdf_path = PDFService.generate_invoice_pdf(
                    invoice_record_data,
                    calculated_items,
                    comp_data
                )
                invoice.pdf_path = pdf_path
                session.commit()

            return True, invoice, "Invoice created successfully."

        except Exception as e:
            session.rollback()
            logger.error(f"Error creating invoice: {e}")
            return False, None, f"Failed to create invoice: {str(e)}"

    @staticmethod
    def update_invoice(
        session: Session,
        invoice_id: int,
        invoice_form_data: Dict[str, Any],
        items_form_data: List[Dict[str, Any]],
        generate_pdf: bool = True
    ) -> Tuple[bool, Optional[Invoice], str]:
        try:
            company = CompanyRepository.get_company(session)
            comp_data = {
                "name": company.name if company else "POULTRY SMART TRADERS",
                "address": company.address if company else "",
                "email": company.email if company else "",
                "phone": company.phone if company else "",
                "logo_path": company.logo_path if company else None,
                "stamp_path": company.stamp_path if company else None,
                "signature_path": company.signature_path if company else None,
                "sales_coordinator_name": company.sales_coordinator_name if company else "Dennis"
            }

            calculated_items = []
            for idx, raw_item in enumerate(items_form_data, 1):
                prod_name = raw_item.get("product_name", "").strip()
                if not prod_name:
                    continue
                
                qty_val = to_decimal(raw_item.get("quantity_value", 1))
                billing_qty = to_decimal(raw_item.get("billing_quantity") or qty_val)
                unit_rate = to_decimal(raw_item.get("unit_rate", 0))
                disc_pct = to_decimal(raw_item.get("discount_percent", 0))
                tax_pct = to_decimal(raw_item.get("tax_percent", 0))

                amt = CalculationService.calculate_line_item(billing_qty, unit_rate, disc_pct, tax_pct)

                calculated_items.append({
                    "serial_no": raw_item.get("serial_no", idx),
                    "product_name": prod_name,
                    "packing": raw_item.get("packing", ""),
                    "quantity_value": qty_val,
                    "quantity_unit": raw_item.get("quantity_unit", ""),
                    "billing_quantity": billing_qty,
                    "bonus": raw_item.get("bonus", ""),
                    "unit_rate": unit_rate,
                    "discount_percent": disc_pct,
                    "tax_percent": tax_pct,
                    "amount": amt
                })

            disc_type = invoice_form_data.get("discount_type", "amount")
            disc_val = to_decimal(invoice_form_data.get("discount_value", 0))
            tax_rate = to_decimal(invoice_form_data.get("tax_rate", 0))
            shipping = to_decimal(invoice_form_data.get("shipping_charges", 0))
            other = to_decimal(invoice_form_data.get("other_charges", 0))
            paid = to_decimal(invoice_form_data.get("paid_amount", 0))

            totals = CalculationService.calculate_invoice_totals(
                calculated_items,
                discount_type=disc_type,
                discount_value=disc_val,
                tax_rate=tax_rate,
                shipping_charges=shipping,
                other_charges=other,
                paid_amount=paid,
                currency_name=company.default_currency if company else "Rupees"
            )

            invoice_record_data = dict(invoice_form_data)
            invoice_record_data.update({
                "subtotal": totals["subtotal"],
                "discount_amount": totals["discount_amount"],
                "tax_amount": totals["tax_amount"],
                "total_amount": totals["total_amount"],
                "invoice_amount": totals["invoice_amount"],
                "total_due": totals["total_due"],
                "paid_amount": totals["paid_amount"],
                "balance_due": totals["balance_due"],
                "amount_in_words": totals["amount_in_words"],
            })

            invoice = InvoiceRepository.update(session, invoice_id, invoice_record_data, calculated_items)

            if generate_pdf and invoice:
                pdf_path = PDFService.generate_invoice_pdf(
                    invoice_record_data,
                    calculated_items,
                    comp_data
                )
                invoice.pdf_path = pdf_path
                session.commit()

            return True, invoice, "Invoice updated successfully."

        except Exception as e:
            session.rollback()
            logger.error(f"Error updating invoice: {e}")
            return False, None, f"Failed to update invoice: {str(e)}"

    @staticmethod
    def duplicate_invoice(session: Session, invoice_id: int, generate_pdf: bool = True) -> Tuple[bool, Optional[Invoice], str]:
        try:
            original = InvoiceRepository.get_by_id(session, invoice_id)
            if not original:
                return False, None, "Original invoice not found."

            new_inv_num = CompanyRepository.get_next_available_invoice_number(session)

            inv_data = {
                "invoice_number": new_inv_num,
                "manual_no": f"{original.manual_no}-COPY" if original.manual_no else "",
                "dc_number_1": original.dc_number_1,
                "dc_number_2": original.dc_number_2,
                "order_number": original.order_number,
                "invoice_date": date.today(),
                "due_date": original.due_date,
                "delivered_to": original.delivered_to,
                "invoiced_to": original.invoiced_to,
                "address": original.address,
                "dispatch_info": original.dispatch_info,
                "customer_id": original.customer_id,
                "status": "draft",
                "discount_type": original.discount_type,
                "discount_value": original.discount_value,
                "tax_rate": original.tax_rate,
                "shipping_charges": original.shipping_charges,
                "other_charges": original.other_charges,
                "notes": original.notes,
                "payment_terms": original.payment_terms,
            }

            items_data = []
            for item in original.items:
                items_data.append({
                    "serial_no": item.serial_no,
                    "product_name": item.product_name,
                    "packing": item.packing,
                    "quantity_value": item.quantity_value,
                    "quantity_unit": item.quantity_unit,
                    "billing_quantity": item.billing_quantity,
                    "bonus": item.bonus,
                    "unit_rate": item.unit_rate,
                    "discount_percent": item.discount_percent,
                    "tax_percent": item.tax_percent,
                })

            return InvoiceService.create_invoice(session, inv_data, items_data, generate_pdf=generate_pdf)

        except Exception as e:
            session.rollback()
            return False, None, f"Failed to duplicate invoice: {str(e)}"
