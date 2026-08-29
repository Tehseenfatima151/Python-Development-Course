"""
Customer Create / Edit Dialog for InvoicePro
"""
from typing import Optional, Dict, Any
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit,
    QTextEdit, QPushButton, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from app.database.db import SessionLocal
from app.database.repositories import CustomerRepository


class CustomerDialog(QDialog):
    def __init__(self, parent=None, customer_id: Optional[int] = None):
        super().__init__(parent)
        self.customer_id = customer_id
        self.saved_customer_id: Optional[int] = None
        self.setWindowTitle("Edit Customer" if customer_id else "Add New Customer")
        self.setFixedWidth(460)

        self.setup_ui()
        if customer_id:
            self.load_customer_data()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        lbl_title = QLabel("Customer Information")
        lbl_title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        layout.addWidget(lbl_title)

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(QLabel("Full Name * :"), 0, 0)
        self.edit_name = QLineEdit()
        self.edit_name.setPlaceholderText("e.g. Ijaz Ahmad")
        grid.addWidget(self.edit_name, 0, 1)

        grid.addWidget(QLabel("Company Name:"), 1, 0)
        self.edit_company = QLineEdit()
        self.edit_company.setPlaceholderText("e.g. Ijaz Ahmad Poultry")
        grid.addWidget(self.edit_company, 1, 1)

        grid.addWidget(QLabel("City:"), 2, 0)
        self.edit_city = QLineEdit()
        self.edit_city.setPlaceholderText("e.g. Mian Chanu")
        grid.addWidget(self.edit_city, 2, 1)

        grid.addWidget(QLabel("Address:"), 3, 0)
        self.edit_address = QLineEdit()
        self.edit_address.setPlaceholderText("e.g. Mian Chanu, Punjab")
        grid.addWidget(self.edit_address, 3, 1)

        grid.addWidget(QLabel("Phone:"), 4, 0)
        self.edit_phone = QLineEdit()
        self.edit_phone.setPlaceholderText("e.g. +92 300 1234567")
        grid.addWidget(self.edit_phone, 4, 1)

        grid.addWidget(QLabel("Email:"), 5, 0)
        self.edit_email = QLineEdit()
        self.edit_email.setPlaceholderText("e.g. customer@example.com")
        grid.addWidget(self.edit_email, 5, 1)

        grid.addWidget(QLabel("Tax ID / NTN:"), 6, 0)
        self.edit_tax_id = QLineEdit()
        grid.addWidget(self.edit_tax_id, 6, 1)

        grid.addWidget(QLabel("Notes:"), 7, 0)
        self.edit_notes = QTextEdit()
        self.edit_notes.setMaximumHeight(60)
        grid.addWidget(self.edit_notes, 7, 1)

        layout.addLayout(grid)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        btn_cancel = QPushButton("Cancel")
        btn_cancel.setFixedHeight(36)
        btn_cancel.setMinimumWidth(90)
        btn_cancel.setCursor(Qt.PointingHandCursor)
        btn_cancel.setStyleSheet("""
            QPushButton {
                background-color: #FFFFFF;
                color: #334155;
                font-size: 13px;
                font-weight: 500;
                border: 1px solid #CBD5E1;
                border-radius: 6px;
                padding: 6px 18px;
            }
            QPushButton:hover  { background-color: #F1F5F9; border-color: #94A3B8; }
            QPushButton:pressed { background-color: #E2E8F0; }
        """)
        btn_cancel.clicked.connect(self.reject)
        btn_layout.addWidget(btn_cancel)

        btn_save = QPushButton("💾  Save Customer")
        btn_save.setFixedHeight(36)
        btn_save.setMinimumWidth(130)
        btn_save.setCursor(Qt.PointingHandCursor)
        btn_save.setFont(QFont("Segoe UI", 11, QFont.Bold))
        btn_save.setStyleSheet("""
            QPushButton {
                background-color: #0A2540;
                color: #FFFFFF;
                font-size: 13px;
                font-weight: 600;
                border: none;
                border-radius: 6px;
                padding: 6px 20px;
            }
            QPushButton:hover  { background-color: #1E3A8A; }
            QPushButton:pressed { background-color: #002D62; }
        """)
        btn_save.clicked.connect(self.save_customer)
        btn_layout.addWidget(btn_save)

        layout.addLayout(btn_layout)

    def load_customer_data(self):
        if not self.customer_id:
            return
        session = SessionLocal()
        try:
            cust = CustomerRepository.get_by_id(session, self.customer_id)
            if cust:
                self.edit_name.setText(cust.name or "")
                self.edit_company.setText(cust.company_name or "")
                self.edit_city.setText(cust.city or "")
                self.edit_address.setText(cust.address or "")
                self.edit_phone.setText(cust.phone or "")
                self.edit_email.setText(cust.email or "")
                self.edit_tax_id.setText(cust.tax_id or "")
                self.edit_notes.setPlainText(cust.notes or "")
        finally:
            session.close()

    def save_customer(self):
        name = self.edit_name.text().strip()
        if not name:
            QMessageBox.warning(self, "Validation Error", "Customer name is required.")
            return

        data = {
            "name": name,
            "company_name": self.edit_company.text().strip(),
            "city": self.edit_city.text().strip(),
            "address": self.edit_address.text().strip(),
            "phone": self.edit_phone.text().strip(),
            "email": self.edit_email.text().strip(),
            "tax_id": self.edit_tax_id.text().strip(),
            "notes": self.edit_notes.toPlainText().strip()
        }

        session = SessionLocal()
        try:
            if self.customer_id:
                cust = CustomerRepository.update(session, self.customer_id, data)
                self.saved_customer_id = cust.id if cust else None
            else:
                cust = CustomerRepository.create(session, data)
                self.saved_customer_id = cust.id if cust else None
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save customer: {e}")
        finally:
            session.close()
