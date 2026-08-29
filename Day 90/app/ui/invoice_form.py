"""
Invoice Form Screen for InvoicePro — Redesigned UX
Tab-based interface: [📝 Edit Invoice] [👁 Preview Invoice]

Edit tab:
  ┌─ Invoice Details card ──────────────────────────────────┐
  ├─ Customer & Delivery card ──────────────────────────────┤
  ├─ Products / Line Items card ────────────────────────────┤
  ├─ Financial Summary card ────────────────────────────────┤
  └─ Notes & Payment card (collapsible) ───────────────────┘
  [Reset] [Save Draft] [Save Invoice ✅] [Preview] [PDF] [Print]

Preview tab:
  Full-width A4 canvas with Fit/Zoom controls.
"""
from datetime import date
from decimal import Decimal
from typing import Optional, Dict, Any, List

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit,
    QDateEdit, QComboBox, QDoubleSpinBox, QTextEdit, QPushButton,
    QScrollArea, QFrame, QMessageBox, QTabWidget, QSplitter, QSizePolicy,
    QSpacerItem
)
from PySide6.QtCore import Qt, Signal, QDate, QTimer
from PySide6.QtGui import QFont, QColor

from app.database.db import SessionLocal
from app.database.repositories import CustomerRepository, CompanyRepository, InvoiceRepository
from app.services.invoice_service import InvoiceService
from app.services.calculation_service import CalculationService, to_decimal
from app.services.pdf_service import PDFService
from app.utils.formatters import format_currency, format_invoice_number
from app.ui.components.items_table import ItemsTableWidget
from app.ui.components.toast import ToastNotification
from app.ui.invoice_preview import InvoicePreviewWidget
from app.ui.dialogs.customer_dialog import CustomerDialog


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────
def _section_label(text: str) -> QLabel:
    """Bold navy section heading."""
    lbl = QLabel(text)
    lbl.setFont(QFont("Segoe UI", 10, QFont.Bold))
    lbl.setStyleSheet("color: #0A2540; padding: 0px;")
    return lbl


def _field_label(text: str) -> QLabel:
    """Small gray field label."""
    lbl = QLabel(text)
    lbl.setFont(QFont("Segoe UI", 8))
    lbl.setStyleSheet("color: #64748B;")
    return lbl


def _card(title: str = "") -> tuple:
    """Returns (card_frame, card_body_layout). card_body_layout is a QVBoxLayout."""
    frame = QFrame()
    frame.setObjectName("invoiceCard")
    frame.setStyleSheet(
        "#invoiceCard {"
        "  background: #FFFFFF;"
        "  border: 1px solid #E2E8F0;"
        "  border-radius: 8px;"
        "}"
    )
    outer = QVBoxLayout(frame)
    outer.setContentsMargins(0, 0, 0, 0)
    outer.setSpacing(0)

    if title:
        header = QWidget()
        header.setStyleSheet(
            "background: #F8FAFC; border-radius: 8px 8px 0 0;"
            " border-bottom: 1px solid #E2E8F0;"
        )
        h_lay = QHBoxLayout(header)
        h_lay.setContentsMargins(16, 10, 16, 10)
        lbl = QLabel(title)
        lbl.setFont(QFont("Segoe UI", 10, QFont.Bold))
        lbl.setStyleSheet("color: #0A2540; background: transparent;")
        h_lay.addWidget(lbl)
        outer.addWidget(header)

    body = QVBoxLayout()
    body.setContentsMargins(16, 14, 16, 14)
    body.setSpacing(10)
    outer.addLayout(body)

    return frame, body


def _input_style() -> str:
    return (
        "QLineEdit, QDateEdit, QComboBox, QDoubleSpinBox, QTextEdit {"
        "  border: 1px solid #CBD5E1; border-radius: 5px;"
        "  padding: 6px 10px; background: #FFFFFF;"
        "  color: #0F172A; font-size: 13px;"
        "}"
        "QLineEdit:focus, QDateEdit:focus, QComboBox:focus, QDoubleSpinBox:focus, QTextEdit:focus {"
        "  border: 1.5px solid #0A2540; background: #F8FAFC;"
        "}"
        "QLineEdit:disabled, QComboBox:disabled, QDoubleSpinBox:disabled {"
        "  background: #F1F5F9; color: #94A3B8;"
        "}"
    )


# ─────────────────────────────────────────────────────────────────────────────
# Main Form Widget
# ─────────────────────────────────────────────────────────────────────────────
class InvoiceFormWidget(QWidget):
    invoice_saved = Signal(int)  # Emits invoice ID when saved

    def __init__(self, parent=None):
        super().__init__(parent)
        self.editing_invoice_id: Optional[int] = None
        self.company_data: Dict[str, Any] = {}

        self.setup_ui()
        self.load_company_data()
        self.load_customers_dropdown()
        self.reset_form()

    # ─────────────────────────────────────────────────────────────────────────
    # UI BUILD
    # ─────────────────────────────────────────────────────────────────────────
    def setup_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Page header strip (outside tabs) ─────────────────────────────────
        page_header = QWidget()
        page_header.setStyleSheet("background: #FFFFFF; border-bottom: 1px solid #E2E8F0;")
        ph_lay = QHBoxLayout(page_header)
        ph_lay.setContentsMargins(28, 16, 28, 16)
        ph_lay.setSpacing(0)

        ph_title_col = QVBoxLayout()
        ph_title_col.setSpacing(4)

        self.lbl_page_title = QLabel("New Invoice")
        self.lbl_page_title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        self.lbl_page_title.setStyleSheet("color: #0A2540; background: transparent;")
        ph_title_col.addWidget(self.lbl_page_title)

        lbl_page_sub = QLabel("Fill in the details below, then save or preview the invoice")
        lbl_page_sub.setFont(QFont("Segoe UI", 10))
        lbl_page_sub.setStyleSheet("color: #64748B; background: transparent;")
        ph_title_col.addWidget(lbl_page_sub)

        ph_lay.addLayout(ph_title_col)
        ph_lay.addStretch()

        root.addWidget(page_header)

        # ── Tab bar ──────────────────────────────────────────────────────────
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setStyleSheet(
            "QTabWidget::pane { border: none; background: #F8FAFC; }"
            "QTabBar::tab {"
            "  background: #E2E8F0; color: #64748B;"
            "  padding: 10px 28px; font-size: 13px; font-weight: 600;"
            "  border: none; border-bottom: 3px solid transparent;"
            "  margin-right: 2px;"
            "}"
            "QTabBar::tab:selected {"
            "  background: #FFFFFF; color: #0A2540;"
            "  border-bottom: 3px solid #0A2540;"
            "}"
            "QTabBar::tab:hover:!selected { background: #CBD5E1; }"
        )

        # Build the two tabs
        self.tab_edit    = self._build_edit_tab()
        self.tab_preview = self._build_preview_tab()

        self.tabs.addTab(self.tab_edit,    "✏️   Edit Invoice")
        self.tabs.addTab(self.tab_preview, "👁️   Preview Invoice")

        # Update page title when switching tabs
        self.tabs.currentChanged.connect(self._on_tab_changed)

        root.addWidget(self.tabs)

    # ──────────────────────────────────────────────────────────────────────────
    # TAB 1: Edit Invoice
    # ──────────────────────────────────────────────────────────────────────────
    def _build_edit_tab(self) -> QWidget:
        container = QWidget()
        container.setStyleSheet("background: #F8FAFC;")
        vlay = QVBoxLayout(container)
        vlay.setContentsMargins(0, 0, 0, 0)
        vlay.setSpacing(0)

        # ── Scrollable body ──────────────────────────────────────────────────
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: transparent; border: none;")
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        body_widget = QWidget()
        body_widget.setStyleSheet("background: transparent;")
        body_lay = QVBoxLayout(body_widget)
        body_lay.setContentsMargins(20, 16, 20, 16)
        body_lay.setSpacing(16)

        # ── Section 1: Invoice Details ────────────────────────────────────────
        card1, lay1 = _card("🧾  Invoice Details")
        body_lay.addWidget(card1)

        grid1 = QGridLayout()
        grid1.setSpacing(10)
        grid1.setColumnStretch(1, 1)
        grid1.setColumnStretch(3, 1)

        # Row 0: Invoice # | Book Serial (No)
        grid1.addWidget(_field_label("Invoice #"), 0, 0)
        inv_num_row = QHBoxLayout()
        self.edit_inv_num = QLineEdit()
        self.edit_inv_num.setPlaceholderText("Auto-generated")
        self.edit_inv_num.setStyleSheet(_input_style())
        self.edit_inv_num.textChanged.connect(self.trigger_live_update)
        inv_num_row.addWidget(self.edit_inv_num)
        lbl_auto = QLabel("Auto ✓")
        lbl_auto.setStyleSheet("color: #10B981; font-size: 11px; padding-left: 4px;")
        inv_num_row.addWidget(lbl_auto)
        inv_num_row.setStretch(0, 1)
        grid1.addLayout(inv_num_row, 0, 1)

        grid1.addWidget(_field_label("Book Serial (No)"), 0, 2)
        self.edit_manual_no = QLineEdit()
        self.edit_manual_no.setPlaceholderText("e.g. 818406")
        self.edit_manual_no.setStyleSheet(_input_style())
        self.edit_manual_no.textChanged.connect(self.trigger_live_update)
        grid1.addWidget(self.edit_manual_no, 0, 3)

        # Row 1: Date | Order #
        grid1.addWidget(_field_label("Invoice Date"), 1, 0)
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setDisplayFormat("dd-MM-yyyy")
        self.date_edit.setStyleSheet(_input_style())
        self.date_edit.dateChanged.connect(self.trigger_live_update)
        grid1.addWidget(self.date_edit, 1, 1)

        grid1.addWidget(_field_label("Order #"), 1, 2)
        self.edit_order_num = QLineEdit()
        self.edit_order_num.setPlaceholderText("Optional order reference")
        self.edit_order_num.setStyleSheet(_input_style())
        self.edit_order_num.textChanged.connect(self.trigger_live_update)
        grid1.addWidget(self.edit_order_num, 1, 3)

        # Row 2: DC #1 | DC #2
        grid1.addWidget(_field_label("DC # 1"), 2, 0)
        self.edit_dc_1 = QLineEdit()
        self.edit_dc_1.setPlaceholderText("e.g. 466")
        self.edit_dc_1.setStyleSheet(_input_style())
        self.edit_dc_1.textChanged.connect(self.trigger_live_update)
        grid1.addWidget(self.edit_dc_1, 2, 1)

        grid1.addWidget(_field_label("DC # 2"), 2, 2)
        self.edit_dc_2 = QLineEdit()
        self.edit_dc_2.setPlaceholderText("e.g. 82087")
        self.edit_dc_2.setStyleSheet(_input_style())
        self.edit_dc_2.textChanged.connect(self.trigger_live_update)
        grid1.addWidget(self.edit_dc_2, 2, 3)

        lay1.addLayout(grid1)

        # ── Section 2: Customer & Delivery ────────────────────────────────────
        card2, lay2 = _card("👤  Customer & Delivery")
        body_lay.addWidget(card2)

        # Customer selector row
        cust_row = QHBoxLayout()
        cust_row.setSpacing(8)
        lbl_cust = _field_label("Select Customer:")
        lbl_cust.setFixedWidth(130)
        cust_row.addWidget(lbl_cust)

        self.combo_customer = QComboBox()
        self.combo_customer.setStyleSheet(_input_style())
        self.combo_customer.currentIndexChanged.connect(self.on_customer_selected)
        cust_row.addWidget(self.combo_customer, 1)

        btn_add_cust = QPushButton("＋  New Customer")
        btn_add_cust.setFixedHeight(34)
        btn_add_cust.setCursor(Qt.PointingHandCursor)
        btn_add_cust.setStyleSheet(
            "QPushButton { background: #0A2540; color: white; border: none;"
            " border-radius: 5px; padding: 4px 14px; font-size: 12px; }"
            "QPushButton:hover { background: #1E3A8A; }"
        )
        btn_add_cust.clicked.connect(self.open_new_customer_dialog)
        cust_row.addWidget(btn_add_cust)
        lay2.addLayout(cust_row)

        # Delivered To / Invoiced To
        grid2 = QGridLayout()
        grid2.setSpacing(10)
        grid2.setColumnStretch(1, 1)
        grid2.setColumnStretch(3, 1)

        grid2.addWidget(_field_label("Delivered To"), 0, 0)
        self.edit_delivered_to = QLineEdit()
        self.edit_delivered_to.setPlaceholderText("Customer / Recipient Name")
        self.edit_delivered_to.setStyleSheet(_input_style())
        self.edit_delivered_to.textChanged.connect(self.trigger_live_update)
        grid2.addWidget(self.edit_delivered_to, 0, 1)

        grid2.addWidget(_field_label("Invoiced To"), 0, 2)
        self.edit_invoiced_to = QLineEdit("Same")
        self.edit_invoiced_to.setStyleSheet(_input_style())
        self.edit_invoiced_to.textChanged.connect(self.trigger_live_update)
        grid2.addWidget(self.edit_invoiced_to, 0, 3)

        grid2.addWidget(_field_label("Delivery Address"), 1, 0)
        self.edit_address = QLineEdit()
        self.edit_address.setPlaceholderText("City or full delivery address")
        self.edit_address.setStyleSheet(_input_style())
        self.edit_address.textChanged.connect(self.trigger_live_update)
        grid2.addWidget(self.edit_address, 1, 1, 1, 3)

        grid2.addWidget(_field_label("Dispatch Info"), 2, 0)
        self.edit_dispatch = QLineEdit()
        self.edit_dispatch.setPlaceholderText("Transporter, Bilty #, Vehicle #")
        self.edit_dispatch.setStyleSheet(_input_style())
        self.edit_dispatch.textChanged.connect(self.trigger_live_update)
        grid2.addWidget(self.edit_dispatch, 2, 1, 1, 3)

        lay2.addLayout(grid2)

        # ── Section 3: Products table ──────────────────────────────────────────
        self.items_table = ItemsTableWidget()
        self.items_table.items_changed.connect(self.trigger_live_update)
        body_lay.addWidget(self.items_table)

        # ── Section 4: Financial Summary ───────────────────────────────────────
        card4, lay4 = _card("💰  Financial Summary")
        body_lay.addWidget(card4)

        fin_row = QHBoxLayout()
        fin_row.setSpacing(20)

        # Left: adjustments grid
        adj_frame = QFrame()
        adj_frame.setStyleSheet("background: transparent;")
        adj_grid = QGridLayout(adj_frame)
        adj_grid.setContentsMargins(0, 0, 0, 0)
        adj_grid.setSpacing(8)
        adj_grid.setColumnStretch(2, 1)

        # Discount
        adj_grid.addWidget(_field_label("Discount Type:"), 0, 0)
        self.combo_disc_type = QComboBox()
        self.combo_disc_type.addItems(["Flat (Rs.)", "Percent (%)"])
        self.combo_disc_type.setStyleSheet(_input_style())
        self.combo_disc_type.setFixedWidth(120)
        self.combo_disc_type.currentIndexChanged.connect(self.trigger_live_update)
        adj_grid.addWidget(self.combo_disc_type, 0, 1)

        adj_grid.addWidget(_field_label("Discount Value:"), 0, 2)
        self.spin_discount = QDoubleSpinBox()
        self.spin_discount.setRange(0.0, 9999999.0)
        self.spin_discount.setValue(0.0)
        self.spin_discount.setButtonSymbols(QDoubleSpinBox.NoButtons)
        self.spin_discount.setStyleSheet(_input_style())
        self.spin_discount.setFixedWidth(120)
        self.spin_discount.valueChanged.connect(self.trigger_live_update)
        adj_grid.addWidget(self.spin_discount, 0, 3)

        # Tax
        adj_grid.addWidget(_field_label("Tax Rate (%):"), 1, 0)
        self.spin_tax = QDoubleSpinBox()
        self.spin_tax.setRange(0.0, 100.0)
        self.spin_tax.setValue(0.0)
        self.spin_tax.setButtonSymbols(QDoubleSpinBox.NoButtons)
        self.spin_tax.setStyleSheet(_input_style())
        self.spin_tax.setFixedWidth(120)
        self.spin_tax.valueChanged.connect(self.trigger_live_update)
        adj_grid.addWidget(self.spin_tax, 1, 1)

        # Shipping
        adj_grid.addWidget(_field_label("Shipping / Freight:"), 1, 2)
        self.spin_shipping = QDoubleSpinBox()
        self.spin_shipping.setRange(0.0, 9999999.0)
        self.spin_shipping.setValue(0.0)
        self.spin_shipping.setButtonSymbols(QDoubleSpinBox.NoButtons)
        self.spin_shipping.setStyleSheet(_input_style())
        self.spin_shipping.setFixedWidth(120)
        self.spin_shipping.valueChanged.connect(self.trigger_live_update)
        adj_grid.addWidget(self.spin_shipping, 1, 3)

        # Status
        adj_grid.addWidget(_field_label("Invoice Status:"), 2, 0)
        self.combo_status = QComboBox()
        self.combo_status.addItems(["Paid", "Pending", "Draft", "Sent", "Overdue", "Cancelled"])
        self.combo_status.setStyleSheet(_input_style())
        self.combo_status.setFixedWidth(120)
        self.combo_status.currentIndexChanged.connect(self.trigger_live_update)
        adj_grid.addWidget(self.combo_status, 2, 1)

        fin_row.addWidget(adj_frame, 2)

        # Right: summary display
        sum_frame = QFrame()
        sum_frame.setObjectName("summaryBox")
        sum_frame.setStyleSheet(
            "#summaryBox {"
            "  background: #F0F4FF; border: 1.5px solid #C7D7F8;"
            "  border-radius: 8px;"
            "}"
        )
        sum_frame.setMinimumWidth(260)
        sum_frame.setMaximumWidth(340)
        sum_lay = QVBoxLayout(sum_frame)
        sum_lay.setContentsMargins(16, 14, 16, 14)
        sum_lay.setSpacing(6)

        def _sum_row(label, attr_name, big=False):
            row = QHBoxLayout()
            lbl = QLabel(label)
            lbl.setFont(QFont("Segoe UI", 9 if not big else 11, QFont.Bold if big else QFont.Normal))
            lbl.setStyleSheet("color: #475569; background: transparent;" if not big else "color: #0A2540; background: transparent;")
            row.addWidget(lbl)
            row.addStretch()
            val = QLabel("Rs. 0")
            val.setFont(QFont("Segoe UI", 9 if not big else 12, QFont.Bold))
            val.setStyleSheet("color: #0A2540; background: transparent;" if not big else "color: #0A2540; background: transparent;")
            val.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            row.addWidget(val)
            sum_lay.addLayout(row)
            setattr(self, attr_name, val)

        _sum_row("Gross Amount:", "lbl_gross")
        _sum_row("Discount:", "lbl_discount")
        _sum_row("Tax:", "lbl_tax")
        _sum_row("Shipping:", "lbl_shipping")

        # Divider
        div = QFrame()
        div.setFrameShape(QFrame.HLine)
        div.setStyleSheet("color: #C7D7F8; background: #C7D7F8; max-height: 1px;")
        sum_lay.addWidget(div)

        _sum_row("Invoice Amount:", "lbl_grand_total", big=True)
        _sum_row("Total Due:", "lbl_total_due", big=True)

        # Words
        self.lbl_words = QLabel("Zero")
        self.lbl_words.setFont(QFont("Segoe UI", 9, QFont.Bold))
        self.lbl_words.setWordWrap(True)
        self.lbl_words.setStyleSheet(
            "color: #1E3A8A; background: transparent;"
            " border-top: 1px solid #C7D7F8; padding-top: 6px; margin-top: 4px;"
        )
        sum_lay.addWidget(self.lbl_words)

        fin_row.addWidget(sum_frame, 1)
        lay4.addLayout(fin_row)

        # ── Section 5: Notes & Payment (collapsible-style) ─────────────────────
        card5, lay5 = _card("📝  Notes & Payment Terms")
        body_lay.addWidget(card5)

        notes_grid = QGridLayout()
        notes_grid.setSpacing(10)
        notes_grid.setColumnStretch(1, 1)

        notes_grid.addWidget(_field_label("Payment Terms:"), 0, 0, Qt.AlignTop)
        self.edit_payment_terms = QTextEdit()
        self.edit_payment_terms.setPlaceholderText("e.g. Payment due within 15 days")
        self.edit_payment_terms.setMaximumHeight(52)
        self.edit_payment_terms.setStyleSheet(_input_style())
        notes_grid.addWidget(self.edit_payment_terms, 0, 1)

        notes_grid.addWidget(_field_label("Notes:"), 1, 0, Qt.AlignTop)
        self.edit_notes = QTextEdit()
        self.edit_notes.setPlaceholderText("e.g. Thank you for your business!")
        self.edit_notes.setMaximumHeight(52)
        self.edit_notes.setStyleSheet(_input_style())
        notes_grid.addWidget(self.edit_notes, 1, 1)

        lay5.addLayout(notes_grid)

        body_lay.addStretch()
        scroll.setWidget(body_widget)
        vlay.addWidget(scroll, 1)

        # ── Sticky action toolbar ──────────────────────────────────────────────
        toolbar = self._build_action_toolbar()
        toolbar.setMinimumHeight(62)
        vlay.addWidget(toolbar, 0)  # 0 = no stretch, always visible at bottom

        return container

    def _build_action_toolbar(self) -> QWidget:
        bar = QFrame()
        bar.setObjectName("actionBar")
        bar.setStyleSheet(
            "#actionBar {"
            "  background: #FFFFFF;"
            "  border-top: 2px solid #E2E8F0;"
            "}"
        )
        bar.setFixedHeight(62)
        lay = QHBoxLayout(bar)
        lay.setContentsMargins(20, 10, 20, 10)
        lay.setSpacing(10)

        def _btn(text, style_class, slot):
            b = QPushButton(text)
            b.setFixedHeight(38)
            b.setCursor(Qt.PointingHandCursor)
            b.setFont(QFont("Segoe UI", 10, QFont.Bold if "primary" in style_class else QFont.Normal))
            styles = {
                "reset":    ("background: #F1F5F9; color: #64748B; border: 1px solid #CBD5E1;",
                             "background: #E2E8F0;"),
                "draft":    ("background: #FFFFFF; color: #0A2540; border: 1.5px solid #0A2540;",
                             "background: #F0F4FF;"),
                "primary":  ("background: #0A2540; color: white; border: none;",
                             "background: #1E3A8A;"),
                "preview":  ("background: #FFFFFF; color: #C8102E; border: 1.5px solid #C8102E;",
                             "background: #FFF0F0;"),
                "pdf":      ("background: #10B981; color: white; border: none;",
                             "background: #059669;"),
                "print":    ("background: #F59E0B; color: white; border: none;",
                             "background: #D97706;"),
            }
            base, hover = styles.get(style_class, styles["reset"])
            b.setStyleSheet(
                f"QPushButton {{ {base} border-radius: 6px; padding: 4px 18px; }}"
                f"QPushButton:hover {{ {hover} }}"
                f"QPushButton:disabled {{ background: #F1F5F9; color: #94A3B8; border: none; }}"
            )
            b.clicked.connect(slot)
            return b

        self.btn_reset        = _btn("↺  Reset",         "reset",   self.reset_form)
        self.btn_save_draft   = _btn("💾  Save Draft",    "draft",   lambda: self.save_invoice_action("draft"))
        self.btn_save         = _btn("✅  Save Invoice",  "primary", lambda: self.save_invoice_action(self.combo_status.currentText().lower()))
        self.btn_preview      = _btn("👁  Preview",       "preview", self.switch_to_preview)
        self.btn_pdf          = _btn("📄  Generate PDF",  "pdf",     self.generate_pdf_action)
        self.btn_print        = _btn("🖨  Print",         "print",   self.print_action)

        lay.addWidget(self.btn_reset)
        lay.addStretch()
        lay.addWidget(self.btn_save_draft)
        lay.addWidget(self.btn_save)
        lay.addWidget(self.btn_preview)
        lay.addWidget(self.btn_pdf)
        lay.addWidget(self.btn_print)

        return bar

    # ──────────────────────────────────────────────────────────────────────────
    # TAB 2: Preview Invoice
    # ──────────────────────────────────────────────────────────────────────────
    def _build_preview_tab(self) -> QWidget:
        container = QWidget()
        container.setStyleSheet("background: #E8EDF2;")
        vlay = QVBoxLayout(container)
        vlay.setContentsMargins(0, 0, 0, 0)
        vlay.setSpacing(0)

        self.preview_panel = InvoicePreviewWidget()
        vlay.addWidget(self.preview_panel)

        return container

    # ─────────────────────────────────────────────────────────────────────────
    # Data loading
    # ─────────────────────────────────────────────────────────────────────────
    def load_company_data(self):
        session = SessionLocal()
        try:
            company = CompanyRepository.get_company(session)
            if company:
                self.company_data = {
                    "name":                     company.name,
                    "address":                  company.address,
                    "email":                    company.email,
                    "phone":                    company.phone,
                    "logo_path":                company.logo_path,
                    "stamp_path":               company.stamp_path,
                    "signature_path":           company.signature_path,
                    "sales_coordinator_name":   company.sales_coordinator_name,
                    "default_currency":         company.default_currency or "Rs."
                }
        finally:
            session.close()

    def load_customers_dropdown(self):
        session = SessionLocal()
        try:
            customers = CustomerRepository.get_all(session)
            self.combo_customer.blockSignals(True)
            self.combo_customer.clear()
            self.combo_customer.addItem("-- Select or Enter Customer Name --", None)
            for cust in customers:
                display = cust.name
                if cust.city:
                    display += f"  ({cust.city})"
                elif cust.address:
                    display += f"  ({cust.address})"
                self.combo_customer.addItem(display, cust.id)
            self.combo_customer.blockSignals(False)
        finally:
            session.close()

    # ─────────────────────────────────────────────────────────────────────────
    # Customer selection
    # ─────────────────────────────────────────────────────────────────────────
    def on_customer_selected(self, index: int):
        cust_id = self.combo_customer.currentData()
        if not cust_id:
            return
        session = SessionLocal()
        try:
            cust = CustomerRepository.get_by_id(session, cust_id)
            if cust:
                self.edit_delivered_to.setText(cust.name)
                self.edit_invoiced_to.setText("Same")
                self.edit_address.setText(cust.address or cust.city or "")
                self.trigger_live_update()
        finally:
            session.close()

    def open_new_customer_dialog(self):
        dlg = CustomerDialog(self)
        if dlg.exec():
            new_id = dlg.saved_customer_id
            self.load_customers_dropdown()
            for i in range(self.combo_customer.count()):
                if self.combo_customer.itemData(i) == new_id:
                    self.combo_customer.setCurrentIndex(i)
                    break

    # ─────────────────────────────────────────────────────────────────────────
    # Live update / calculations
    # ─────────────────────────────────────────────────────────────────────────
    def trigger_live_update(self):
        invoice_data = self.get_current_form_invoice_data()
        items_data   = self.items_table.get_items_data()

        gross  = invoice_data.get("subtotal",        Decimal("0.00"))
        disc   = invoice_data.get("discount_amount", Decimal("0.00"))
        tax    = invoice_data.get("tax_amount",      Decimal("0.00"))
        ship   = invoice_data.get("shipping_charges",Decimal("0.00"))
        grand  = invoice_data.get("invoice_amount",  Decimal("0.00"))
        due    = invoice_data.get("total_due",       Decimal("0.00"))
        words  = invoice_data.get("amount_in_words", "")
        sym    = self.company_data.get("default_currency", "Rs.")

        def _fmt(v):
            return format_currency(v, symbol=sym)

        self.lbl_gross.setText(_fmt(gross))
        self.lbl_discount.setText(_fmt(disc))
        self.lbl_tax.setText(_fmt(tax))
        self.lbl_shipping.setText(_fmt(ship))
        self.lbl_grand_total.setText(_fmt(grand))
        self.lbl_total_due.setText(_fmt(due))
        self.lbl_words.setText(f"Rupees: {words}" if words else "Rupees: Zero")

        # Update preview canvas
        self.preview_panel.update_preview(invoice_data, items_data, self.company_data)

    def get_current_form_invoice_data(self) -> Dict[str, Any]:
        items_data = self.items_table.get_items_data()
        disc_type  = "percent" if self.combo_disc_type.currentIndex() == 1 else "amount"
        disc_val   = Decimal(str(self.spin_discount.value()))
        tax_val    = Decimal(str(self.spin_tax.value()))
        ship_val   = Decimal(str(self.spin_shipping.value()))

        totals = CalculationService.calculate_invoice_totals(
            items_data,
            discount_type=disc_type,
            discount_value=disc_val,
            tax_rate=tax_val,
            shipping_charges=ship_val,
            currency_name=self.company_data.get("default_currency", "Rupees")
        )

        qdate    = self.date_edit.date()
        inv_date = date(qdate.year(), qdate.month(), qdate.day())

        return {
            "invoice_number":   self.edit_inv_num.text().strip(),
            "manual_no":        self.edit_manual_no.text().strip(),
            "dc_number_1":      self.edit_dc_1.text().strip(),
            "dc_number_2":      self.edit_dc_2.text().strip(),
            "order_number":     self.edit_order_num.text().strip(),
            "invoice_date":     inv_date,
            "delivered_to":     self.edit_delivered_to.text().strip(),
            "invoiced_to":      self.edit_invoiced_to.text().strip(),
            "address":          self.edit_address.text().strip(),
            "dispatch_info":    self.edit_dispatch.text().strip(),
            "customer_id":      self.combo_customer.currentData(),
            "status":           self.combo_status.currentText().lower(),
            "discount_type":    disc_type,
            "discount_value":   disc_val,
            "discount_amount":  totals["discount_amount"],
            "tax_rate":         tax_val,
            "tax_amount":       totals["tax_amount"],
            "shipping_charges": ship_val,
            "other_charges":    Decimal("0.00"),
            "subtotal":         totals["subtotal"],
            "total_amount":     totals["total_amount"],
            "invoice_amount":   totals["invoice_amount"],
            "total_due":        totals["total_due"],
            "paid_amount":      totals["invoice_amount"] if self.combo_status.currentText() == "Paid" else Decimal("0.00"),
            "balance_due":      Decimal("0.00") if self.combo_status.currentText() == "Paid" else totals["invoice_amount"],
            "amount_in_words":  totals["amount_in_words"],
            "is_draft":         (self.combo_status.currentText() == "Draft"),
            "payment_terms":    self.edit_payment_terms.toPlainText().strip(),
            "notes":            self.edit_notes.toPlainText().strip(),
        }

    # ─────────────────────────────────────────────────────────────────────────
    # Action handlers
    # ─────────────────────────────────────────────────────────────────────────
    def save_invoice_action(self, status: str = "paid"):
        invoice_data = self.get_current_form_invoice_data()
        invoice_data["status"]   = status
        invoice_data["is_draft"] = (status == "draft")
        items_data = self.items_table.get_items_data()

        if not invoice_data["delivered_to"]:
            QMessageBox.warning(
                self, "Validation Error",
                "Please enter a customer name in the 'Delivered To' field."
            )
            return

        if not items_data:
            QMessageBox.warning(
                self, "Validation Error",
                "Please add at least one product / line item before saving."
            )
            return

        session = SessionLocal()
        saved_id = None
        save_msg = ""
        save_success = False
        try:
            if self.editing_invoice_id:
                success, inv, msg = InvoiceService.update_invoice(
                    session, self.editing_invoice_id, invoice_data, items_data, generate_pdf=True
                )
            else:
                success, inv, msg = InvoiceService.create_invoice(
                    session, invoice_data, items_data, generate_pdf=True
                )

            if success and inv:
                saved_id = inv.id
                saved_num = inv.invoice_number
                self.editing_invoice_id = inv.id
                self.edit_inv_num.setText(inv.invoice_number)
                if hasattr(self, "lbl_page_title"):
                    self.lbl_page_title.setText(f"Edit Invoice #{inv.invoice_number}")
                save_success = True
            else:
                save_msg = msg
        finally:
            session.close()

        # Emit signal and show toast AFTER session is fully closed
        # so that refresh queries in main_window see committed data
        if save_success:
            ToastNotification.show_toast(
                self.window(),
                f"✅  Invoice #{saved_num} saved successfully!",
                "success"
            )
            self.invoice_saved.emit(saved_id)
        else:
            QMessageBox.critical(self, "Save Error", save_msg)

    def switch_to_preview(self):
        """Switch to Preview tab and auto-fit the canvas."""
        self.trigger_live_update()
        self.tabs.setCurrentIndex(1)
        QTimer.singleShot(80, self.preview_panel.fit_to_width)

    def _on_tab_changed(self, index: int):
        if index == 1:
            self.lbl_page_title.setText(
                f"Preview — Invoice #{self.edit_inv_num.text()}" if self.edit_inv_num.text()
                else "Preview Invoice"
            )
            QTimer.singleShot(80, self.preview_panel.fit_to_width)
        else:
            inv_num = self.edit_inv_num.text()
            if self.editing_invoice_id:
                self.lbl_page_title.setText(f"Edit Invoice #{inv_num}")
            else:
                self.lbl_page_title.setText("New Invoice")

    def generate_pdf_action(self):
        """Generate PDF from current form data (not cached path) and open it."""
        self.trigger_live_update()
        invoice_data = self.get_current_form_invoice_data()
        items_data   = self.items_table.get_items_data()
        # Always regenerate — never use cached path from a previous invoice
        self.preview_panel.last_generated_pdf_path = None
        self.preview_panel.invoice_data  = invoice_data
        self.preview_panel.items_data    = items_data
        self.preview_panel.company_data  = self.company_data
        self.preview_panel.generate_and_open_pdf()

    def print_action(self):
        """Print from current form data (not cached path)."""
        self.trigger_live_update()
        invoice_data = self.get_current_form_invoice_data()
        items_data   = self.items_table.get_items_data()
        # Always regenerate — never use cached path from a previous invoice
        self.preview_panel.last_generated_pdf_path = None
        self.preview_panel.invoice_data  = invoice_data
        self.preview_panel.items_data    = items_data
        self.preview_panel.company_data  = self.company_data
        self.preview_panel.print_invoice()

    def preview_widget_open_pdf(self):
        """Backward-compatible alias used by main_window shortcuts."""
        self.generate_pdf_action()

    # ─────────────────────────────────────────────────────────────────────────
    # Form reset
    # ─────────────────────────────────────────────────────────────────────────
    def reset_form(self):
        self.editing_invoice_id = None
        if hasattr(self, "lbl_page_title"):
            self.lbl_page_title.setText("New Invoice")
        session = SessionLocal()
        try:
            company  = CompanyRepository.get_company(session)
            next_num = company.next_invoice_number if company else 468
            prefix   = company.invoice_prefix      if company else ""
            self.edit_inv_num.setText(format_invoice_number(prefix, next_num))
        finally:
            session.close()

        self.edit_manual_no.clear()
        self.edit_dc_1.clear()
        self.edit_dc_2.clear()
        self.edit_order_num.clear()
        self.date_edit.setDate(QDate.currentDate())
        self.combo_customer.setCurrentIndex(0)
        self.edit_delivered_to.clear()
        self.edit_invoiced_to.setText("Same")
        self.edit_address.clear()
        self.edit_dispatch.clear()
        self.spin_discount.setValue(0.0)
        self.spin_tax.setValue(0.0)
        self.spin_shipping.setValue(0.0)
        self.combo_status.setCurrentText("Paid")
        self.edit_payment_terms.clear()
        self.edit_notes.clear()
        self.items_table.clear_all_rows()
        self.items_table.add_empty_row()
        self.tabs.setCurrentIndex(0)
        self.trigger_live_update()

    # ─────────────────────────────────────────────────────────────────────────
    # Load existing invoice for editing
    # ─────────────────────────────────────────────────────────────────────────
    def load_invoice(self, invoice_id: int):
        session = SessionLocal()
        try:
            inv = InvoiceRepository.get_by_id(session, invoice_id)
            if not inv:
                return

            self.editing_invoice_id = inv.id
            if hasattr(self, "lbl_page_title"):
                self.lbl_page_title.setText(f"Edit Invoice #{inv.invoice_number or invoice_id}")
            self.edit_inv_num.setText(inv.invoice_number or "")
            self.edit_manual_no.setText(inv.manual_no or "")
            self.edit_dc_1.setText(inv.dc_number_1 or "")
            self.edit_dc_2.setText(inv.dc_number_2 or "")
            self.edit_order_num.setText(inv.order_number or "")

            if inv.invoice_date:
                self.date_edit.setDate(
                    QDate(inv.invoice_date.year, inv.invoice_date.month, inv.invoice_date.day)
                )

            # Match customer in combo
            self.combo_customer.blockSignals(True)
            if inv.customer_id:
                for i in range(self.combo_customer.count()):
                    if self.combo_customer.itemData(i) == inv.customer_id:
                        self.combo_customer.setCurrentIndex(i)
                        break
            else:
                self.combo_customer.setCurrentIndex(0)
            self.combo_customer.blockSignals(False)

            self.edit_delivered_to.setText(inv.delivered_to or "")
            self.edit_invoiced_to.setText(inv.invoiced_to or "Same")
            self.edit_address.setText(inv.address or "")
            self.edit_dispatch.setText(inv.dispatch_info or "")

            self.combo_disc_type.setCurrentIndex(1 if inv.discount_type == "percent" else 0)
            self.spin_discount.setValue(float(inv.discount_value or 0.0))
            self.spin_tax.setValue(float(inv.tax_rate or 0.0))
            self.spin_shipping.setValue(float(inv.shipping_charges or 0.0))

            status_str = (inv.status or "paid").capitalize()
            self.combo_status.setCurrentText(status_str)

            if hasattr(inv, "payment_terms") and inv.payment_terms:
                self.edit_payment_terms.setPlainText(inv.payment_terms)
            if hasattr(inv, "notes") and inv.notes:
                self.edit_notes.setPlainText(inv.notes)

            # Load line items
            items_list = []
            for itm in inv.items:
                items_list.append({
                    "serial_no":       itm.serial_no,
                    "product_name":    itm.product_name,
                    "packing":         itm.packing,
                    "quantity_value":  itm.quantity_value,
                    "quantity_unit":   itm.quantity_unit,
                    "billing_quantity": itm.billing_quantity,
                    "bonus":           itm.bonus,
                    "unit_rate":       itm.unit_rate,
                    "amount":          itm.amount,
                })
            self.items_table.set_items_data(items_list)
            self.tabs.setCurrentIndex(0)
            self.trigger_live_update()

        finally:
            session.close()
