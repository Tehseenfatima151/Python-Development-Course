"""
Helper Utilities for InvoicePro
Handles system operations such as opening PDFs, printing, file dialogs, and sanitization.
"""
import os
import sys
import subprocess
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


def sanitize_filename(name: str) -> str:
    """Sanitizes a string to be safely used as a filename."""
    keep_chars = ("-", "_", ".", " ")
    return "".join(c for c in name if c.isalnum() or c in keep_chars).rstrip()


def open_file_in_system_viewer(filepath: Path) -> bool:
    """Opens a file (such as a PDF) in the default OS application."""
    if not filepath or not os.path.exists(filepath):
        logger.error(f"File not found for viewing: {filepath}")
        return False
    try:
        if sys.platform.startswith("win"):
            os.startfile(str(filepath))
        elif sys.platform.startswith("darwin"):
            subprocess.run(["open", str(filepath)], check=True)
        else:
            subprocess.run(["xdg-open", str(filepath)], check=True)
        return True
    except Exception as e:
        logger.error(f"Failed to open file {filepath}: {e}")
        return False


def print_file_with_system_dialog(filepath: Path) -> bool:
    """Sends a PDF file to the system printer."""
    if not filepath or not os.path.exists(filepath):
        logger.error(f"File not found for printing: {filepath}")
        return False
    try:
        if sys.platform.startswith("win"):
            # Use ShellExecute with 'print' verb
            import win32api  # type: ignore
            import win32print  # type: ignore
            win32api.ShellExecute(0, "print", str(filepath), None, ".", 0)
            return True
        else:
            subprocess.run(["lpr", str(filepath)], check=True)
            return True
    except Exception as e:
        logger.warning(f"Direct print failed ({e}). Falling back to opening file viewer.")
        return open_file_in_system_viewer(filepath)
