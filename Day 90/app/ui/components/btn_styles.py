"""
Shared button style helpers for InvoicePro.
Use these instead of setProperty("class", ...) which is unreliable in PySide6.
"""

BTN_PRIMARY = """
QPushButton {
    background-color: #0A2540;
    color: #FFFFFF;
    font-size: 13px;
    font-weight: 600;
    border: none;
    border-radius: 6px;
    padding: 7px 18px;
}
QPushButton:hover   { background-color: #1E3A8A; }
QPushButton:pressed { background-color: #002D62; }
QPushButton:disabled { background-color: #94A3B8; color: #FFFFFF; }
"""

BTN_SECONDARY = """
QPushButton {
    background-color: #FFFFFF;
    color: #334155;
    font-size: 13px;
    font-weight: 500;
    border: 1px solid #CBD5E1;
    border-radius: 6px;
    padding: 7px 16px;
}
QPushButton:hover   { background-color: #F1F5F9; border-color: #94A3B8; color: #0A2540; }
QPushButton:pressed { background-color: #E2E8F0; }
QPushButton:disabled { background-color: #F8FAFC; color: #CBD5E1; border-color: #E2E8F0; }
"""

BTN_DANGER = """
QPushButton {
    background-color: #C8102E;
    color: #FFFFFF;
    font-size: 13px;
    font-weight: 600;
    border: none;
    border-radius: 6px;
    padding: 7px 18px;
}
QPushButton:hover   { background-color: #A50D24; }
QPushButton:pressed { background-color: #880B1D; }
"""

BTN_SUCCESS = """
QPushButton {
    background-color: #10B981;
    color: #FFFFFF;
    font-size: 13px;
    font-weight: 600;
    border: none;
    border-radius: 6px;
    padding: 7px 18px;
}
QPushButton:hover   { background-color: #059669; }
QPushButton:pressed { background-color: #047857; }
"""

BTN_ACTION_DROPDOWN = """
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
"""


def apply_primary(btn):
    btn.setStyleSheet(BTN_PRIMARY)


def apply_secondary(btn):
    btn.setStyleSheet(BTN_SECONDARY)


def apply_danger(btn):
    btn.setStyleSheet(BTN_DANGER)


def apply_success(btn):
    btn.setStyleSheet(BTN_SUCCESS)
