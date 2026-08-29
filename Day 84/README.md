# Day 84— Python Scripting Portfolio Project: Automatic File Organizer

Part of my [100 Days of Code — Python Bootcamp](https://github.com/Tehseenfatima151) journey (Angela Yu).

## 📌 Project: Automatic File Organizer

A practical automation script that scans a folder (like a messy Downloads folder) and automatically sorts every file into category subfolders — Images, Documents, Videos, Music, Archives, Code, Installers, and Other — based on file extension. Tested end-to-end on real dummy files before writing this README (see "Tested Output" below).

---

## 🧠 Concepts Covered

### 1. Working with the filesystem using `pathlib`
```python
from pathlib import Path

folder = Path(folder_path)
for item in folder.iterdir():
    if item.is_file():
        ...
```
`pathlib.Path` is the modern, recommended way to work with file paths in Python — more readable than string-concatenating paths manually, and works consistently across Windows/Mac/Linux.

### 2. Mapping file extensions to categories
```python
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ...],
    "Documents": [".pdf", ".doc", ".docx", ...],
    ...
}

def get_category(extension):
    for category, extensions in FILE_CATEGORIES.items():
        if extension.lower() in extensions:
            return category
    return "Other"
```
A dictionary lookup keeps this easily extendable — adding a new file type or category is a one-line change, not a rewrite of logic.

### 3. Creating folders safely
```python
destination_folder.mkdir(exist_ok=True)
```
`exist_ok=True` prevents an error if the category folder already exists (e.g. running the script twice) — without it, `mkdir()` raises `FileExistsError`.

### 4. Moving files with `shutil`
```python
import shutil
shutil.move(str(item), str(destination_folder / item.name))
```
`shutil.move()` handles the actual file relocation — safer than manually copying + deleting, since it's a single atomic-ish operation.

### 5. A `dry_run` safety feature
```python
def organize_folder(folder_path, dry_run=False):
    ...
    if not dry_run:
        destination_folder.mkdir(exist_ok=True)
        shutil.move(...)
```
Before running any script that moves/deletes real files, it's good practice to preview what *would* happen. `dry_run=True` shows the plan without touching anything — a habit worth having for any automation script, not just this one.

### 6. Command-line arguments with `sys.argv`
```python
import sys
target_folder = sys.argv[1] if len(sys.argv) > 1 else "."
```
This lets the script be run against any folder from the terminal — `python file_organizer.py ~/Downloads` — instead of hardcoding a path, making it an actually reusable tool rather than a one-off script.

### 7. Building a clear summary report
```python
summary.setdefault(category, []).append(item.name)
```
`.setdefault()` avoids a manual `if category not in summary: summary[category] = []` check — cleanly handles both "first file in this category" and "adding to an existing category" in one line.

---

## 📂 Project Structure
```
day81/
└── file_organizer.py
```

## ▶️ How to Run
```bash
python file_organizer.py /path/to/folder

# or, run it on the current folder:
python file_organizer.py
```

⚠️ **This script actually moves files.** Test it on a throwaway folder first (like this project's own test run below) before pointing it at a real Downloads folder.

---

## 🧪 Tested Output
Ran against a test folder containing 9 dummy files of different types:

```
Scanning folder: .../test_folder

==================================================
Organization Summary
==================================================

📁 Other (1 file)
   Moved: random_thing.xyz

📁 Music (1 file)
   Moved: song.mp3

📁 Documents (2 files)
   Moved: report.pdf
   Moved: notes.txt

📁 Archives (1 file)
   Moved: archive.zip

📁 Installers (1 file)
   Moved: installer.exe

📁 Videos (1 file)
   Moved: movie.mp4

📁 Code (1 file)
   Moved: script.py

📁 Images (1 file)
   Moved: vacation_photo.jpg

✅ Total: 9 file(s) organized into 8 categories.
```
Verified afterward that every file landed in its correct subfolder on disk.

---

## ✅ Key Takeaways
- `pathlib.Path` is the modern standard for filesystem work in Python — prefer it over manual string path-building.
- A `dry_run` mode is a valuable safety habit for any script that modifies/deletes real files — always preview before executing.
- Dictionary-based lookups (extension → category) keep rule-based logic easy to extend without touching the core function.
- `sys.argv` turns a one-off script into a reusable command-line tool.
- Real-world portfolio projects don't need to be complex — a small, genuinely useful automation script (like cleaning a Downloads folder) demonstrates practical scripting skills clearly.

## 📝 Practice Tasks
1. Add a `--undo` flag that reverses the last organization run (would need to log moves to a file first).
2. Add an option to organize by **date modified** instead of file type (e.g. into `2024/`, `2025/` folders).
3. Add a `.gitignore`-style config file so users can customize categories without editing the script.
4. Turn this into a scheduled task (cron on Mac/Linux, Task Scheduler on Windows) that auto-organizes Downloads every day.
