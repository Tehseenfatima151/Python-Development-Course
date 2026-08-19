"""
Setup Wizard and About Dialog for InvoicePro
"""
from PySide6.QtWidgets import (
    QWizard, QWizardPage, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel,
    QLineEdit, QDoubleSpinBox, QSpinBox, QDialog, QPushButton, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap

from app.config import APP_NAME, APP_VERSION, APP_SUBTITLE, COLOR_NAVY_PRIMARY
from app.database.db import SessionLocal
from app.database.repositories import CompanyRepository
from app.services.company_service import CompanyService


class FirstLaunchWizard(QWizard):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Welcome to {APP_NAME} — Setup Wizard")
        self.setWizardStyle(QWizard.ModernStyle)
        self.setFixedSize(560, 420)

        self.addPage(self.create_welcome_page())
        self.addPage(self.create_company_page())
        self.addPage(self.create_numbering_page())

    def create_welcome_page(self) -> QWizardPage:
        page = QWizardPage()
        page.setTitle(f"Welcome to {APP_NAME}")
        page.setSubTitle("Commercial-grade invoice generator for modern businesses.")

        layout = QVBoxLayout(page)
        layout.setSpacing(14)

        lbl_desc = QLabel(
            f"<b>{APP_NAME}</b> helps you effortlessly create, manage, and export professional "
            "business invoices matching standard trade and commercial formats.<br/><br/>"
            "Let's configure your basic business information to get started in seconds."
        )
        lbl_desc.setWordWrap(True)
        layout.addWidget(lbl_desc)
        layout.addStretch()
        return page

    def create_company_page(self) -> QWizardPage:
        page = QWizardPage()
        page.setTitle("Company Information")
        page.setSubTitle("Enter your business details that appear on printed invoices.")

        layout = QGridLayout(page)
        layout.setSpacing(10)

        layout.addWidget(QLabel("Business Name * :"), 0, 0)
        self.edit_comp_name = QLineEdit("POULTRY SMART TRADERS")
        layout.addWidget(self.edit_comp_name, 0, 1)

        layout.addWidget(QLabel("Address * :"), 1, 0)
        self.edit_comp_addr = QLineEdit("23-A Gulshan Iqbal Alla Din Park, Karachi (Pak.)")
        layout.addWidget(self.edit_comp_addr, 1, 1)

        layout.addWidget(QLabel("Email:"), 2, 0)
        self.edit_comp_email = QLineEdit("poultrysmarttraders01@gmail.com")
        layout.addWidget(self.edit_comp_email, 2, 1)

        layout.addWidget(QLabel("Signatory Name:"), 3, 0)
        self.edit_coord_name = QLineEdit("Dennis")
        layout.addWidget(self.edit_coord_name, 3, 1)

        return page

    def create_numbering_page(self) -> QWizardPage:
        page = QWizardPage()
        page.setTitle("Currency & Numbering Preferences")
        page.setSubTitle("Configure your starting invoice number and currency.")

        layout = QGridLayout(page)
        layout.setSpacing(10)

        layout.addWidget(QLabel("Currency Symbol:"), 0, 0)
        self.edit_currency = QLineEdit("Rs.")
        layout.addWidget(self.edit_currency, 0, 1)

        layout.addWidget(QLabel("Invoice Prefix:"), 1, 0)
        self.edit_prefix = QLineEdit("")
        self.edit_prefix.setPlaceholderText("e.g. INV-")
        layout.addWidget(self.edit_prefix, 1, 1)

        layout.addWidget(QLabel("Starting Invoice #:"), 2, 0)
        self.spin_start_num = QSpinBox()
        self.spin_start_num.setRange(1, 99999999)
        self.spin_start_num.setValue(468)
        layout.addWidget(self.spin_start_num, 2, 1)

        return page

    def accept(self):
        # Save wizard data into database
        data = {
            "name": self.edit_comp_name.text().strip() or "POULTRY SMART TRADERS",
            "address": self.edit_comp_addr.text().strip() or "23-A Gulshan Iqbal Alla Din Park, Karachi (Pak.)",
            "email": self.edit_comp_email.text().strip(),
            "sales_coordinator_name": self.edit_coord_name.text().strip() or "Dennis",
            "default_currency": self.edit_currency.text().strip() or "Rs.",
            "invoice_prefix": self.edit_prefix.text().strip(),
            "next_invoice_number": self.spin_start_num.value()
        }
        session = SessionLocal()
        try:
            CompanyService.update_company_profile(session, data)
        finally:
            session.close()

        super().accept()


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"About {APP_NAME}")
        self.setFixedSize(480, 380)
        self.setStyleSheet("QDialog { background: #FFFFFF; }")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(14)

        # ── App name & version ────────────────────────────────────────────────
        lbl_app = QLabel(APP_NAME)
        lbl_app.setFont(QFont("Segoe UI", 20, QFont.Bold))
        lbl_app.setStyleSheet("color: #0A2540; background: transparent;")
        layout.addWidget(lbl_app)

        lbl_sub = QLabel(f"{APP_SUBTITLE}  —  Version {APP_VERSION}")
        lbl_sub.setFont(QFont("Segoe UI", 10))
        lbl_sub.setStyleSheet("color: #64748B; background: transparent;")
        layout.addWidget(lbl_sub)

        # ── Divider ───────────────────────────────────────────────────────────
        div = QFrame()
        div.setFrameShape(QFrame.HLine)
        div.setStyleSheet("background: #E2E8F0; border: none; max-height: 1px;")
        div.setFixedHeight(1)
        layout.addWidget(div)

        # ── Info card ─────────────────────────────────────────────────────────
        card = QFrame()
        card.setStyleSheet(
            "QFrame { background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; }"
        )
        card_lay = QVBoxLayout(card)
        card_lay.setContentsMargins(18, 14, 18, 14)
        card_lay.setSpacing(7)

        _label_style = "color: #1E293B; font-size: 13px; background: transparent;"

        def _row(html: str) -> QLabel:
            lbl = QLabel(html)
            lbl.setTextFormat(Qt.RichText)
            lbl.setStyleSheet(_label_style)
            lbl.setWordWrap(True)
            return lbl

        card_lay.addWidget(_row("<b style='color:#0A2540;'>Tech Stack:</b>  Python 3, PySide6, SQLAlchemy, SQLite, ReportLab"))
        card_lay.addWidget(_row("<b style='color:#0A2540;'>Design:</b>  Navy / Red professional invoice layout"))

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("background: #E2E8F0; border: none; max-height: 1px;")
        sep.setFixedHeight(1)
        card_lay.addWidget(sep)

        card_lay.addWidget(_row("<b style='color:#0A2540;'>Keyboard Shortcuts</b>"))
        shortcuts = [
            ("Ctrl + N", "New Invoice"),
            ("Ctrl + S", "Save Invoice"),
            ("Ctrl + P", "Print Invoice"),
            ("Ctrl + F", "Search Invoices"),
            ("Ctrl + Q", "Exit Application"),
        ]
        for keys, desc in shortcuts:
            card_lay.addWidget(_row(
                f"&nbsp;&nbsp;<b style='color:#C8102E;'>{keys}</b>"
                f"<span style='color:#475569;'>  —  {desc}</span>"
            ))

        layout.addWidget(card)
        layout.addStretch()

        # ── Close button ──────────────────────────────────────────────────────
        btn_close = QPushButton("  Close")
        btn_close.setFixedHeight(38)
        btn_close.setMinimumWidth(100)
        btn_close.setCursor(Qt.PointingHandCursor)
        btn_close.setFont(QFont("Segoe UI", 11, QFont.Bold))
        btn_close.setStyleSheet("""
            QPushButton {
                background-color: #0A2540;
                color: #FFFFFF;
                font-weight: 600;
                border: none;
                border-radius: 6px;
                padding: 8px 24px;
            }
            QPushButton:hover   { background-color: #1E3A8A; }
            QPushButton:pressed { background-color: #002D62; }
        """)
        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close, 0, Qt.AlignRight)
