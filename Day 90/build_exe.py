"""
PyInstaller Build Automation Script for InvoicePro
Packages InvoicePro into a standalone Windows executable.
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def build():
    print("=" * 60)
    print("Building InvoicePro Windows Desktop Executable...")
    print("=" * 60)

    dist_dir = BASE_DIR / "dist"
    build_dir = BASE_DIR / "build"
    spec_file = BASE_DIR / "InvoicePro.spec"
    main_script = BASE_DIR / "app" / "main.py"
    resources_dir = BASE_DIR / "app" / "resources"

    # Clean old builds
    for d in [dist_dir, build_dir]:
        if d.exists():
            shutil.rmtree(d, ignore_errors=True)
    if spec_file.exists():
        spec_file.unlink(missing_ok=True)

    # PyInstaller command arguments
    pyinstaller_args = [
        sys.executable, "-m", "PyInstaller",
        "--name=InvoicePro",
        "--noconsole",
        "--onedir",
        "--clean",
        "--noconfirm",
        f"--paths={str(BASE_DIR)}",
        f"--add-data={resources_dir}{os.pathsep}app/resources",
        # Explicitly include all application modules
        "--collect-all=app",
        "--hidden-import=app",
        "--hidden-import=app.config",
        "--hidden-import=app.database",
        "--hidden-import=app.database.models",
        "--hidden-import=app.database.db",
        "--hidden-import=app.database.repositories",
        "--hidden-import=app.services",
        "--hidden-import=app.services.calculation_service",
        "--hidden-import=app.services.pdf_service",
        "--hidden-import=app.services.invoice_service",
        "--hidden-import=app.services.company_service",
        "--hidden-import=app.services.backup_service",
        "--hidden-import=app.ui",
        "--hidden-import=app.ui.main_window",
        "--hidden-import=app.ui.dashboard",
        "--hidden-import=app.ui.invoice_form",
        "--hidden-import=app.ui.invoice_history",
        "--hidden-import=app.ui.invoice_preview",
        "--hidden-import=app.ui.customer_management",
        "--hidden-import=app.ui.company_settings",
        "--hidden-import=app.ui.backup_restore",
        "--hidden-import=app.ui.about_dialog",
        "--hidden-import=app.ui.wizard",
        "--hidden-import=app.ui.components.badges",
        "--hidden-import=app.ui.components.cards",
        "--hidden-import=app.ui.components.items_table",
        "--hidden-import=app.ui.components.toast",
        "--hidden-import=app.ui.dialogs.customer_dialog",
        "--hidden-import=app.utils.formatters",
        "--hidden-import=app.utils.helpers",
        "--hidden-import=app.utils.num_to_words",
        "--hidden-import=app.utils.validators",
        # Dependencies
        "--hidden-import=PySide6",
        "--hidden-import=PySide6.QtCore",
        "--hidden-import=PySide6.QtGui",
        "--hidden-import=PySide6.QtWidgets",
        "--hidden-import=sqlalchemy",
        "--hidden-import=reportlab",
        "--hidden-import=num2words",
        "--hidden-import=PIL",
        "--hidden-import=pypdf",
        str(main_script)
    ]

    print(f"Executing: {' '.join(pyinstaller_args)}")
    result = subprocess.run(pyinstaller_args, cwd=str(BASE_DIR))

    if result.returncode == 0:
        exe_path = dist_dir / "InvoicePro" / "InvoicePro.exe"
        print("\n" + "=" * 60)
        print("BUILD SUCCESSFUL!")
        print(f"Executable location: {exe_path}")
        print("=" * 60)
        return True
    else:
        print("\nBUILD FAILED!")
        return False


if __name__ == "__main__":
    success = build()
    sys.exit(0 if success else 1)
