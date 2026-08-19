"""
First Launch Onboarding Wizard for InvoicePro
Guides user through initial company profile and billing defaults setup.
"""
from decimal import Decimal
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFormLayout, QFrame, QMessageBox, QComboBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from app.config import APP_NAME, APP_SUBTITLE, DEFAULT_CURRENCY
from app.database.db import SessionLocal
from app.database.repositories import CompanyRepository


class FirstLaunchWizard(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Welcome to {APP_NAME} — Initial Setup")
        self.resize(560, 480)
        self.setModal(True)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(18)

        # Header Banner
        header = QFrame()
        header.setStyleSheet("background-color: #0A2540; border-radius: 8px; padding: 12px;")
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(12, 12, 12, 12)

        lbl_title = QLabel(f"Welcome to {APP_NAME}")
        lbl_title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        lbl_title.setStyleSheet("color: white;")
        header_layout.addWidget(lbl_title)

        lbl_desc = QLabel("Let's configure your business profile and invoice settings.")
        lbl_desc.setFont(QFont("Segoe UI", 10))
        lbl_desc.setStyleSheet("color: #E2E8F0;")
        header_layout.addWidget(lbl_desc)

        layout.addWidget(header)

        # Form Layout
        form_frame = QFrame()
        form_layout = QFormLayout(form_frame)
        form_layout.setContentsMargins(8, 8, 8, 8)
        form_layout.setSpacing(12)

        self.txt_name = QLineEdit("POULTRY SMART TRADERS")
        form_layout.addRow("Company Name *:", self.txt_name)

        self.txt_address = QLineEdit("23-A Gulshan Iqbal Alla Din Park, Karachi (Pak.)")
        form_layout.addRow("Address:", self.txt_address)

        self.txt_email = QLineEdit("poultrysmarttraders01@gmail.com")
        form_layout.addRow("Email:", self.txt_email)

        self.txt_phone = QLineEdit("")
        form_layout.addRow("Phone / Mobile:", self.txt_phone)

        self.combo_currency = QComboBox()
        self.combo_currency.addItems(["Rs. (PKR)", "$ (USD)", "€ (EUR)", "£ (GBP)", "AED", "SAR"])
        form_layout.addRow("Default Currency:", self.combo_currency)

        self.txt_coordinator = QLineEdit("Dennis")
        form_layout.addRow("Sales Coordinator:", self.txt_coordinator)

        layout.addWidget(form_frame)
        layout.addStretch()

        # Action Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        btn_start = QPushButton("🚀 Get Started with InvoicePro")
        btn_start.setFont(QFont("Segoe UI", 11, QFont.Bold))
        btn_start.setFixedHeight(40)
        btn_start.setStyleSheet("""
            QPushButton {
                background-color: #0A2540;
                color: white;
                border-radius: 6px;
                padding: 8px 24px;
            }
            QPushButton:hover {
                background-color: #1E3A8A;
            }
        """)
        btn_start.clicked.connect(self.save_and_continue)
        btn_layout.addWidget(btn_start)

        layout.addLayout(btn_layout)

    def save_and_continue(self):
        name = self.txt_name.text().strip()
        if not name:
            QMessageBox.warning(self, "Validation Error", "Company name is required.")
            return

        curr_text = self.combo_currency.currentText().split()[0]

        session = SessionLocal()
        try:
            CompanyRepository.update_company(session, {
                "name": name,
                "address": self.txt_address.text().strip(),
                "email": self.txt_email.text().strip(),
                "phone": self.txt_phone.text().strip(),
                "default_currency": curr_text,
                "sales_coordinator_name": self.txt_coordinator.text().strip() or "Dennis"
            })
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save profile: {e}")
        finally:
            session.close()
