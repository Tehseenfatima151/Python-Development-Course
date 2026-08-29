"""
Invoice History & Management Screen for InvoicePro
Full-featured invoice grid with live search, status filters, and actions.
"""
from typing import Optional
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox,
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox,
    QMenu, QFrame
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QAction

from app.database.db import SessionLocal
from app.database.repositories import InvoiceRepository, CompanyRepository
from app.services.invoice_service import InvoiceService
from app.services.pdf_service import PDFService
from app.utils.formatters import format_currency, format_date
from app.utils.helpers import open_file_in_system_viewer, print_file_with_system_dialog
from app.ui.components.badges import StatusBadge
from app.ui.components.toast import ToastNotification


# Shared style for the dropdown action button — compact
_ACTION_BTN_STYLE = """
QPushButton {
    background-color: #0A2540;
    color: #FFFFFF;
    font-size: 11px;
    font-weight: 600;
    border: none;
    border-radius: 5px;
    padding: 3px 8px;
    min-width: 72px;
    max-width: 80px;
}
QPushButton:hover  { background-color: #1E3A8A; }
QPushButton:pressed { background-color: #002D62; }
"""


def _make_action_btn(label: str = "Actions ▾") -> QPushButton:
    btn = QPushButton(label)
    btn.setFixedHeight(28)
    btn.setStyleSheet(_ACTION_BTN_STYLE)
    btn.setCursor(Qt.PointingHandCursor)
    return btn


class InvoiceHistoryWidget(QWidget):
    navigate_requested = Signal(str, object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.load_invoices()

    # ── UI setup ──────────────────────────────────────────────────────────────
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(16)

        # Page Header
        header_row = QHBoxLayout()
        title_col = QVBoxLayout()
        title_col.setSpacing(4)

        lbl_title = QLabel("Invoices")
        lbl_title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        lbl_title.setStyleSheet("color: #0A2540;")
        title_col.addWidget(lbl_title)

        lbl_sub = QLabel("Search, filter, and manage all your invoices")
        lbl_sub.setFont(QFont("Segoe UI", 11))
        lbl_sub.setStyleSheet("color: #64748B;")
        title_col.addWidget(lbl_sub)

        header_row.addLayout(title_col)
        header_row.addStretch()

        btn_create = QPushButton("＋  New Invoice")
        btn_create.setFont(QFont("Segoe UI", 11, QFont.Bold))
        btn_create.setFixedHeight(40)
        btn_create.setMinimumWidth(150)
        btn_create.setCursor(Qt.PointingHandCursor)
        btn_create.setStyleSheet("""
            QPushButton { background-color:#0A2540; color:#FFFFFF; font-weight:600;
                border:none; border-radius:6px; padding:8px 20px; }
            QPushButton:hover   { background-color:#1E3A8A; }
            QPushButton:pressed { background-color:#002D62; }
        """)
        btn_create.clicked.connect(lambda: self.navigate_requested.emit("new_invoice", None))
        header_row.addWidget(btn_create)

        layout.addLayout(header_row)

        # Filter bar
        filter_frame = QFrame()
        filter_frame.setStyleSheet(
            "QFrame { background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; }"
        )
        filter_lay = QHBoxLayout(filter_frame)
        filter_lay.setContentsMargins(14, 10, 14, 10)
        filter_lay.setSpacing(12)

        self.edit_search = QLineEdit()
        self.edit_search.setPlaceholderText("🔍  Search by invoice #, customer, DC #, address...")
        self.edit_search.textChanged.connect(self.load_invoices)
        self.edit_search.setFixedHeight(34)
        filter_lay.addWidget(self.edit_search, 3)

        lbl_status = QLabel("Status:")
        lbl_status.setFont(QFont("Segoe UI", 9, QFont.Bold))
        lbl_status.setStyleSheet("color: #475569;")
        filter_lay.addWidget(lbl_status)

        self.combo_status = QComboBox()
        self.combo_status.addItems(["All", "Paid", "Pending", "Sent", "Draft", "Overdue", "Cancelled"])
        self.combo_status.setFixedHeight(34)
        self.combo_status.setMinimumWidth(120)
        self.combo_status.currentTextChanged.connect(self.load_invoices)
        filter_lay.addWidget(self.combo_status)

        btn_refresh = QPushButton("🔄  Refresh")
        btn_refresh.setFixedHeight(34)
        btn_refresh.setCursor(Qt.PointingHandCursor)
        btn_refresh.setStyleSheet("""
            QPushButton { background-color:#FFFFFF; color:#334155; font-size:13px;
                font-weight:500; border:1px solid #CBD5E1; border-radius:6px; padding:6px 14px; }
            QPushButton:hover   { background-color:#F1F5F9; border-color:#94A3B8; color:#0A2540; }
            QPushButton:pressed { background-color:#E2E8F0; }
        """)
        btn_refresh.clicked.connect(self.load_invoices)
        filter_lay.addWidget(btn_refresh)

        layout.addWidget(filter_frame)

        # Invoices table
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "Invoice #", "Book No", "DC # 1", "DC # 2",
            "Customer / Delivered To", "Date", "Amount (Rs.)", "Status", "Actions"
        ])
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionMode(QTableWidget.NoSelection)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setShowGrid(False)
        self.table.setFocusPolicy(Qt.NoFocus)
        self.table.verticalHeader().setDefaultSectionSize(38)

        hdr = self.table.horizontalHeader()
        hdr.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        hdr.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        hdr.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        hdr.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        hdr.setSectionResizeMode(4, QHeaderView.Stretch)
        hdr.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        hdr.setSectionResizeMode(6, QHeaderView.ResizeToContents)
        hdr.setSectionResizeMode(7, QHeaderView.ResizeToContents)
        hdr.setSectionResizeMode(8, QHeaderView.Fixed)
        self.table.setColumnWidth(8, 88)

        layout.addWidget(self.table)

        self.lbl_count = QLabel("Showing 0 invoices")
        self.lbl_count.setFont(QFont("Segoe UI", 9))
        self.lbl_count.setStyleSheet("color: #64748B;")
        layout.addWidget(self.lbl_count)

    # ── Data loading ──────────────────────────────────────────────────────────
    def load_invoices(self):
        search_text   = self.edit_search.text().strip()
        status_filter = self.combo_status.currentText().lower()
        if status_filter == "all":
            status_filter = ""

        session = SessionLocal()
        try:
            invoices = InvoiceRepository.get_all(session, search=search_text, status=status_filter)
            self.table.setRowCount(len(invoices))
            self.lbl_count.setText(f"Showing {len(invoices)} invoice(s)")

            for r, inv in enumerate(invoices):
                it0 = QTableWidgetItem(inv.invoice_number or "")
                it0.setFont(QFont("Segoe UI", 9, QFont.Bold))
                self.table.setItem(r, 0, it0)

                self.table.setItem(r, 1, QTableWidgetItem(inv.manual_no or ""))
                self.table.setItem(r, 2, QTableWidgetItem(inv.dc_number_1 or ""))
                self.table.setItem(r, 3, QTableWidgetItem(inv.dc_number_2 or ""))
                self.table.setItem(r, 4, QTableWidgetItem(inv.delivered_to or ""))
                self.table.setItem(r, 5, QTableWidgetItem(format_date(inv.invoice_date)))

                it6 = QTableWidgetItem(format_currency(inv.invoice_amount, decimals=0))
                it6.setFont(QFont("Segoe UI", 9, QFont.Bold))
                it6.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.table.setItem(r, 6, it6)

                badge = StatusBadge(inv.status or "paid")
                self.table.setCellWidget(r, 7, badge)

                # Single dropdown action button — always fully visible
                btn = _make_action_btn("Actions ▾")
                inv_id   = inv.id
                pdf_path = inv.pdf_path
                btn.clicked.connect(
                    lambda checked=False, iid=inv_id, p=pdf_path, b=btn:
                    self._show_invoice_menu(iid, p, b)
                )
                self.table.setCellWidget(r, 8, btn)

        finally:
            session.close()

    def _show_invoice_menu(self, invoice_id: int, pdf_path: Optional[str], button: QPushButton):
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu { background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 6px; padding: 4px 0; }
            QMenu::item { padding: 8px 20px; font-size: 13px; color: #0F172A; }
            QMenu::item:selected { background: #F1F5F9; color: #0A2540; }
            QMenu::separator { height: 1px; background: #E2E8F0; margin: 3px 0; }
        """)

        act_edit = QAction("✏  Edit Invoice", self)
        act_edit.triggered.connect(lambda: self.navigate_requested.emit("edit_invoice", invoice_id))
        menu.addAction(act_edit)

        act_pdf = QAction("📄  Open / Generate PDF", self)
        act_pdf.triggered.connect(lambda: self.open_or_generate_pdf(invoice_id, pdf_path))
        menu.addAction(act_pdf)

        act_print = QAction("🖨  Print Invoice", self)
        act_print.triggered.connect(lambda: self.print_invoice(invoice_id))
        menu.addAction(act_print)

        act_dup = QAction("📋  Duplicate Invoice", self)
        act_dup.triggered.connect(lambda: self.duplicate_invoice(invoice_id))
        menu.addAction(act_dup)

        menu.addSeparator()

        act_del = QAction("🗑  Delete Invoice", self)
        act_del.triggered.connect(lambda: self.delete_invoice(invoice_id))
        menu.addAction(act_del)

        menu.exec(button.mapToGlobal(button.rect().bottomLeft()))

    # ── Actions ───────────────────────────────────────────────────────────────
    def open_or_generate_pdf(self, invoice_id: int, existing_path: Optional[str]):
        if existing_path and open_file_in_system_viewer(existing_path):
            return

        session = SessionLocal()
        try:
            inv = InvoiceRepository.get_by_id(session, invoice_id)
            if not inv:
                return

            inv_data = {
                "invoice_number":  inv.invoice_number,
                "manual_no":       inv.manual_no,
                "dc_number_1":     inv.dc_number_1,
                "dc_number_2":     inv.dc_number_2,
                "order_number":    inv.order_number,
                "invoice_date":    inv.invoice_date,
                "delivered_to":    inv.delivered_to,
                "invoiced_to":     inv.invoiced_to,
                "address":         inv.address,
                "dispatch_info":   inv.dispatch_info,
                "subtotal":        inv.subtotal,
                "discount_amount": inv.discount_amount,
                "invoice_amount":  inv.invoice_amount,
                "total_due":       inv.total_due,
                "amount_in_words": inv.amount_in_words,
            }
            items_data = [{
                "serial_no":        itm.serial_no,
                "product_name":     itm.product_name,
                "packing":          itm.packing,
                "quantity_value":   itm.quantity_value,
                "quantity_unit":    itm.quantity_unit,
                "billing_quantity": itm.billing_quantity,
                "bonus":            itm.bonus,
                "unit_rate":        itm.unit_rate,
                "amount":           itm.amount,
            } for itm in inv.items]

            company = CompanyRepository.get_company(session)
            comp_data = {
                "name":                   company.name if company else "",
                "address":                company.address if company else "",
                "email":                  company.email if company else "",
                "sales_coordinator_name": company.sales_coordinator_name if company else "Dennis",
            }

            pdf_path = PDFService.generate_invoice_pdf(inv_data, items_data, comp_data)
            inv.pdf_path = pdf_path
            session.commit()
            open_file_in_system_viewer(pdf_path)
            ToastNotification.show_toast(self.window(), "PDF opened successfully!", "success")
        finally:
            session.close()

    def duplicate_invoice(self, invoice_id: int):
        session = SessionLocal()
        try:
            success, new_inv, msg = InvoiceService.duplicate_invoice(session, invoice_id)
            if success and new_inv:
                ToastNotification.show_toast(
                    self.window(), f"Duplicated as #{new_inv.invoice_number}", "success"
                )
                self.load_invoices()
                self.navigate_requested.emit("edit_invoice", new_inv.id)
            else:
                QMessageBox.warning(self, "Error", msg)
        finally:
            session.close()

    def print_invoice(self, invoice_id: int):
        session = SessionLocal()
        try:
            inv = InvoiceRepository.get_by_id(session, invoice_id)
            if inv and inv.pdf_path:
                print_file_with_system_dialog(inv.pdf_path)
                ToastNotification.show_toast(self.window(), "Sending to printer...", "info")
            else:
                self.open_or_generate_pdf(invoice_id, None)
        finally:
            session.close()

    def delete_invoice(self, invoice_id: int):
        reply = QMessageBox.question(
            self, "Confirm Deletion",
            "Are you sure you want to permanently delete this invoice?\nThis action cannot be undone.",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            session = SessionLocal()
            try:
                InvoiceRepository.delete(session, invoice_id)
                ToastNotification.show_toast(self.window(), "Invoice deleted.", "info")
                self.load_invoices()
            finally:
                session.close()
