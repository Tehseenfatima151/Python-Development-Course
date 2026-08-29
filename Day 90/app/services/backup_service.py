"""
Backup and Restore Service for InvoicePro
Handles automated database ZIP snapshot exports, safety checkpoints, and restorations.
"""
import os
import shutil
import zipfile
import logging
from datetime import datetime
from pathlib import Path
from typing import Tuple
from sqlalchemy import text

from app.config import DATA_DIR, BACKUP_DIR
from app.database.db import engine, SessionLocal

logger = logging.getLogger(__name__)


class BackupService:
    @staticmethod
    def get_db_file_path() -> Path:
        return DATA_DIR / "invoicepro.db"

    @staticmethod
    def create_backup() -> Tuple[bool, str, str]:
        """
        Checkpoints WAL and creates a timestamped ZIP archive containing the SQLite database.
        Returns: (success, backup_path, message)
        """
        try:
            BACKUP_DIR.mkdir(parents=True, exist_ok=True)
            db_path = BackupService.get_db_file_path()

            if not db_path.exists():
                return False, "", "Database file does not exist to back up."

            # Force WAL checkpoint so all committed transactions are in the main .db file
            try:
                with engine.connect() as conn:
                    conn.execute(text("PRAGMA wal_checkpoint(TRUNCATE)"))
            except Exception as pe:
                logger.warning(f"WAL checkpoint warning: {pe}")

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            zip_name = f"invoicepro_backup_{timestamp}.zip"
            zip_path = BACKUP_DIR / zip_name

            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
                zf.write(db_path, arcname="invoicepro.db")

            logger.info(f"Database backup created at {zip_path}")
            return True, str(zip_path), f"Backup created successfully: {zip_name}"

        except Exception as e:
            logger.error(f"Backup creation error: {e}")
            return False, "", f"Failed to create backup: {str(e)}"

    @staticmethod
    def restore_backup(zip_path_str: str) -> Tuple[bool, str]:
        """
        Safely restores a SQLite database from a ZIP archive.
        Takes an automatic safety backup of current database first.
        """
        try:
            zip_path = Path(zip_path_str)
            if not zip_path.exists():
                return False, "Selected backup archive file does not exist."

            db_path = BackupService.get_db_file_path()

            # Close all engine connections
            SessionLocal.remove()
            engine.dispose()

            # 1. Take safety backup of current state if DB exists
            if db_path.exists():
                safety_ts = datetime.now().strftime("%Y%m%d_%H%M%S_prerestore")
                safety_zip = BACKUP_DIR / f"invoicepro_safety_{safety_ts}.zip"
                with zipfile.ZipFile(safety_zip, "w", zipfile.ZIP_DEFLATED) as zf:
                    zf.write(db_path, arcname="invoicepro.db")

            # Remove lingering -wal or -shm files
            for extra_ext in ["-wal", "-shm"]:
                extra_file = Path(str(db_path) + extra_ext)
                if extra_file.exists():
                    try:
                        extra_file.unlink()
                    except Exception:
                        pass

            # 2. Extract backup database into DATA_DIR
            with zipfile.ZipFile(zip_path, "r") as zf:
                zf.extract("invoicepro.db", path=DATA_DIR)

            logger.info(f"Database successfully restored from {zip_path}")
            return True, "Database restored successfully."

        except Exception as e:
            logger.error(f"Backup restoration error: {e}")
            return False, f"Failed to restore backup: {str(e)}"
