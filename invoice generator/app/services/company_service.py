"""
Company Service & Backup Service for InvoicePro
Handles company profile persistence, branding assets, and database backup / restore.
"""
import os
import shutil
import zipfile
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
from sqlalchemy.orm import Session

from app.config import DATA_DIR, BACKUP_DIR, DATABASE_URL
from app.database.models import Company
from app.database.repositories import CompanyRepository

logger = logging.getLogger(__name__)


class CompanyService:
    @staticmethod
    def get_company_profile(session: Session) -> Optional[Company]:
        return CompanyRepository.get_company(session)

    @staticmethod
    def update_company_profile(session: Session, data: Dict[str, Any]) -> Tuple[bool, Optional[Company], str]:
        try:
            company = CompanyRepository.update_company(session, data)
            return True, company, "Company profile updated successfully."
        except Exception as e:
            session.rollback()
            logger.error(f"Error updating company profile: {e}")
            return False, None, f"Failed to update profile: {str(e)}"


class BackupService:
    @staticmethod
    def create_backup(backup_dir: Optional[Path] = None) -> Tuple[bool, str, str]:
        """
        Creates a timestamped ZIP backup of the SQLite database and metadata.
        """
        target_dir = backup_dir or BACKUP_DIR
        target_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"InvoicePro_Backup_{timestamp}.zip"
        backup_filepath = target_dir / backup_filename

        db_file = DATA_DIR / "invoicepro.db"
        if not db_file.exists():
            return False, "", "Database file not found."

        try:
            with zipfile.ZipFile(backup_filepath, "w", zipfile.ZIP_DEFLATED) as zip_file:
                # Add SQLite file
                zip_file.write(db_file, arcname="invoicepro.db")

                # Add metadata
                metadata = {
                    "app": "InvoicePro",
                    "version": "1.0.0",
                    "backup_time": datetime.utcnow().isoformat(),
                    "filename": backup_filename
                }
                zip_file.writestr("metadata.json", json.dumps(metadata, indent=2))

            logger.info(f"Database backup created at {backup_filepath}")
            return True, str(backup_filepath), f"Backup successfully created: {backup_filename}"
        except Exception as e:
            logger.error(f"Backup failed: {e}")
            return False, "", f"Backup failed: {str(e)}"

    @staticmethod
    def restore_backup(backup_zip_path: str) -> Tuple[bool, str]:
        """
        Restores a backup ZIP file after creating a safety checkpoint of the current DB.
        """
        if not os.path.exists(backup_zip_path):
            return False, "Backup file does not exist."

        try:
            # 1. Create safety backup first
            BackupService.create_backup()

            # 2. Extract database
            with zipfile.ZipFile(backup_zip_path, "r") as zip_file:
                namelist = zip_file.namelist()
                if "invoicepro.db" not in namelist:
                    return False, "Invalid backup file: 'invoicepro.db' missing from archive."

                target_db_path = DATA_DIR / "invoicepro.db"
                zip_file.extract("invoicepro.db", path=DATA_DIR)

            logger.info(f"Successfully restored database from: {backup_zip_path}")
            return True, "Database restored successfully. Please restart the application."
        except Exception as e:
            logger.error(f"Restore failed: {e}")
            return False, f"Failed to restore database: {str(e)}"
