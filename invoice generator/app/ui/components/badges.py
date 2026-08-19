"""
Status Badge UI Component for InvoicePro
Renders modern, rounded status badge pills for invoice statuses.
"""
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class StatusBadge(QLabel):
    STATUS_STYLES = {
        "paid": {
            "bg": "#DCFCE7",
            "text": "#15803D",
            "border": "#86EFAC",
            "label": "Paid"
        },
        "pending": {
            "bg": "#FEF3C7",
            "text": "#B45309",
            "border": "#FCD34D",
            "label": "Pending"
        },
        "draft": {
            "bg": "#F1F5F9",
            "text": "#475569",
            "border": "#CBD5E1",
            "label": "Draft"
        },
        "sent": {
            "bg": "#DBEAFE",
            "text": "#1D4ED8",
            "border": "#93C5FD",
            "label": "Sent"
        },
        "overdue": {
            "bg": "#FEE2E2",
            "text": "#B91C1C",
            "border": "#FCA5A5",
            "label": "Overdue"
        },
        "cancelled": {
            "bg": "#F3F4F6",
            "text": "#6B7280",
            "border": "#D1D5DB",
            "label": "Cancelled"
        }
    }

    def __init__(self, status: str = "draft", parent=None):
        super().__init__(parent)
        self.setFont(QFont("Segoe UI", 9, QFont.Bold))
        self.setAlignment(Qt.AlignCenter)
        # Fixed height + enough minimum width so no text gets clipped
        self.setFixedHeight(26)
        self.setMinimumWidth(72)
        self.set_status(status)

    def set_status(self, status: str):
        status_key = (status or "draft").lower()
        cfg = self.STATUS_STYLES.get(status_key, self.STATUS_STYLES["draft"])
        self.setText(cfg["label"])
        self.setStyleSheet(f"""
            QLabel {{
                background-color: {cfg["bg"]};
                color: {cfg["text"]};
                border: 1.5px solid {cfg["border"]};
                border-radius: 13px;
                padding: 3px 14px;
                font-weight: 700;
                font-size: 11px;
                min-width: 72px;
            }}
        """)
        # Ensure widget resizes to fit text
        self.adjustSize()
