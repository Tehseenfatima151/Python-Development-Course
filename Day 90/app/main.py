"""
InvoicePro Main Application Entry Point
"""
import os
import sys
import logging
from pathlib import Path

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

from app.config import (
    APP_NAME, APP_VERSION, APP_SUBTITLE, STYLES_DIR, LOG_FILE, LOG_DIR
)
from app.database.db import init_db, SessionLocal
from app.database.repositories import CompanyRepository
from app.ui.main_window import MainWindow
from app.ui.wizard import FirstLaunchWizard

# Setup global logging
LOG_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    encoding="utf-8"
)
logger = logging.getLogger("InvoicePro")


def load_stylesheet(app: QApplication):
    qss_path = STYLES_DIR / "theme.qss"
    if qss_path.exists():
        with open(qss_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
        logger.info("Loaded custom stylesheet theme.qss.")


def main():
    logger.info(f"Starting {APP_NAME} v{APP_VERSION}")

    # High DPI scaling attributes for crisp rendering on 4K / Retina displays
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    app.setOrganizationName("InvoicePro")

    # Load theme
    load_stylesheet(app)

    # Initialize Database
    try:
        init_db()
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.critical(f"Database initialization failed: {e}")
        sys.exit(1)

    # First launch check: if company has default name and 0 custom customer invoices
    session = SessionLocal()
    try:
        company = CompanyRepository.get_company(session)
        is_first_launch = (company is None)
    finally:
        session.close()

    if is_first_launch:
        wizard = FirstLaunchWizard()
        wizard.exec()

    # Launch Main Window
    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
