# Day 89 InvoicePro — Professional Windows Desktop Invoice Generator

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![PySide6](https://img.shields.io/badge/GUI-PySide6-green.svg)](https://wiki.qt.io/Qt_for_Python)
[![SQLAlchemy](https://img.shields.io/badge/ORM-SQLAlchemy-red.svg)](https://www.sqlalchemy.org/)
[![ReportLab](https://img.shields.io/badge/PDF-ReportLab-orange.svg)](https://www.reportlab.com/)

**InvoicePro** is a commercial-grade, high-performance desktop invoice generator for Windows built with **Python 3.11+**, **PySide6 (Qt for Python)**, **SQLite + SQLAlchemy**, and **ReportLab**.

The application reproduces the professional visual hierarchy, structure, typography, table columns, metadata boxes, and dual-tone Navy (`#0A2540`) & Red (`#C8102E`) visual identity of standard commercial trade invoices while making every field completely dynamic, editable, and backed by a local relational database.

---

## 🌟 Key Features

- **Split-Screen Invoice Creator**: Form inputs on the left with instant real-time live preview on the right.
- **Trade & Commercial Data Model**: Supports Book Serial (`No:`), Invoice #, DC #1, DC #2, Order #, Delivered To, Invoiced To, Destination Address, and Dispatch Information.
- **Dynamic Line Items**: Product Name, Packing (`1kg`, `5 liter`, `25kg`), Physical Quantity, Quantity Unit, Billing Quantity, Bonus items, Unit Rate, and Line Amounts.
- **High-Precision Financial Arithmetic**: Pure `Decimal` arithmetic for subtotals, item discounts, invoice discounts, tax rates, shipping charges, and automatic English amount-to-words conversion (e.g. *One Lac Fifty One Thousand Five Hundred*).
- **Pixel-Perfect PDF Generation**: Native ReportLab vector PDF generator with A4 print layout, dynamic header, vector/custom logos, company stamp seal badge, authorized signature, and bottom wave accents.
- **Executive Dashboard**: KPI metric cards (Total Revenue, Monthly Revenue, Total Invoices, Paid, Pending) and recent billing activity table.
- **Full Invoice Lifecycle**: Searchable and filterable history grid, status tracking (*Paid*, *Pending*, *Draft*, *Sent*, *Overdue*, *Cancelled*), 1-click duplication, PDF export, system printing, and cascade deletion.
- **Customer Management**: Directory with search, financial summary (total spend, outstanding balance, invoice history), and 1-click invoice creation.
- **Company Branding & Settings**: Upload logo, stamp seal, and signature images, customize signatory names, bank account details, and invoice numbering sequences.
- **Local Data Safety & Backups**: 1-click timestamped SQLite database backups and safe restore with pre-restoration checkpoints.
- **Windows Desktop Executable**: Complete PyInstaller build script to generate standalone `InvoicePro.exe`.

---

## 🏗 Architecture & Code Structure

```text
invoice_generator/
│
├── app/
│   ├── main.py                     # Application entry point & Qt event loop
│   ├── config.py                   # Configuration, directories, color themes
│   │
│   ├── database/
│   │   ├── db.py                   # SQLite engine, session factory, auto-seed
│   │   ├── models.py               # SQLAlchemy ORM models (Company, Customer, Invoice, Item)
│   │   └── repositories.py         # Transactional CRUD repositories
│   │
│   ├── services/
│   │   ├── calculation_service.py  # Decimal arithmetic, discounts, taxes, totals
│   │   ├── pdf_service.py          # ReportLab PDF template generation
│   │   ├── invoice_service.py      # Invoice business logic & duplication
│   │   ├── company_service.py      # Company settings & preferences
│   │   └── backup_service.py       # Database ZIP export & restore
│   │
│   ├── utils/
│   │   ├── validators.py           # Email, numeric, and discount validators
│   │   ├── formatters.py           # Currency, date, and quantity formatters
│   │   ├── num_to_words.py         # Number to English words converter
│   │   └── helpers.py              # OS file opening & printer helpers
│   │
│   ├── ui/
│   │   ├── main_window.py          # Modern sidebar shell with tab navigation
│   │   ├── dashboard.py            # KPI cards & recent billing data
│   │   ├── invoice_form.py         # Split-screen invoice creator & editor
│   │   ├── invoice_preview.py      # Live high-DPI A4 preview widget
│   │   ├── invoice_history.py      # Searchable & filterable invoice grid
│   │   ├── customer_management.py  # Customer CRM & spending metrics
│   │   ├── company_settings.py     # Brand customizer & numbering defaults
│   │   ├── backup_restore.py       # Database snapshot & restore UI
│   │   ├── wizard.py               # First-launch onboarding wizard
│   │   ├── about_dialog.py         # About dialog & keyboard shortcuts
│   │   │
│   │   ├── components/
│   │   │   ├── cards.py            # MetricCard & CardPanel widgets
│   │   │   ├── badges.py           # StatusBadge pill widgets
│   │   │   ├── items_table.py      # Dynamic line items table
│   │   │   └── toast.py            # Non-blocking animated toast alerts
│   │   └── dialogs/
│   │       └── customer_dialog.py  # Create/Edit customer modal
│   │
│   └── resources/
│       └── styles/
│           └── theme.qss           # Modern dark/light stylesheet
│
├── tests/
│   ├── test_calculations.py        # Math precision & discount tests
│   ├── test_database.py            # CRUD & cascade deletion tests
│   ├── test_pdf.py                 # PDF generation & element tests
│   └── test_formatters.py          # Number to words & format tests
│
├── build_exe.py                    # PyInstaller standalone build script
├── requirements.txt                # Dependencies
└── README.md
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.11 or higher
- Windows 10 / 11

### 2. Installation
Clone the repository and install dependencies:
```powershell
pip install -r requirements.txt
```

### 3. Running the Application
Launch the application:
```powershell
python -m app.main
```

### 4. Running Automated Tests
Run the pytest test suite:
```powershell
pytest tests/ -v
```

### 5. Packaging into Standalone Windows EXE
Build the standalone `InvoicePro.exe` executable:
```powershell
python build_exe.py
```
The output executable will be generated at: `dist/InvoicePro/InvoicePro.exe`.

---

## ⌨ Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| `Ctrl + N` | Create New Invoice |
| `Ctrl + S` | Save Current Invoice |
| `Ctrl + P` | Print Current Invoice |
| `Ctrl + F` | Search All Invoices |
| `Ctrl + Q` | Exit Application |

---

## 📄 License
This project is proprietary software for commercial invoicing and portfolio demonstration.
