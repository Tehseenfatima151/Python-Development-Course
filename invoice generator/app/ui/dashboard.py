"""
Dashboard Screen for InvoicePro
Displays high-level KPI cards, quick actions, and recent invoices.
"""
from decimal import Decimal

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QFrame, QScrollArea,
    QSizePolicy, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QColor, QLinearGradient, QPalette, QPainter

from app.database.db import SessionLocal
from app.database.repositories import InvoiceRepository, CompanyRepository
from app.utils.formatters import format_currency, format_date
from app.utils.helpers import open_file_in_system_viewer
from app.ui.components.cards import CardPanel
from app.ui.components.badges import StatusBadge
from app.config import COLOR_NAVY_PRIMARY, COLOR_NAVY_DARK, COLOR_SUCCESS, COLOR_WARNING
from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QAction


# Shared action button style — compact size
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
QPushButton:hover   { background-color: #1E3A8A; }
QPushButton:pressed { background-color: #002D62; }
"""


# ── Colorful KPI Card ─────────────────────────────────────────────────────────
class KPICard(QFrame):
    """
    Professional gradient KPI card with icon, title, value and subtitle.
    Each card has its own accent color scheme.
    """
    def __init__(self, title: str, value: str, icon: str,
                 subtitle: str, grad_start: str, grad_end: str,
                 parent=None):
        super().__init__(parent)
        self._grad_start = grad_start
        self._grad_end   = grad_end

        self.setFixedHeight(120)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setStyleSheet(f"""
            KPICard {{
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 {grad_start}, stop:1 {grad_end}
                );
                border-radius: 14px;
                border: none;
            }}
        """)

        # Drop shadow
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(18)
        shadow.setOffset(0, 4)
        shadow.setColor(QColor(0, 0, 0, 45))
        self.setGraphicsEffect(shadow)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(20, 16, 20, 14)
        lay.setSpacing(4)

        # Top row: icon + title
        top = QHBoxLayout()
        top.setSpacing(10)

        lbl_icon = QLabel(icon)
        lbl_icon.setFont(QFont("Segoe UI", 22))
        lbl_icon.setStyleSheet("color: rgba(255,255,255,0.90); background: transparent;")
        lbl_icon.setFixedWidth(36)
        top.addWidget(lbl_icon)

        lbl_title = QLabel(title.upper())
        lbl_title.setFont(QFont("Segoe UI", 9, QFont.Bold))
        lbl_title.setStyleSheet(
            "color: rgba(255,255,255,0.85); background: transparent;"
            " letter-spacing: 1px;"
        )
        top.addWidget(lbl_title)
        top.addStretch()
        lay.addLayout(top)

        # Value (big number)
        self.lbl_value = QLabel(value)
        self.lbl_value.setFont(QFont("Segoe UI", 22, QFont.Bold))
        self.lbl_value.setStyleSheet("color: #FFFFFF; background: transparent;")
        lay.addWidget(self.lbl_value)

        # Subtitle
        lbl_sub = QLabel(subtitle)
        lbl_sub.setFont(QFont("Segoe UI", 9))
        lbl_sub.setStyleSheet("color: rgba(255,255,255,0.70); background: transparent;")
        lay.addWidget(lbl_sub)

    def update_value(self, val: str):
        self.lbl_value.setText(val)


class DashboardWidget(QWidget):
    navigate_requested = Signal(str, object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        # Outer scroll area so the page scrolls if window is small
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("background: transparent; border: none;")

        container = QWidget()
        container.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(28, 24, 28, 28)
        layout.setSpacing(22)

        # ── 1. Page Header ───────────────────────────────────────────────────
        header_row = QHBoxLayout()
        header_row.setSpacing(0)

        title_col = QVBoxLayout()
        title_col.setSpacing(4)

        lbl_title = QLabel("Dashboard")
        lbl_title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        lbl_title.setStyleSheet("color: #0A2540;")
        title_col.addWidget(lbl_title)

        lbl_sub = QLabel("Overview of your billing activity and revenue")
        lbl_sub.setFont(QFont("Segoe UI", 11))
        lbl_sub.setStyleSheet("color: #64748B;")
        title_col.addWidget(lbl_sub)

        header_row.addLayout(title_col)
        header_row.addStretch()

        btn_new = QPushButton("＋  New Invoice")
        btn_new.setFont(QFont("Segoe UI", 11, QFont.Bold))
        btn_new.setFixedHeight(40)
        btn_new.setMinimumWidth(160)
        btn_new.setCursor(Qt.PointingHandCursor)
        btn_new.setStyleSheet("""
            QPushButton { background-color:#0A2540; color:#FFFFFF; font-weight:600;
                border:none; border-radius:6px; padding:8px 20px; }
            QPushButton:hover   { background-color:#1E3A8A; }
            QPushButton:pressed { background-color:#002D62; }
        """)
        btn_new.clicked.connect(lambda: self.navigate_requested.emit("new_invoice", None))
        header_row.addWidget(btn_new)

        layout.addLayout(header_row)

        # ── 2. KPI Cards ─────────────────────────────────────────────────────
        cards_row = QHBoxLayout()
        cards_row.setSpacing(14)

        # 5 colorful gradient cards — each a distinct professional color
        self.card_total_rev = KPICard(
            "Total Revenue", "Rs. 0", "💰",
            "Lifetime billed",
            "#1A56DB", "#0A2540"          # Deep navy → darker navy
        )
        self.card_month_rev = KPICard(
            "This Month", "Rs. 0", "📈",
            "Current calendar month",
            "#7C3AED", "#4C1D95"          # Purple
        )
        self.card_total_inv = KPICard(
            "Total Invoices", "0", "📄",
            "All invoices created",
            "#0891B2", "#155E75"          # Cyan / teal
        )
        self.card_paid_inv = KPICard(
            "Paid Invoices", "0", "✅",
            "Fully settled",
            "#059669", "#064E3B"          # Green
        )
        self.card_pending_inv = KPICard(
            "Pending / Unpaid", "0", "⏳",
            "Action required",
            "#D97706", "#92400E"          # Amber / orange
        )

        for card in [self.card_total_rev, self.card_month_rev, self.card_total_inv,
                     self.card_paid_inv, self.card_pending_inv]:
            cards_row.addWidget(card)

        layout.addLayout(cards_row)

        # ── 3. Quick Actions ─────────────────────────────────────────────────
        actions_panel = CardPanel("Quick Actions", "Frequently used invoicing workflows")
        actions_row = QHBoxLayout()
        actions_row.setSpacing(10)

        quick_btns = [
            ("📄  All Invoices",     "invoices"),
            ("👥  Manage Customers", "customers"),
            ("🏢  Company Profile",  "company"),
            ("💾  Backup & Restore", "backup"),
        ]
        for label, target in quick_btns:
            b = QPushButton(label)
            b.setFixedHeight(36)
            b.setCursor(Qt.PointingHandCursor)
            b.setStyleSheet("""
                QPushButton { background-color:#FFFFFF; color:#334155; font-size:13px;
                    font-weight:500; border:1px solid #CBD5E1; border-radius:6px; padding:6px 16px; }
                QPushButton:hover   { background-color:#F1F5F9; border-color:#94A3B8; color:#0A2540; }
                QPushButton:pressed { background-color:#E2E8F0; }
            """)
            b.clicked.connect(lambda checked=False, t=target: self.navigate_requested.emit(t, None))
            actions_row.addWidget(b)

        actions_row.addStretch()
        actions_panel.layout.addLayout(actions_row)
        layout.addWidget(actions_panel)

        # ── 4. Recent Invoices ───────────────────────────────────────────────
        recent_panel = CardPanel("Recent Invoices", "Latest billing transactions")

        self.table_recent = QTableWidget()
        self.table_recent.setColumnCount(7)
        self.table_recent.setHorizontalHeaderLabels(
            ["Invoice #", "Book No", "Customer / Delivered To", "Date", "Amount (Rs.)", "Status", "Actions"]
        )
        self.table_recent.verticalHeader().setVisible(False)
        self.table_recent.setAlternatingRowColors(True)
        self.table_recent.setSelectionMode(QTableWidget.NoSelection)
        self.table_recent.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table_recent.setShowGrid(False)
        self.table_recent.setFocusPolicy(Qt.NoFocus)

        hdr = self.table_recent.horizontalHeader()
        hdr.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        hdr.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        hdr.setSectionResizeMode(2, QHeaderView.Stretch)
        hdr.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        hdr.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        hdr.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        hdr.setSectionResizeMode(6, QHeaderView.Fixed)
        self.table_recent.setColumnWidth(6, 88)
        self.table_recent.verticalHeader().setDefaultSectionSize(38)

        recent_panel.layout.addWidget(self.table_recent)
        layout.addWidget(recent_panel)

        layout.addStretch()

        scroll.setWidget(container)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.addWidget(scroll)

    # ── Data refresh ─────────────────────────────────────────────────────────
    def refresh_data(self):
        session = SessionLocal()
        try:
            metrics = InvoiceRepository.get_dashboard_metrics(session)

            self.card_total_rev.update_value(format_currency(metrics["total_revenue"],       symbol="Rs."))
            self.card_month_rev.update_value(format_currency(metrics["this_month_revenue"],  symbol="Rs."))
            self.card_total_inv.update_value(str(metrics["total_invoices"]))
            self.card_paid_inv.update_value(str(metrics["paid_invoices"]))
            self.card_pending_inv.update_value(str(metrics["pending_invoices"]))

            recent = metrics["recent_invoices"]
            self.table_recent.setRowCount(len(recent))

            for r, inv in enumerate(recent):
                # Invoice #
                it0 = QTableWidgetItem(inv.invoice_number or "")
                it0.setFont(QFont("Segoe UI", 9, QFont.Bold))
                self.table_recent.setItem(r, 0, it0)

                # Book No
                self.table_recent.setItem(r, 1, QTableWidgetItem(inv.manual_no or ""))

                # Customer
                cust_name = inv.delivered_to or (inv.customer.name if inv.customer else "")
                self.table_recent.setItem(r, 2, QTableWidgetItem(cust_name))

                # Date
                self.table_recent.setItem(r, 3, QTableWidgetItem(format_date(inv.invoice_date)))

                # Amount
                it4 = QTableWidgetItem(format_currency(inv.invoice_amount, decimals=0))
                it4.setFont(QFont("Segoe UI", 9, QFont.Bold))
                it4.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.table_recent.setItem(r, 4, it4)

                # Status badge
                badge = StatusBadge(inv.status or "paid")
                self.table_recent.setCellWidget(r, 5, badge)

                # Single dropdown action button
                btn = QPushButton("Actions ▾")
                btn.setFixedHeight(28)
                btn.setStyleSheet(_ACTION_BTN_STYLE)
                btn.setCursor(Qt.PointingHandCursor)
                inv_id   = inv.id
                pdf_path = inv.pdf_path
                btn.clicked.connect(
                    lambda checked=False, iid=inv_id, p=pdf_path, b=btn:
                    self._show_invoice_menu(iid, p, b)
                )
                self.table_recent.setCellWidget(r, 6, btn)

        finally:
            session.close()

    def _show_invoice_menu(self, invoice_id: int, pdf_path, button: QPushButton):
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu { background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 6px; padding: 4px 0; }
            QMenu::item { padding: 8px 20px; font-size: 13px; color: #0F172A; }
            QMenu::item:selected { background: #F1F5F9; color: #0A2540; }
            QMenu::separator { height: 1px; background: #E2E8F0; margin: 3px 0; }
        """)

        act_edit = QAction("✏  Edit Invoice", self)
        act_edit.triggered.connect(
            lambda: self.navigate_requested.emit("edit_invoice", invoice_id)
        )
        menu.addAction(act_edit)

        act_pdf = QAction("📄  Open PDF", self)
        act_pdf.triggered.connect(
            lambda: open_file_in_system_viewer(pdf_path) if pdf_path else None
        )
        menu.addAction(act_pdf)

        menu.exec(button.mapToGlobal(button.rect().bottomLeft()))
