import os
import sys
from pathlib import Path

if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys._MEIPASS)
    APP_DATA_DIR = Path(os.path.dirname(sys.executable))
else:
    BASE_DIR = Path(__file__).resolve().parent.parent
    APP_DATA_DIR = BASE_DIR

DATA_DIR = APP_DATA_DIR / 'data'
EXPORT_DIR = APP_DATA_DIR / 'exports'
BACKUP_DIR = APP_DATA_DIR / 'backups'
LOG_DIR = APP_DATA_DIR / 'logs'
ASSETS_DIR = BASE_DIR / 'app' / 'resources' / 'assets'
STYLES_DIR = BASE_DIR / 'app' / 'resources' / 'styles'

for directory in [DATA_DIR, EXPORT_DIR, BACKUP_DIR, LOG_DIR, ASSETS_DIR, STYLES_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

DATABASE_URL = f"sqlite:///{DATA_DIR / 'invoicepro.db'}"
LOG_FILE = LOG_DIR / 'app.log'

APP_NAME = "InvoicePro"
APP_SUBTITLE = "Professional Invoice Generator"
APP_VERSION = "1.0.0"
ORGANIZATION_NAME = "InvoicePro"

COLOR_NAVY_PRIMARY = "#0A2540"
COLOR_NAVY_DARK = "#002D62"
COLOR_NAVY_LIGHT = "#1E3A8A"
COLOR_RED_ACCENT = "#C8102E"
COLOR_RED_HOVER = "#A50D24"
COLOR_BG_MAIN = "#F8FAFC"
COLOR_BG_CARD = "#FFFFFF"
COLOR_BG_SIDEBAR = "#0A2540"
COLOR_TEXT_PRIMARY = "#0F172A"
COLOR_TEXT_SECONDARY = "#64748B"
COLOR_TEXT_MUTED = "#94A3B8"
COLOR_BORDER = "#E2E8F0"
COLOR_BORDER_FOCUS = "#0A2540"
COLOR_SUCCESS = "#10B981"
COLOR_WARNING = "#F59E0B"
COLOR_DANGER = "#EF4444"
COLOR_INFO = "#3B82F6"

DEFAULT_CURRENCY = "Rs."
DEFAULT_CURRENCY_CODE = "PKR"
DEFAULT_TAX_RATE = 0.0
DEFAULT_INVOICE_PREFIX = "INV-"
DEFAULT_STARTING_NUMBER = 468
DEFAULT_DATE_FORMAT = "%d-%m-%Y"
DEFAULT_PAYMENT_TERMS = "Payment is due within 15 days from the date of invoice."
DEFAULT_NOTES = "Thank you for your business!"
