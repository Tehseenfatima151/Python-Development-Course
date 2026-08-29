"""
Custom UI Cards and Badges for InvoicePro
Provides modern metric KPI cards, rounded panels, and status badges.
"""
from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor
from app.config import (
    COLOR_NAVY_PRIMARY, COLOR_NAVY_DARK, COLOR_RED_ACCENT, COLOR_BG_CARD,
    COLOR_TEXT_PRIMARY, COLOR_TEXT_SECONDARY, COLOR_SUCCESS, COLOR_WARNING, COLOR_DANGER
)


class CardPanel(QFrame):
    """Clean modern card container."""
    def __init__(self, title: str = "", subtitle: str = "", parent=None):
        super().__init__(parent)
        self.setProperty("class", "card-panel")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(18, 18, 18, 18)
        self.layout.setSpacing(12)

        if title:
            header_layout = QVBoxLayout()
            header_layout.setSpacing(2)
            
            lbl_title = QLabel(title)
            lbl_title.setProperty("class", "card-title")
            lbl_title.setFont(QFont("Segoe UI", 12, QFont.Bold))
            header_layout.addWidget(lbl_title)

            if subtitle:
                lbl_sub = QLabel(subtitle)
                lbl_sub.setProperty("class", "card-subtitle")
                header_layout.addWidget(lbl_sub)

            self.layout.addLayout(header_layout)


class MetricCard(QFrame):
    """Dashboard KPI Metric Card."""
    def __init__(self, title: str, value: str, icon_str: str = "", subtitle: str = "", accent_color: str = COLOR_NAVY_PRIMARY, parent=None):
        super().__init__(parent)
        self.setProperty("class", "card-panel")
        self.setFixedHeight(110)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 14, 16, 14)
        main_layout.setSpacing(4)

        # Top row: Title and Icon
        top_layout = QHBoxLayout()
        lbl_title = QLabel(title.upper())
        lbl_title.setFont(QFont("Segoe UI", 9, QFont.Bold))
        lbl_title.setStyleSheet("color: #64748B; letter-spacing: 0.5px;")
        top_layout.addWidget(lbl_title)

        if icon_str:
            lbl_icon = QLabel(icon_str)
            lbl_icon.setFont(QFont("Segoe UI", 14))
            lbl_icon.setStyleSheet(f"color: {accent_color};")
            top_layout.addWidget(lbl_icon, 0, Qt.AlignRight)

        main_layout.addLayout(top_layout)

        # Value
        self.lbl_value = QLabel(value)
        self.lbl_value.setFont(QFont("Segoe UI", 18, QFont.Bold))
        self.lbl_value.setStyleSheet(f"color: {accent_color};")
        main_layout.addWidget(self.lbl_value)

        # Subtitle / trend
        if subtitle:
            lbl_sub = QLabel(subtitle)
            lbl_sub.setFont(QFont("Segoe UI", 8))
            lbl_sub.setStyleSheet("color: #94A3B8;")
            main_layout.addWidget(lbl_sub)
        else:
            main_layout.addStretch()

    def update_value(self, new_val: str):
        self.lbl_value.setText(new_val)


class StatusBadge(QLabel):
    """Pill badge for invoice status."""
    def __init__(self, status: str = "paid", parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self.setFixedHeight(26)
        self.setMinimumWidth(72)
        self.set_status(status)

    def set_status(self, status: str):
        status_clean = (status or "draft").lower()
        labels = {
            "paid": "Paid", "pending": "Pending", "sent": "Sent",
            "overdue": "Overdue", "draft": "Draft", "cancelled": "Cancelled"
        }
        self.setText(labels.get(status_clean, status_clean.capitalize()))
        
        styles = {
            "paid":      "background-color:#DCFCE7; color:#15803D; border:1.5px solid #86EFAC;",
            "pending":   "background-color:#FEF3C7; color:#B45309; border:1.5px solid #FCD34D;",
            "sent":      "background-color:#DBEAFE; color:#1D4ED8; border:1.5px solid #93C5FD;",
            "overdue":   "background-color:#FEE2E2; color:#B91C1C; border:1.5px solid #FCA5A5;",
            "draft":     "background-color:#F1F5F9; color:#475569; border:1.5px solid #CBD5E1;",
            "cancelled": "background-color:#F3F4F6; color:#6B7280; border:1.5px solid #D1D5DB;",
        }
        base = styles.get(status_clean, styles["draft"])
        self.setStyleSheet(
            f"QLabel {{ {base} font-weight:700; font-size:11px;"
            " border-radius:13px; padding:3px 14px; min-width:72px; }}"
        )
        self.adjustSize()
