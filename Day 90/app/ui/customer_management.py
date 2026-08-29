"""
Customer Management Screen for InvoicePro
Customer directory, spending statistics, invoice history, and customer profile editor.
"""
from typing import Optional
from decimal import Decimal

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QSplitter,
    QFrame, QMessageBox, QScrollArea, QMenu
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QAction

from app.database.db import SessionLocal
from app.database.repositories import CustomerRepository, InvoiceRepository
from app.utils.formatters import format_currency, format_date
from app.ui.components.cards import CardPanel, MetricCard
from app.ui.dialogs.customer_dialog import CustomerDialog
from app.ui.components.toast import ToastNotification
from app.config import COLOR_NAVY_PRIMARY, COLOR_SUCCESS, COLOR_WARNING


class CustomerManagementWidget(QWidget):
    navigate_requested = Signal(str, object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_customer_id: Optional[int] = None
        self.setup_ui()
        self.load_customers()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(28, 24, 28, 24)
        main_layout.setSpacing(16)

        # ── Page Header ──────────────────────────────────────────────────────
        title_row = QHBoxLayout()
        title_col = QVBoxLayout()
        title_col.setSpacing(4)

        lbl_title = QLabel("Customers")
        lbl_title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        lbl_title.setStyleSheet("color: #0A2540;")
        title_col.addWidget(lbl_title)

        lbl_sub = QLabel("Manage your customer directory and billing history")
        lbl_sub.setFont(QFont("Segoe UI", 11))
        lbl_sub.setStyleSheet("color: #64748B;")
        title_col.addWidget(lbl_sub)

        title_row.addLayout(title_col)
        title_row.addStretch()

        btn_add = QPushButton("＋  Add Customer")
        btn_add.setFont(QFont("Segoe UI", 11, QFont.Bold))
        btn_add.setFixedHeight(40)
        btn_add.setMinimumWidth(150)
        btn_add.setCursor(Qt.PointingHandCursor)
        btn_add.setStyleSheet("""
            QPushButton {
                background-color: #0A2540;
                color: #FFFFFF;
                font-weight: 600;
                border: none;
                border-radius: 6px;
                padding: 8px 20px;
            }
            QPushButton:hover  { background-color: #1E3A8A; }
            QPushButton:pressed { background-color: #002D62; }
        """)
        btn_add.clicked.connect(self.open_add_customer)
        title_row.addWidget(btn_add)

        main_layout.addLayout(title_row)

        splitter = QSplitter(Qt.Horizontal)

        # ----------------------------------------------------
        # LEFT PANE: Customer Directory
        # ----------------------------------------------------
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(10)

        self.edit_search = QLineEdit()
        self.edit_search.setPlaceholderText("🔍 Search customers by name, company, city, or phone...")
        self.edit_search.textChanged.connect(self.load_customers)
        left_layout.addWidget(self.edit_search)

        self.table_customers = QTableWidget()
        self.headers = ["Name", "Company", "City", "Phone", "Actions"]
        self.table_customers.setColumnCount(len(self.headers))
        self.table_customers.setHorizontalHeaderLabels(self.headers)
        self.table_customers.verticalHeader().setVisible(False)
        self.table_customers.setAlternatingRowColors(True)
        self.table_customers.setSelectionBehavior(QTableWidget.SelectRows)
        self.table_customers.itemSelectionChanged.connect(self.on_customer_selected)

        header = self.table_customers.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Interactive)
        header.setSectionResizeMode(2, QHeaderView.Interactive)
        header.setSectionResizeMode(3, QHeaderView.Interactive)
        header.setSectionResizeMode(4, QHeaderView.Fixed)
        self.table_customers.setColumnWidth(4, 110)

        left_layout.addWidget(self.table_customers)
        splitter.addWidget(left_widget)

        # ----------------------------------------------------
        # RIGHT PANE: Customer Profile & Analytics
        # ----------------------------------------------------
        right_scroll = QScrollArea()
        right_scroll.setWidgetResizable(True)
        right_scroll.setStyleSheet("background-color: transparent; border: none;")

        self.profile_container = QWidget()
        self.profile_layout = QVBoxLayout(self.profile_container)
        self.profile_layout.setContentsMargins(10, 0, 0, 0)
        self.profile_layout.setSpacing(14)

        # Placeholder when no customer selected
        self.lbl_empty = QLabel("Select a customer from the left list to view details and billing history.")
        self.lbl_empty.setFont(QFont("Segoe UI", 11))
        self.lbl_empty.setStyleSheet("color: #94A3B8; padding: 40px;")
        self.lbl_empty.setAlignment(Qt.AlignCenter)
        self.profile_layout.addWidget(self.lbl_empty)

        # Actual profile detail container
        self.detail_widget = QWidget()
        detail_layout = QVBoxLayout(self.detail_widget)
        detail_layout.setContentsMargins(0, 0, 0, 0)
        detail_layout.setSpacing(14)

        # Customer Info Card
        self.card_info = CardPanel("Customer Profile")
        self.grid_info = QGridLayout()
        self.grid_info.setSpacing(8)

        self.lbl_name_val = QLabel("-")
        self.lbl_name_val.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.grid_info.addWidget(QLabel("Name:"), 0, 0)
        self.grid_info.addWidget(self.lbl_name_val, 0, 1)

        self.lbl_company_val = QLabel("-")
        self.grid_info.addWidget(QLabel("Company:"), 1, 0)
        self.grid_info.addWidget(self.lbl_company_val, 1, 1)

        self.lbl_address_val = QLabel("-")
        self.grid_info.addWidget(QLabel("Address:"), 2, 0)
        self.grid_info.addWidget(self.lbl_address_val, 2, 1)

        self.lbl_phone_val = QLabel("-")
        self.grid_info.addWidget(QLabel("Phone:"), 3, 0)
        self.grid_info.addWidget(self.lbl_phone_val, 3, 1)

        self.lbl_email_val = QLabel("-")
        self.grid_info.addWidget(QLabel("Email:"), 4, 0)
        self.grid_info.addWidget(self.lbl_email_val, 4, 1)

        self.card_info.layout.addLayout(self.grid_info)
        detail_layout.addWidget(self.card_info)

        # Customer Financial Stats
        stats_row = QHBoxLayout()
        self.card_cust_spent = MetricCard("Total Spent", "Rs. 0", "💳", "Lifetime invoiced", COLOR_NAVY_PRIMARY)
        self.card_cust_due = MetricCard("Outstanding Due", "Rs. 0", "⏳", "Pending balance", COLOR_WARNING)
        stats_row.addWidget(self.card_cust_spent)
        stats_row.addWidget(self.card_cust_due)
        detail_layout.addLayout(stats_row)

        # Action buttons
        btn_row = QHBoxLayout()

        self.btn_create_inv = QPushButton("➕  Create Invoice")
        self.btn_create_inv.setFixedHeight(36)
        self.btn_create_inv.setCursor(Qt.PointingHandCursor)
        self.btn_create_inv.setStyleSheet("""
            QPushButton {
                background-color: #0A2540;
                color: #FFFFFF;
                font-size: 12px;
                font-weight: 600;
                border: none;
                border-radius: 6px;
                padding: 6px 16px;
            }
            QPushButton:hover  { background-color: #1E3A8A; }
            QPushButton:pressed { background-color: #002D62; }
        """)
        self.btn_create_inv.clicked.connect(self.create_invoice_for_customer)
        btn_row.addWidget(self.btn_create_inv)

        btn_edit_cust = QPushButton("✏  Edit Details")
        btn_edit_cust.setFixedHeight(36)
        btn_edit_cust.setCursor(Qt.PointingHandCursor)
        btn_edit_cust.setStyleSheet("""
            QPushButton {
                background-color: #FFFFFF;
                color: #334155;
                font-size: 12px;
                font-weight: 500;
                border: 1px solid #CBD5E1;
                border-radius: 6px;
                padding: 6px 16px;
            }
            QPushButton:hover  { background-color: #F1F5F9; border-color: #94A3B8; }
            QPushButton:pressed { background-color: #E2E8F0; }
        """)
        btn_edit_cust.clicked.connect(self.open_edit_customer)
        btn_row.addWidget(btn_edit_cust)

        detail_layout.addLayout(btn_row)

        # Invoices for this customer
        self.card_cust_invoices = CardPanel("Customer Invoices")
        self.table_cust_inv = QTableWidget()
        self.table_cust_inv.setColumnCount(4)
        self.table_cust_inv.setHorizontalHeaderLabels(["Invoice #", "Date", "Amount", "Status"])
        self.table_cust_inv.verticalHeader().setVisible(False)
        self.table_cust_inv.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table_cust_inv.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table_cust_inv.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table_cust_inv.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.card_cust_invoices.layout.addWidget(self.table_cust_inv)
        detail_layout.addWidget(self.card_cust_invoices)

        self.profile_layout.addWidget(self.detail_widget)
        self.detail_widget.setVisible(False)

        right_scroll.setWidget(self.profile_container)
        splitter.addWidget(right_scroll)

        splitter.setStretchFactor(0, 5)
        splitter.setStretchFactor(1, 5)

        main_layout.addWidget(splitter)

    def load_customers(self):
        search_query = self.edit_search.text().strip()
        session = SessionLocal()
        try:
            customers = CustomerRepository.get_all(session, search=search_query)
            self.table_customers.setRowCount(len(customers))

            for r, cust in enumerate(customers):
                # Name
                item_name = QTableWidgetItem(cust.name or "")
                item_name.setFont(QFont("Segoe UI", 9, QFont.Bold))
                item_name.setData(Qt.UserRole, cust.id)
                self.table_customers.setItem(r, 0, item_name)

                # Company
                self.table_customers.setItem(r, 1, QTableWidgetItem(cust.company_name or ""))

                # City
                self.table_customers.setItem(r, 2, QTableWidgetItem(cust.city or ""))

                # Phone
                self.table_customers.setItem(r, 3, QTableWidgetItem(cust.phone or ""))

                # Single dropdown action button
                act_btn = QPushButton("Actions ▾")
                act_btn.setFixedHeight(28)
                act_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #0A2540;
                        color: #FFFFFF;
                        font-size: 12px;
                        font-weight: 600;
                        border: none;
                        border-radius: 5px;
                        padding: 4px 10px;
                        min-width: 90px;
                    }
                    QPushButton:hover   { background-color: #1E3A8A; }
                    QPushButton:pressed { background-color: #002D62; }
                """)
                act_btn.setCursor(Qt.PointingHandCursor)
                cust_id_captured = cust.id
                act_btn.clicked.connect(
                    lambda checked=False, cid=cust_id_captured, b=act_btn:
                    self._show_customer_menu(cid, b)
                )
                self.table_customers.setCellWidget(r, 4, act_btn)

            # Auto select first customer if available
            if customers and not self.selected_customer_id:
                self.table_customers.selectRow(0)

        finally:
            session.close()

    def _show_customer_menu(self, customer_id: int, button: QPushButton):
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu { background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 6px; padding: 4px 0; }
            QMenu::item { padding: 8px 20px; font-size: 13px; color: #0F172A; }
            QMenu::item:selected { background: #F1F5F9; color: #0A2540; }
            QMenu::separator { height: 1px; background: #E2E8F0; margin: 3px 0; }
        """)

        act_view = QAction("👁  View Profile", self)
        act_view.triggered.connect(lambda: self.load_customer_profile(customer_id))
        menu.addAction(act_view)

        act_inv = QAction("➕  New Invoice", self)
        act_inv.triggered.connect(lambda: self.navigate_requested.emit("new_invoice_for_customer", customer_id))
        menu.addAction(act_inv)

        act_edit = QAction("✏  Edit Details", self)
        act_edit.triggered.connect(lambda: self.edit_customer_by_id(customer_id))
        menu.addAction(act_edit)

        menu.addSeparator()

        act_del = QAction("🗑  Delete Customer", self)
        act_del.triggered.connect(lambda: self.delete_customer_by_id(customer_id))
        menu.addAction(act_del)

        menu.exec(button.mapToGlobal(button.rect().bottomLeft()))

    def on_customer_selected(self):
        selected_rows = self.table_customers.selectionModel().selectedRows()
        if not selected_rows:
            self.selected_customer_id = None
            self.lbl_empty.setVisible(True)
            self.detail_widget.setVisible(False)
            return

        row = selected_rows[0].row()
        cust_id = self.table_customers.item(row, 0).data(Qt.UserRole)
        self.load_customer_profile(cust_id)

    def load_customer_profile(self, customer_id: int):
        self.selected_customer_id = customer_id
        session = SessionLocal()
        try:
            cust = CustomerRepository.get_by_id(session, customer_id)
            if not cust:
                return

            self.lbl_empty.setVisible(False)
            self.detail_widget.setVisible(True)

            self.lbl_name_val.setText(cust.name or "")
            self.lbl_company_val.setText(cust.company_name or "-")
            self.lbl_address_val.setText(cust.address or cust.city or "-")
            self.lbl_phone_val.setText(cust.phone or "-")
            self.lbl_email_val.setText(cust.email or "-")

            stats = CustomerRepository.get_customer_stats(session, customer_id)
            self.card_cust_spent.update_value(format_currency(stats["total_spent"], symbol="Rs."))
            self.card_cust_due.update_value(format_currency(stats["total_due"], symbol="Rs."))

            invoices = stats["invoices"]
            self.table_cust_inv.setRowCount(len(invoices))
            for r, inv in enumerate(invoices):
                self.table_cust_inv.setItem(r, 0, QTableWidgetItem(inv.invoice_number or ""))
                self.table_cust_inv.setItem(r, 1, QTableWidgetItem(format_date(inv.invoice_date)))
                self.table_cust_inv.setItem(r, 2, QTableWidgetItem(format_currency(inv.invoice_amount, symbol="Rs.")))
                self.table_cust_inv.setItem(r, 3, QTableWidgetItem((inv.status or "paid").upper()))

        finally:
            session.close()

    def open_add_customer(self):
        dlg = CustomerDialog(self)
        if dlg.exec():
            self.load_customers()
            ToastNotification.show_toast(self.window(), "Customer added successfully.", "success")

    def edit_customer_by_id(self, customer_id: int):
        dlg = CustomerDialog(self, customer_id=customer_id)
        if dlg.exec():
            self.load_customers()
            if self.selected_customer_id == customer_id:
                self.load_customer_profile(customer_id)
            ToastNotification.show_toast(self.window(), "Customer updated.", "success")

    def open_edit_customer(self):
        if self.selected_customer_id:
            self.edit_customer_by_id(self.selected_customer_id)

    def delete_customer_by_id(self, customer_id: int):
        reply = QMessageBox.question(
            self,
            "Confirm Customer Deletion",
            "Are you sure you want to delete this customer?\nAll associated invoices will also be deleted.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            session = SessionLocal()
            try:
                CustomerRepository.delete(session, customer_id)
                self.selected_customer_id = None
                self.load_customers()
                ToastNotification.show_toast(self.window(), "Customer deleted.", "info")
            finally:
                session.close()

    def create_invoice_for_customer(self):
        if self.selected_customer_id:
            self.navigate_requested.emit("new_invoice_for_customer", self.selected_customer_id)
