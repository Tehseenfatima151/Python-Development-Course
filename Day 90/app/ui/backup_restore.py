"""
Backup & Restore UI for InvoicePro
Allows creating snapshot ZIP backups of the SQLite database and safely restoring.
"""
import os
from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget,
    QTableWidgetItem, QHeaderView, QFileDialog, QMessageBox, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from app.config import BACKUP_DIR
from app.services.backup_service import BackupService
from app.ui.components.cards import CardPanel
from app.ui.components.toast import ToastNotification


class BackupRestoreWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.load_backups_list()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(16)

        # ── Page Header ──────────────────────────────────────────────────────
        title_row = QHBoxLayout()
        title_col = QVBoxLayout()
        title_col.setSpacing(4)

        lbl_title = QLabel("Backup & Restore")
        lbl_title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        lbl_title.setStyleSheet("color: #0A2540;")
        title_col.addWidget(lbl_title)

        lbl_sub = QLabel("Create database snapshots and restore from previous backups")
        lbl_sub.setFont(QFont("Segoe UI", 11))
        lbl_sub.setStyleSheet("color: #64748B;")
        title_col.addWidget(lbl_sub)

        title_row.addLayout(title_col)
        title_row.addStretch()

        btn_backup = QPushButton("💾  Create Backup Now")
        btn_backup.setFont(QFont("Segoe UI", 11, QFont.Bold))
        btn_backup.setFixedHeight(40)
        btn_backup.setMinimumWidth(170)
        btn_backup.setCursor(Qt.PointingHandCursor)
        btn_backup.setStyleSheet("""
            QPushButton { background-color:#0A2540; color:#FFFFFF; font-weight:600;
                border:none; border-radius:6px; padding:8px 20px; }
            QPushButton:hover   { background-color:#1E3A8A; }
            QPushButton:pressed { background-color:#002D62; }
        """)
        btn_backup.clicked.connect(self.create_backup_action)
        title_row.addWidget(btn_backup)

        btn_restore_file = QPushButton("📂  Restore From File...")
        btn_restore_file.setFixedHeight(40)
        btn_restore_file.setMinimumWidth(170)
        btn_restore_file.setCursor(Qt.PointingHandCursor)
        btn_restore_file.setStyleSheet("""
            QPushButton { background-color:#FFFFFF; color:#334155; font-size:13px;
                font-weight:500; border:1px solid #CBD5E1; border-radius:6px; padding:8px 18px; }
            QPushButton:hover   { background-color:#F1F5F9; border-color:#94A3B8; color:#0A2540; }
            QPushButton:pressed { background-color:#E2E8F0; }
        """)
        btn_restore_file.clicked.connect(self.restore_from_file_action)
        title_row.addWidget(btn_restore_file)

        layout.addLayout(title_row)

        # Backup History Panel
        panel = CardPanel("Available Backups", "Local snapshot archives stored in the backups folder")
        
        self.table = QTableWidget()
        self.headers = ["Filename", "File Size", "Last Modified", "Actions"]
        self.table.setColumnCount(len(self.headers))
        self.table.setHorizontalHeaderLabels(self.headers)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.Fixed)
        self.table.setColumnWidth(3, 110)
        self.table.verticalHeader().setDefaultSectionSize(42)

        panel.layout.addWidget(self.table)
        layout.addWidget(panel)

    def load_backups_list(self):
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        backup_files = sorted(BACKUP_DIR.glob("*.zip"), key=os.path.getmtime, reverse=True)
        self.table.setRowCount(len(backup_files))

        for r, fpath in enumerate(backup_files):
            # Filename
            item_name = QTableWidgetItem(fpath.name)
            item_name.setFont(QFont("Segoe UI", 9, QFont.Bold))
            self.table.setItem(r, 0, item_name)

            # Size
            size_kb = fpath.stat().st_size / 1024
            item_size = QTableWidgetItem(f"{size_kb:.1f} KB")
            self.table.setItem(r, 1, item_size)

            # Modified
            import datetime
            mtime = datetime.datetime.fromtimestamp(fpath.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            item_time = QTableWidgetItem(mtime)
            self.table.setItem(r, 2, item_time)

            # Action: Restore button with consistent style
            btn_restore = QPushButton("↩ Restore")
            btn_restore.setFixedHeight(28)
            btn_restore.setStyleSheet("""
                QPushButton {
                    background-color: #C8102E;
                    color: #FFFFFF;
                    font-size: 12px;
                    font-weight: 600;
                    border: none;
                    border-radius: 5px;
                    padding: 4px 10px;
                    min-width: 80px;
                }
                QPushButton:hover   { background-color: #A50D24; }
                QPushButton:pressed { background-color: #880B1D; }
            """)
            btn_restore.setCursor(Qt.PointingHandCursor)
            btn_restore.clicked.connect(lambda checked=False, p=str(fpath): self.restore_specific_backup(p))
            self.table.setCellWidget(r, 3, btn_restore)

    def create_backup_action(self):
        success, path, msg = BackupService.create_backup()
        if success:
            ToastNotification.show_toast(self.window(), "Database backup created successfully!", "success")
            self.load_backups_list()
        else:
            QMessageBox.critical(self, "Backup Error", msg)

    def restore_from_file_action(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Backup Archive", str(BACKUP_DIR), "Zip Archives (*.zip)")
        if file_path:
            self.restore_specific_backup(file_path)

    def restore_specific_backup(self, zip_path: str):
        reply = QMessageBox.warning(
            self,
            "Confirm Database Restore",
            "Are you sure you want to restore this database snapshot?\n"
            "An automatic backup of your current database will be taken before restoring.\n\n"
            "After restoration, the application will require a restart.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            success, msg = BackupService.restore_backup(zip_path)
            if success:
                QMessageBox.information(self, "Restore Completed", msg)
                self.load_backups_list()
            else:
                QMessageBox.critical(self, "Restore Error", msg)
