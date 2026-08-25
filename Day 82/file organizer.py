"""
Day 81 — Python Scripting Portfolio Project
Automatic File Organizer

Scans a target folder and automatically sorts files into subfolders
based on their file type (Images, Documents, Videos, Music, Archives,
Code, etc.) — a practical automation script useful for cleaning up a
real Downloads folder.

Usage:
    python file_organizer.py <folder_path>

If no folder_path is given, it defaults to the current directory.
"""

import os
import shutil
import sys
from pathlib import Path

# Map of category -> list of file extensions that belong to it
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".heic"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".xlsx", ".xls", ".ppt", ".pptx", ".csv"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv"],
    "Music": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".json", ".ipynb"],
    "Installers": [".exe", ".msi", ".dmg", ".pkg", ".deb"],
}


def get_category(extension: str) -> str:
    """Return the category folder name for a given file extension."""
    extension = extension.lower()
    for category, extensions in FILE_CATEGORIES.items():
        if extension in extensions:
            return category
    return "Other"


def organize_folder(folder_path: str, dry_run: bool = False) -> dict:
    """
    Organize all files in folder_path into category subfolders.
    Returns a summary dict: {category: [filenames moved]}.

    dry_run=True previews what WOULD happen without actually moving files —
    always run this first on a real folder before the real move.
    """
    folder = Path(folder_path)
    if not folder.is_dir():
        raise NotADirectoryError(f"'{folder_path}' is not a valid folder.")

    summary = {}

    # Only look at files directly inside the folder (not subfolders),
    # and skip files that are already sorted (inside a category folder)
    for item in folder.iterdir():
        if item.is_file():
            category = get_category(item.suffix)
            destination_folder = folder / category

            summary.setdefault(category, []).append(item.name)

            if not dry_run:
                destination_folder.mkdir(exist_ok=True)
                shutil.move(str(item), str(destination_folder / item.name))

    return summary


def print_summary(summary: dict, dry_run: bool):
    action = "Would move" if dry_run else "Moved"
    total = sum(len(files) for files in summary.values())

    if total == 0:
        print("No files found to organize.")
        return

    print(f"\n{'=' * 50}")
    print(f"{'DRY RUN — ' if dry_run else ''}Organization Summary")
    print(f"{'=' * 50}")
    for category, files in summary.items():
        print(f"\n📁 {category} ({len(files)} file{'s' if len(files) != 1 else ''})")
        for f in files:
            print(f"   {action}: {f}")
    print(f"\n✅ Total: {total} file(s) organized into {len(summary)} categories.")


if __name__ == "__main__":
    target_folder = sys.argv[1] if len(sys.argv) > 1 else "."

    print(f"Scanning folder: {os.path.abspath(target_folder)}")
    result = organize_folder(target_folder, dry_run=False)
    print_summary(result, dry_run=False)