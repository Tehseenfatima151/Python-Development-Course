# 📂 Day 98 — Python Automation | Smart File Organizer

A Python automation project that automatically organizes files into categorized folders based on their file extensions.

## 🎯 Project Overview

Managing a messy Downloads or Desktop folder manually can be time-consuming. This project uses Python to automatically detect file types and move them into appropriate folders.

The goal is to automate a simple but practical everyday task using Python's built-in file-handling libraries.

## ✨ Features

* 📂 Automatically creates required folders
* 🔍 Detects file types using file extensions
* 🚚 Moves files into appropriate categories
* 📄 Organizes documents
* 🖼️ Organizes images
* 🎥 Organizes videos
* 🎵 Organizes audio files
* 📦 Organizes archive files
* 💻 Organizes programming/code files
* 📁 Places unsupported files in `Others`
* 🛡️ Handles existing folders safely
* ⚡ Quickly processes multiple files

## 🗂️ File Categories

| File Type                        | Folder    |
| -------------------------------- | --------- |
| `.pdf`, `.docx`, `.txt`, `.xlsx` | Documents |
| `.jpg`, `.jpeg`, `.png`, `.gif`  | Images    |
| `.mp4`, `.mkv`, `.avi`, `.mov`   | Videos    |
| `.mp3`, `.wav`, `.flac`          | Audio     |
| `.zip`, `.rar`, `.7z`, `.tar`    | Archives  |
| `.py`, `.js`, `.html`, `.css`    | Code      |
| Other extensions                 | Others    |

## 📁 Example

### Before

```text
Downloads/
├── resume.pdf
├── photo.jpg
├── song.mp3
├── project.zip
├── video.mp4
├── script.py
└── notes.docx
```

### After

```text
Downloads/
├── Documents/
│   ├── resume.pdf
│   └── notes.docx
├── Images/
│   └── photo.jpg
├── Audio/
│   └── song.mp3
├── Archives/
│   └── project.zip
├── Videos/
│   └── video.mp4
└── Code/
    └── script.py
```

## 🛠️ Technologies Used

* Python
* `pathlib`
* `shutil`
* File System Automation
* Conditional Logic
* Exception Handling

## 🧠 Concepts Learned

### 1. File System Automation

Learned how Python can interact with files and directories programmatically.

### 2. Path Handling

Used `pathlib` to work with file paths and extensions in a clean and reliable way.

### 3. File Operations

Used `shutil` to move files automatically between directories.

### 4. Conditional Automation

The program determines where a file belongs based on its extension.

### 5. Error Handling

Automation scripts need to handle unexpected files, missing directories, and other possible runtime issues safely.

## 🚀 Real-World Applications

This project can be extended into a more advanced productivity automation tool with features such as:

* 🔄 Automatic folder cleanup
* 📅 Scheduled organization
* 🔎 Duplicate file detection
* ✏️ Automatic file renaming
* 📝 Activity logging
* 📊 Organization reports
* 🖥️ Desktop automation
* 📥 Automatic Downloads folder management

## ▶️ How to Run

Clone the repository and navigate to the project directory.

```bash
python file_organizer.py
```

Configure the target folder path and run the script.

The program will automatically scan the folder and organize the files according to their types.

## 📌 Project Structure

```text
Day-98/
│
├── file_organizer.py
└── README.md
```

## 🎓 Day 98 Takeaway

> **Python automation can turn repetitive manual tasks into simple, reusable programs.**

Day 98 focused on using Python as a practical automation tool rather than just a programming language. This project demonstrates how a small script can solve a real everyday productivity problem.

## 📚 Python 100 Days of Code

**Day 98 of my Python learning journey**

Part of my ongoing **Python Development Pro Bootcamp / 100 Days of Code** journey.

---

⭐ Building one practical project at a time.
