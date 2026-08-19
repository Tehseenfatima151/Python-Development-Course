"""
Company Settings & Preferences Screen for InvoicePro
"""
import os
from decimal import Decimal
from typing import Optional

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit,
    QTextEdit, QPushButton, QTabWidget, QFileDialog, QFrame, QScrollArea,
    QMessageBox, QDoubleSpinBox, QSpinBox, QSizePolicy
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QPixmap

from app.database.db import SessionLocal
from app.database.repositories import CompanyRepository
from app.services.company_service import CompanyService
from app.ui.components.toast import ToastNotification


# ── Shared inline styles ──────────────────────────────────────────────────────
_FIELD = (
    "QLineEdit, QTextEdit, QDoubleSpinBox, QSpinBox {"
    "  background-color: #FFFFFF;"
    "  border: 1.5px solid #CBD5E1;"
    "  border-radius: 6px;"
    "  padding: 7px 10px;"
    "  color: #0F172A;"
    "  font-size: 13px;"
    "}"
    "QLineEdit:focus, QTextEdit:focus, QDoubleSpinBox:focus, QSpinBox:focus {"
    "  border: 1.5px solid #0A2540;"
    "  background-color: #F8FAFC;"
    "}"
    "QLineEdit:disabled {"
    "  background-color: #F1F5F9;"
    "  color: #94A3B8;"
    "}"
)

_BTN_PRIMARY = (
    "QPushButton { background-color:#0A2540; color:#FFFFFF; font-size:13px;"
    " font-weight:600; border:none; border-radius:6px; padding:8px 20px; }"
    "QPushButton:hover   { background-color:#1E3A8A; }"
    "QPushButton:pressed { background-color:#002D62; }"
)

_BTN_SEC = (
    "QPushButton { background-color:#FFFFFF; color:#334155; font-size:13px;"
    " font-weight:500; border:1.5px solid #CBD5E1; border-radius:6px; padding:7px 14px; }"
    "QPushButton:hover   { background-color:#F1F5F9; border-color:#94A3B8; color:#0A2540; }"
    "QPushButton:pressed { background-color:#E2E8F0; }"
)

_LBL = "QLabel { color: #374151; font-size: 13px; font-weight: 500; background: transparent; }"


def _label(text: str) -> QLabel:
    lbl = QLabel(text)
    lbl.setStyleSheet(_LBL)
    lbl.setMinimumWidth(180)
    lbl.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
    return lbl


def _field(placeholder: str = "", height: int = 38) -> QLineEdit:
    f = QLineEdit()
    f.setPlaceholderText(placeholder)
    f.setFixedHeight(height)
    f.setStyleSheet(_FIELD)
    return f


def _section_card(title: str) -> tuple:
    """Returns (card_frame, grid_layout)"""
    card = QFrame()
    card.setStyleSheet(
        "QFrame { background:#FFFFFF; border:1px solid #E2E8F0;"
        " border-radius:10px; }"
    )
    vlay = QVBoxLayout(card)
    vlay.setContentsMargins(0, 0, 0, 0)
    vlay.setSpacing(0)

    # Card header
    hdr = QWidget()
    hdr.setFixedHeight(44)
    hdr.setStyleSheet(
        "QWidget { background:#F8FAFC; border-radius:10px 10px 0 0;"
        " border-bottom:1px solid #E2E8F0; }"
    )
    hdr_lay = QHBoxLayout(hdr)
    hdr_lay.setContentsMargins(18, 0, 18, 0)
    lbl = QLabel(title)
    lbl.setFont(QFont("Segoe UI", 11, QFont.Bold))
    lbl.setStyleSheet("color:#0A2540; background:transparent; border:none;")
    hdr_lay.addWidget(lbl)
    vlay.addWidget(hdr)

    # Card body grid
    body = QWidget()
    body.setStyleSheet("QWidget { background:#FFFFFF; border-radius:0 0 10px 10px; }")
    grid = QGridLayout(body)
    grid.setContentsMargins(20, 16, 20, 20)
    grid.setSpacing(14)
    grid.setColumnStretch(1, 1)
    grid.setColumnMinimumWidth(0, 190)
    vlay.addWidget(body)

    return card, grid


class CompanySettingsWidget(QWidget):
    settings_saved = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.logo_path_val: Optional[str] = None
        self.stamp_path_val: Optional[str] = None
        self.sig_path_val: Optional[str] = None
        self.setup_ui()
        self.load_settings()

    # ── UI BUILD ──────────────────────────────────────────────────────────────
    def setup_ui(self):
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("background: transparent; border: none;")

        container = QWidget()
        container.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(28, 24, 28, 28)
        layout.setSpacing(20)

        # ── Page Header ──────────────────────────────────────────────────────
        hdr_row = QHBoxLayout()
        title_col = QVBoxLayout()
        title_col.setSpacing(4)

        lbl_title = QLabel("Company Profile")
        lbl_title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        lbl_title.setStyleSheet("color: #0A2540;")
        title_col.addWidget(lbl_title)

        lbl_sub = QLabel("Configure your business information, branding, and invoice settings")
        lbl_sub.setFont(QFont("Segoe UI", 11))
        lbl_sub.setStyleSheet("color: #64748B;")
        title_col.addWidget(lbl_sub)

        hdr_row.addLayout(title_col)
        hdr_row.addStretch()

        btn_save_top = QPushButton("💾  Save Changes")
        btn_save_top.setFont(QFont("Segoe UI", 11, QFont.Bold))
        btn_save_top.setFixedHeight(40)
        btn_save_top.setMinimumWidth(160)
        btn_save_top.setCursor(Qt.PointingHandCursor)
        btn_save_top.setStyleSheet(_BTN_PRIMARY)
        btn_save_top.clicked.connect(self.save_settings)
        hdr_row.addWidget(btn_save_top)

        layout.addLayout(hdr_row)

        # ── Tab widget ───────────────────────────────────────────────────────
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #E2E8F0;
                border-radius: 0 0 10px 10px;
                background: #F8FAFC;
            }
            QTabBar::tab {
                background: #F1F5F9;
                color: #475569;
                padding: 10px 22px;
                font-size: 13px;
                font-weight: 600;
                border: none;
                border-bottom: 3px solid transparent;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: #FFFFFF;
                color: #0A2540;
                border-bottom: 3px solid #0A2540;
            }
            QTabBar::tab:hover:!selected {
                background: #E2E8F0;
                color: #0A2540;
            }
        """)

        self.tabs.addTab(self._build_profile_tab(),  "🏢  Company Profile")
        self.tabs.addTab(self._build_branding_tab(), "🎨  Branding & Signatures")
        self.tabs.addTab(self._build_prefs_tab(),    "⚙  Numbering & Defaults")
        self.tabs.addTab(self._build_bank_tab(),     "🏦  Banking & Payment Terms")

        layout.addWidget(self.tabs)

        # Bottom save button
        btn_save_bot = QPushButton("💾  Save All Settings")
        btn_save_bot.setFixedHeight(42)
        btn_save_bot.setFont(QFont("Segoe UI", 11, QFont.Bold))
        btn_save_bot.setCursor(Qt.PointingHandCursor)
        btn_save_bot.setStyleSheet(_BTN_PRIMARY)
        btn_save_bot.clicked.connect(self.save_settings)
        layout.addWidget(btn_save_bot)

        scroll.setWidget(container)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.addWidget(scroll)

    # ── TAB 1: Business Profile ───────────────────────────────────────────────
    def _build_profile_tab(self) -> QWidget:
        tab = QWidget()
        tab.setStyleSheet("background: #F8FAFC;")
        vlay = QVBoxLayout(tab)
        vlay.setContentsMargins(20, 20, 20, 20)
        vlay.setSpacing(16)

        card, grid = _section_card("Business Information")

        rows = [
            ("Business Name *",    "_name",    "e.g. POULTRY SMART TRADERS"),
            ("Business Tagline",   "_tagline", "e.g. Trusted Poultry Suppliers"),
            ("Physical Address *", "_address", "e.g. 23-A Gulshan Iqbal, Karachi"),
            ("Email Address",      "_email",   "e.g. info@company.com"),
            ("Phone Number",       "_phone",   "e.g. +92 300 1234567"),
            ("Website",            "_website", "e.g. www.company.com"),
            ("Tax ID / NTN",       "_tax_id",  "e.g. 1234567-8"),
            ("Registration No.",   "_reg_no",  "e.g. REG-0001"),
        ]

        for i, (label, attr, placeholder) in enumerate(rows):
            grid.addWidget(_label(label + ":"), i, 0)
            f = _field(placeholder)
            setattr(self, "edit" + attr, f)
            grid.addWidget(f, i, 1)

        vlay.addWidget(card)
        vlay.addStretch()
        return tab

    # ── TAB 2: Branding ───────────────────────────────────────────────────────
    def _build_branding_tab(self) -> QWidget:
        tab = QWidget()
        tab.setStyleSheet("background: #F8FAFC;")
        vlay = QVBoxLayout(tab)
        vlay.setContentsMargins(20, 20, 20, 20)
        vlay.setSpacing(16)

        card, grid = _section_card("Logos, Stamps & Signatures")

        # ── Logo row
        grid.addWidget(_label("Company Logo:"), 0, 0)
        logo_w = QWidget()
        logo_w.setStyleSheet("background:transparent;")
        logo_row = QHBoxLayout(logo_w)
        logo_row.setContentsMargins(0, 0, 0, 0)
        logo_row.setSpacing(10)

        self.lbl_logo_preview = QLabel("Vector Default Active")
        self.lbl_logo_preview.setFixedSize(150, 60)
        self.lbl_logo_preview.setStyleSheet(
            "border: 2px dashed #CBD5E1; background: #F8FAFC;"
            " border-radius: 6px; color: #94A3B8; font-size:11px;"
        )
        self.lbl_logo_preview.setAlignment(Qt.AlignCenter)
        logo_row.addWidget(self.lbl_logo_preview)

        btn_ul = QPushButton("📁  Choose Logo...")
        btn_ul.setFixedHeight(36)
        btn_ul.setStyleSheet(_BTN_SEC)
        btn_ul.clicked.connect(self.choose_logo)
        logo_row.addWidget(btn_ul)

        btn_cl = QPushButton("✕  Clear")
        btn_cl.setFixedHeight(36)
        btn_cl.setStyleSheet(_BTN_SEC)
        btn_cl.clicked.connect(self.clear_logo)
        logo_row.addWidget(btn_cl)
        logo_row.addStretch()
        grid.addWidget(logo_w, 0, 1)

        # ── Stamp row
        grid.addWidget(_label("Company Stamp / Seal:"), 1, 0)
        stamp_w = QWidget()
        stamp_w.setStyleSheet("background:transparent;")
        stamp_row = QHBoxLayout(stamp_w)
        stamp_row.setContentsMargins(0, 0, 0, 0)
        stamp_row.setSpacing(10)

        self.lbl_stamp_preview = QLabel("Vector Stamp Active")
        self.lbl_stamp_preview.setFixedSize(80, 80)
        self.lbl_stamp_preview.setStyleSheet(
            "border: 2px dashed #CBD5E1; background: #F8FAFC;"
            " border-radius: 6px; color: #94A3B8; font-size:11px;"
        )
        self.lbl_stamp_preview.setAlignment(Qt.AlignCenter)
        stamp_row.addWidget(self.lbl_stamp_preview)

        btn_us = QPushButton("📁  Choose Stamp...")
        btn_us.setFixedHeight(36)
        btn_us.setStyleSheet(_BTN_SEC)
        btn_us.clicked.connect(self.choose_stamp)
        stamp_row.addWidget(btn_us)

        btn_cs = QPushButton("✕  Clear")
        btn_cs.setFixedHeight(36)
        btn_cs.setStyleSheet(_BTN_SEC)
        btn_cs.clicked.connect(self.clear_stamp)
        stamp_row.addWidget(btn_cs)
        stamp_row.addStretch()
        grid.addWidget(stamp_w, 1, 1)

        # ── Signature row
        grid.addWidget(_label("Signature Image:"), 2, 0)
        sig_w = QWidget()
        sig_w.setStyleSheet("background:transparent;")
        sig_row = QHBoxLayout(sig_w)
        sig_row.setContentsMargins(0, 0, 0, 0)
        sig_row.setSpacing(10)

        self.lbl_sig_preview = QLabel("Script Signature Active")
        self.lbl_sig_preview.setFixedSize(150, 55)
        self.lbl_sig_preview.setStyleSheet(
            "border: 2px dashed #CBD5E1; background: #F8FAFC;"
            " border-radius: 6px; color: #94A3B8; font-size:11px;"
        )
        self.lbl_sig_preview.setAlignment(Qt.AlignCenter)
        sig_row.addWidget(self.lbl_sig_preview)

        btn_usi = QPushButton("📁  Choose Signature...")
        btn_usi.setFixedHeight(36)
        btn_usi.setStyleSheet(_BTN_SEC)
        btn_usi.clicked.connect(self.choose_signature)
        sig_row.addWidget(btn_usi)

        btn_csi = QPushButton("✕  Clear")
        btn_csi.setFixedHeight(36)
        btn_csi.setStyleSheet(_BTN_SEC)
        btn_csi.clicked.connect(self.clear_signature)
        sig_row.addWidget(btn_csi)
        sig_row.addStretch()
        grid.addWidget(sig_w, 2, 1)

        # ── Sales coordinator
        grid.addWidget(_label("Sales Coordinator Name:"), 3, 0)
        self.edit_sales_coord = _field("e.g. Dennis")
        grid.addWidget(self.edit_sales_coord, 3, 1)

        vlay.addWidget(card)
        vlay.addStretch()
        return tab

    # ── TAB 3: Numbering & Defaults ───────────────────────────────────────────
    def _build_prefs_tab(self) -> QWidget:
        tab = QWidget()
        tab.setStyleSheet("background: #F8FAFC;")
        vlay = QVBoxLayout(tab)
        vlay.setContentsMargins(20, 20, 20, 20)
        vlay.setSpacing(16)

        card, grid = _section_card("Invoice Numbering & Currency")

        grid.addWidget(_label("Default Currency Symbol:"), 0, 0)
        self.edit_currency = _field("e.g. Rs.")
        grid.addWidget(self.edit_currency, 0, 1)

        grid.addWidget(_label("Default Tax Rate (%):"), 1, 0)
        self.spin_tax = QDoubleSpinBox()
        self.spin_tax.setRange(0.0, 100.0)
        self.spin_tax.setDecimals(2)
        self.spin_tax.setValue(0.0)
        self.spin_tax.setFixedHeight(38)
        self.spin_tax.setStyleSheet(_FIELD)
        grid.addWidget(self.spin_tax, 1, 1)

        grid.addWidget(_label("Invoice Prefix:"), 2, 0)
        self.edit_prefix = _field("e.g. INV- or leave blank")
        grid.addWidget(self.edit_prefix, 2, 1)

        grid.addWidget(_label("Next Invoice Number:"), 3, 0)
        self.spin_next_num = QSpinBox()
        self.spin_next_num.setRange(1, 99999999)
        self.spin_next_num.setValue(468)
        self.spin_next_num.setFixedHeight(38)
        self.spin_next_num.setStyleSheet(_FIELD)
        grid.addWidget(self.spin_next_num, 3, 1)

        vlay.addWidget(card)
        vlay.addStretch()
        return tab

    # ── TAB 4: Banking ────────────────────────────────────────────────────────
    def _build_bank_tab(self) -> QWidget:
        tab = QWidget()
        tab.setStyleSheet("background: #F8FAFC;")
        vlay = QVBoxLayout(tab)
        vlay.setContentsMargins(20, 20, 20, 20)
        vlay.setSpacing(16)

        card, grid = _section_card("Bank Details & Payment Terms")

        grid.addWidget(_label("Bank Name:"), 0, 0)
        self.edit_bank_name = _field("e.g. HBL / MCB / Meezan")
        grid.addWidget(self.edit_bank_name, 0, 1)

        grid.addWidget(_label("Account Number:"), 1, 0)
        self.edit_bank_acc = _field("e.g. 01234567890123")
        grid.addWidget(self.edit_bank_acc, 1, 1)

        grid.addWidget(_label("IBAN:"), 2, 0)
        self.edit_iban = _field("e.g. PK36SCBL0000001123456702")
        grid.addWidget(self.edit_iban, 2, 1)

        grid.addWidget(_label("Default Payment Terms:"), 3, 0, Qt.AlignTop)
        self.edit_terms = QTextEdit()
        self.edit_terms.setPlaceholderText("e.g. Payment due within 15 days from invoice date.")
        self.edit_terms.setFixedHeight(90)
        self.edit_terms.setStyleSheet(_FIELD)
        grid.addWidget(self.edit_terms, 3, 1)

        vlay.addWidget(card)
        vlay.addStretch()
        return tab

    # ── Data loading ──────────────────────────────────────────────────────────
    def load_settings(self):
        session = SessionLocal()
        try:
            company = CompanyRepository.get_company(session)
            if not company:
                return

            self.edit_name.setText(company.name or "")
            self.edit_tagline.setText(company.tagline or "")
            self.edit_address.setText(company.address or "")
            self.edit_email.setText(company.email or "")
            self.edit_phone.setText(company.phone or "")
            self.edit_website.setText(company.website or "")
            self.edit_tax_id.setText(company.tax_id or "")
            self.edit_reg_no.setText(company.reg_no or "")

            self.logo_path_val = company.logo_path
            if self.logo_path_val and os.path.exists(self.logo_path_val):
                pix = QPixmap(self.logo_path_val).scaled(
                    150, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
                self.lbl_logo_preview.setPixmap(pix)

            self.stamp_path_val = company.stamp_path
            if self.stamp_path_val and os.path.exists(self.stamp_path_val):
                pix = QPixmap(self.stamp_path_val).scaled(
                    80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
                self.lbl_stamp_preview.setPixmap(pix)

            self.sig_path_val = company.signature_path
            if self.sig_path_val and os.path.exists(self.sig_path_val):
                pix = QPixmap(self.sig_path_val).scaled(
                    150, 55, Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
                self.lbl_sig_preview.setPixmap(pix)

            self.edit_sales_coord.setText(company.sales_coordinator_name or "Dennis")
            self.edit_currency.setText(company.default_currency or "Rs.")
            self.spin_tax.setValue(float(company.default_tax_rate or 0.0))
            self.edit_prefix.setText(company.invoice_prefix or "")
            self.spin_next_num.setValue(int(company.next_invoice_number or 468))
            self.edit_bank_name.setText(company.bank_name or "")
            self.edit_bank_acc.setText(company.bank_account or "")
            self.edit_iban.setText(company.iban or "")
            self.edit_terms.setPlainText(company.payment_instructions or "")

        finally:
            session.close()

    # ── Image choosers ────────────────────────────────────────────────────────
    def choose_logo(self):
        p, _ = QFileDialog.getOpenFileName(
            self, "Select Company Logo", "", "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if p:
            self.logo_path_val = p
            pix = QPixmap(p).scaled(150, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.lbl_logo_preview.setPixmap(pix)

    def clear_logo(self):
        self.logo_path_val = None
        self.lbl_logo_preview.clear()
        self.lbl_logo_preview.setText("Vector Default Active")

    def choose_stamp(self):
        p, _ = QFileDialog.getOpenFileName(
            self, "Select Company Stamp", "", "Images (*.png *.jpg *.jpeg)"
        )
        if p:
            self.stamp_path_val = p
            pix = QPixmap(p).scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.lbl_stamp_preview.setPixmap(pix)

    def clear_stamp(self):
        self.stamp_path_val = None
        self.lbl_stamp_preview.clear()
        self.lbl_stamp_preview.setText("Vector Stamp Active")

    def choose_signature(self):
        p, _ = QFileDialog.getOpenFileName(
            self, "Select Signature Image", "", "Images (*.png *.jpg *.jpeg)"
        )
        if p:
            self.sig_path_val = p
            pix = QPixmap(p).scaled(150, 55, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.lbl_sig_preview.setPixmap(pix)

    def clear_signature(self):
        self.sig_path_val = None
        self.lbl_sig_preview.clear()
        self.lbl_sig_preview.setText("Script Signature Active")

    # ── Save ──────────────────────────────────────────────────────────────────
    def save_settings(self):
        name = self.edit_name.text().strip()
        if not name:
            QMessageBox.warning(self, "Validation Error", "Business name is required.")
            return

        data = {
            "name":                   name,
            "tagline":                self.edit_tagline.text().strip(),
            "address":                self.edit_address.text().strip(),
            "email":                  self.edit_email.text().strip(),
            "phone":                  self.edit_phone.text().strip(),
            "website":                self.edit_website.text().strip(),
            "tax_id":                 self.edit_tax_id.text().strip(),
            "reg_no":                 self.edit_reg_no.text().strip(),
            "logo_path":              self.logo_path_val,
            "stamp_path":             self.stamp_path_val,
            "signature_path":         self.sig_path_val,
            "sales_coordinator_name": self.edit_sales_coord.text().strip() or "Dennis",
            "default_currency":       self.edit_currency.text().strip() or "Rs.",
            "default_tax_rate":       Decimal(str(self.spin_tax.value())),
            "invoice_prefix":         self.edit_prefix.text().strip(),
            "next_invoice_number":    self.spin_next_num.value(),
            "bank_name":              self.edit_bank_name.text().strip(),
            "bank_account":           self.edit_bank_acc.text().strip(),
            "iban":                   self.edit_iban.text().strip(),
            "payment_instructions":   self.edit_terms.toPlainText().strip(),
        }

        session = SessionLocal()
        try:
            success, comp, msg = CompanyService.update_company_profile(session, data)
            if success:
                ToastNotification.show_toast(
                    self.window(), "Company settings saved successfully.", "success"
                )
                self.settings_saved.emit()
            else:
                QMessageBox.critical(self, "Error", msg)
        finally:
            session.close()
