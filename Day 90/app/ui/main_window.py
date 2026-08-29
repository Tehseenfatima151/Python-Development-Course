"""
Main Application Window for InvoicePro
Implements modern sidebar navigation, page routing, keyboard shortcuts, and global notifications.
"""
import os
import sys
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton,
    QLabel, QStackedWidget, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QKeySequence, QShortcut, QPixmap, QBitmap, QPainter, QBrush, QColor

from app.config import APP_NAME, APP_SUBTITLE, APP_VERSION
from app.database.db import SessionLocal
from app.database.repositories import CompanyRepository
from app.ui.dashboard import DashboardWidget
from app.ui.invoice_form import InvoiceFormWidget
from app.ui.invoice_history import InvoiceHistoryWidget
from app.ui.customer_management import CustomerManagementWidget
from app.ui.company_settings import CompanySettingsWidget
from app.ui.backup_restore import BackupRestoreWidget
from app.ui.about_dialog import AboutDialog


# Shared nav button style applied directly (PySide6 class-property QSS is unreliable)
NAV_BTN_NORMAL = """
    QPushButton {
        background-color: transparent;
        color: #B0BCCC;
        text-align: left;
        padding: 10px 16px 10px 16px;
        font-size: 13px;
        font-weight: 500;
        border: none;
        border-radius: 8px;
        margin: 1px 8px;
    }
    QPushButton:hover {
        background-color: rgba(255, 255, 255, 0.10);
        color: #FFFFFF;
    }
"""

NAV_BTN_ACTIVE = """
    QPushButton {
        background-color: #C8102E;
        color: #FFFFFF;
        text-align: left;
        padding: 10px 16px 10px 16px;
        font-size: 13px;
        font-weight: 700;
        border: none;
        border-radius: 8px;
        margin: 1px 8px;
    }
    QPushButton:hover {
        background-color: #A50D24;
        color: #FFFFFF;
    }
"""


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} — {APP_SUBTITLE} v{APP_VERSION}")
        self.resize(1280, 820)
        self.setMinimumSize(1024, 680)

        self.setup_ui()
        self.setup_shortcuts()

    def setup_ui(self):
        central_widget = QWidget(self)
        central_widget.setObjectName("centralWidget")
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ─────────────────────────────────────────────────────────────
        # SIDEBAR — Dark Navy
        # ─────────────────────────────────────────────────────────────
        self.sidebar = QWidget()
        self.sidebar.setObjectName("sidebarWidget")
        self.sidebar.setFixedWidth(232)
        # Apply sidebar background directly so it always renders correctly
        self.sidebar.setStyleSheet("""
            QWidget#sidebarWidget {
                background-color: #0A2540;
                border-right: 1px solid #071C33;
            }
        """)

        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 20)
        sidebar_layout.setSpacing(4)

        # ── Brand / Logo area ────────────────────────────────────────
        brand_frame = QWidget()
        brand_frame.setStyleSheet("background: transparent;")
        brand_lay = QHBoxLayout(brand_frame)
        brand_lay.setContentsMargins(14, 14, 14, 14)
        brand_lay.setSpacing(12)
        brand_lay.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        # Company logo (circular, from DB)
        self.lbl_logo = QLabel()
        self.lbl_logo.setFixedSize(46, 46)
        self.lbl_logo.setAlignment(Qt.AlignCenter)
        self.lbl_logo.setStyleSheet(
            "background: rgba(255,255,255,0.12);"
            " border-radius: 23px;"
            " border: 2px solid rgba(255,255,255,0.25);"
        )
        self._load_sidebar_logo()
        brand_lay.addWidget(self.lbl_logo)

        # App name + subtitle
        title_col = QVBoxLayout()
        title_col.setSpacing(2)

        lbl_brand = QLabel(APP_NAME)
        lbl_brand.setFont(QFont("Segoe UI", 15, QFont.Bold))
        lbl_brand.setStyleSheet("color: #FFFFFF; background: transparent;")
        lbl_brand.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        title_col.addWidget(lbl_brand)

        lbl_sub = QLabel("Professional Billing")
        lbl_sub.setFont(QFont("Segoe UI", 9))
        lbl_sub.setStyleSheet("color: #94A3B8; background: transparent;")
        lbl_sub.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        title_col.addWidget(lbl_sub)

        brand_lay.addLayout(title_col)
        sidebar_layout.addWidget(brand_frame)

        # ── Thin separator ───────────────────────────────────────────
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setFixedHeight(1)
        sep.setStyleSheet("background-color: #1E3A5F; border: none;")
        sidebar_layout.addWidget(sep)
        sidebar_layout.addSpacing(6)

        # ── Navigation items ─────────────────────────────────────────
        self.nav_buttons = []
        nav_items = [
            ("📊   Dashboard",          0),
            ("➕   New Invoice",         1),
            ("📋   Invoices",            2),
            ("👥   Customers",           3),
            ("🏢   Company Profile",     4),
            ("💾   Backup & Restore",    5),
        ]

        for text, page_idx in nav_items:
            btn = QPushButton(text)
            btn.setFixedHeight(44)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet(NAV_BTN_NORMAL)
            btn.clicked.connect(lambda checked=False, idx=page_idx: self.switch_page(idx))
            sidebar_layout.addWidget(btn)
            self.nav_buttons.append(btn)

        sidebar_layout.addStretch()

        # ── About button at bottom ───────────────────────────────────
        sep2 = QFrame()
        sep2.setFrameShape(QFrame.HLine)
        sep2.setFixedHeight(1)
        sep2.setStyleSheet("background-color: #1E3A5F; border: none;")
        sidebar_layout.addWidget(sep2)
        sidebar_layout.addSpacing(6)

        btn_about = QPushButton("ℹ   About InvoicePro")
        btn_about.setFixedHeight(40)
        btn_about.setCursor(Qt.PointingHandCursor)
        btn_about.setStyleSheet(NAV_BTN_NORMAL)
        btn_about.clicked.connect(self.show_about_dialog)
        sidebar_layout.addWidget(btn_about)

        main_layout.addWidget(self.sidebar)

        # ─────────────────────────────────────────────────────────────
        # MAIN CONTENT AREA — Stacked pages
        # ─────────────────────────────────────────────────────────────
        self.pages = QStackedWidget()
        self.pages.setStyleSheet("background-color: #F8FAFC;")

        self.page_dashboard = DashboardWidget()
        self.page_dashboard.navigate_requested.connect(self.handle_navigation_request)
        self.pages.addWidget(self.page_dashboard)          # Index 0

        self.page_invoice_form = InvoiceFormWidget()
        self.page_invoice_form.invoice_saved.connect(self.on_invoice_saved)
        self.pages.addWidget(self.page_invoice_form)       # Index 1

        self.page_invoice_history = InvoiceHistoryWidget()
        self.page_invoice_history.navigate_requested.connect(self.handle_navigation_request)
        self.pages.addWidget(self.page_invoice_history)    # Index 2

        self.page_customers = CustomerManagementWidget()
        self.page_customers.navigate_requested.connect(self.handle_navigation_request)
        self.pages.addWidget(self.page_customers)          # Index 3

        self.page_company = CompanySettingsWidget()
        self.page_company.settings_saved.connect(self.on_company_settings_saved)
        self.pages.addWidget(self.page_company)            # Index 4

        self.page_backup = BackupRestoreWidget()
        self.pages.addWidget(self.page_backup)             # Index 5

        main_layout.addWidget(self.pages)

        # Activate Dashboard by default
        self.switch_page(0)

    def switch_page(self, page_index: int):
        self.pages.setCurrentIndex(page_index)

        # Update nav button styling
        for i, btn in enumerate(self.nav_buttons):
            if i == page_index:
                btn.setStyleSheet(NAV_BTN_ACTIVE)
            else:
                btn.setStyleSheet(NAV_BTN_NORMAL)

        # Refresh page data on switch
        if page_index == 0:
            self.page_dashboard.refresh_data()
        elif page_index == 2:
            self.page_invoice_history.load_invoices()
        elif page_index == 3:
            self.page_customers.load_customers()
        elif page_index == 4:
            self.page_company.load_settings()

    def handle_navigation_request(self, target: str, payload: object):
        if target == "new_invoice":
            self.page_invoice_form.reset_form()
            self.switch_page(1)
        elif target == "edit_invoice":
            if isinstance(payload, int):
                self.page_invoice_form.load_invoice(payload)
                self.switch_page(1)
        elif target == "new_invoice_for_customer":
            if isinstance(payload, int):
                self.page_invoice_form.reset_form()
                for i in range(self.page_invoice_form.combo_customer.count()):
                    if self.page_invoice_form.combo_customer.itemData(i) == payload:
                        self.page_invoice_form.combo_customer.setCurrentIndex(i)
                        break
                self.switch_page(1)
        elif target == "invoices":
            self.switch_page(2)
        elif target == "customers":
            self.switch_page(3)
        elif target == "company":
            self.switch_page(4)
        elif target == "backup":
            self.switch_page(5)

    def on_invoice_saved(self, invoice_id: int):
        self.page_dashboard.refresh_data()
        self.page_invoice_history.load_invoices()

    def on_company_settings_saved(self):
        self.page_invoice_form.load_company_data()
        self.page_dashboard.refresh_data()
        self._load_sidebar_logo()  # Refresh logo when company settings change

    def _load_sidebar_logo(self):
        """Load company logo into the sidebar circle, falling back to a clean icon."""
        session = SessionLocal()
        try:
            company = CompanyRepository.get_company(session)
            logo_path = company.logo_path if company else None
        finally:
            session.close()

        if logo_path and os.path.exists(logo_path):
            try:
                pix = QPixmap(logo_path)
                if not pix.isNull():
                    circular = self._make_circular_pixmap(pix, 42)
                    self.lbl_logo.setPixmap(circular)
                    self.lbl_logo.setText("")
                    self.lbl_logo.setStyleSheet(
                        "background: transparent;"
                        " border-radius: 23px;"
                        " border: 2px solid rgba(255,255,255,0.30);"
                    )
                    return
            except Exception:
                pass

        # Fallback: clean invoice icon on a red accent circle
        self.lbl_logo.clear()
        self.lbl_logo.setText("🧾")
        self.lbl_logo.setFont(QFont("Segoe UI", 22))
        self.lbl_logo.setAlignment(Qt.AlignCenter)
        self.lbl_logo.setStyleSheet(
            "color: #FFFFFF;"
            " background: #C8102E;"
            " border-radius: 23px;"
            " border: none;"
        )

    @staticmethod
    def _make_circular_pixmap(source: QPixmap, size: int) -> QPixmap:
        """Crop a pixmap into a circle of the given size."""
        scaled = source.scaled(
            size, size,
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation
        )
        # Crop to square from center
        x = (scaled.width()  - size) // 2
        y = (scaled.height() - size) // 2
        scaled = scaled.copy(x, y, size, size)

        # Apply circular mask
        result = QPixmap(size, size)
        result.fill(Qt.transparent)
        painter = QPainter(result)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(scaled))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, size, size)
        painter.end()
        return result

    def show_about_dialog(self):
        dlg = AboutDialog(self)
        dlg.exec()

    def setup_shortcuts(self):
        QShortcut(QKeySequence("Ctrl+N"), self,
                  lambda: self.handle_navigation_request("new_invoice", None))
        QShortcut(QKeySequence("Ctrl+S"), self,
                  lambda: self.page_invoice_form.save_invoice_action("paid")
                  if self.pages.currentIndex() == 1 else None)
        QShortcut(QKeySequence("Ctrl+P"), self,
                  lambda: self.page_invoice_form.preview_panel.print_invoice()
                  if self.pages.currentIndex() == 1 else None)
        QShortcut(QKeySequence("Ctrl+F"), self, lambda: self.switch_page(2))
        QShortcut(QKeySequence("Ctrl+Q"), self, self.close)
