# Sales Data Analyzer

A production-grade, workflow-centric Python application and interactive analytics dashboard that transforms raw sales CSV transactional data into verified datasets, business KPIs, interactive visualizations, linear regression sales forecasts, and publication-ready executive PDF business reports.

The application features a **dual operating architecture**:
1. **Interactive Web Application** (`streamlit run dashboard.py`) built around a clean User Upload &rarr; Validate &rarr; Clean &rarr; Analyze &rarr; Predict &rarr; PDF Export workflow.
2. **Terminal-Based CLI** (`python main.py`) for automated, scriptable, or local command-line operations.

---

## What Problem Does This Solve?

Retail enterprises and businesses frequently store sales history in messy, disparate CSV files containing missing values, duplicate records, unformatted date columns, or inconsistent schemas. Making sense of this raw data usually requires tedious manual spreadsheet manipulation.

**Sales Data Analyzer** automates the complete data intelligence lifecycle:
```text
User Uploads CSV 
       ↓
Automatic Schema & Column Validation
       ↓
Data Cleaning & Missing Value Imputation
       ↓
Executive KPIs, Trends & Correlations
       ↓
Machine Learning Next-Month Sales Forecast
       ↓
Downloadable Cleaned CSV & Professional PDF Business Report
```

---

## Features

- **User-Centric Web Workflow (`dashboard.py`)**:
  - **Welcome Screen**: Communicates features with a value checklist and an intuitive file uploader (`.csv`).
  - **Demo Benchmark Dataset**: 1-click **"Try Demo Dataset"** option to explore the entire tool without needing a file on hand.
  - **Raw Data Overview & Pre-Cleaning Preview**: Inspects rows, columns, data types, missing cells, duplicate records, and displays the first 15 rows before cleaning.
  - **Data Cleaning Audit**: Interactive cleaning pipeline with missing-value imputation (median/mode), duplicate removal, invalid date pruning, and immediate download of the cleaned CSV.
  - **Executive Summary Dashboard**: Live KPI cards (Revenue, Units, Orders, Average Order Value, Top Performers, Sales Trend indicator).
  - **Dynamic Date Filtering**: Custom date range selection with quick presets (**Full Dataset**, **Last 2 Years**, **Last 1 Year**).
  - **Interactive Visualizations (Plotly)**:
    - Chronological Monthly Sales Trend line chart.
    - Quarterly revenue breakdown bar chart.
    - Top 5 Best-Selling Products horizontal leaderboard.
    - Category market share donut chart.
    - Regional territory volume chart (gracefully skipped if no region column exists).
    - Numerical correlation matrix with dynamic natural language insights.
  - **Basic Machine Learning Forecast**: Ordinary Least Squares Simple Linear Regression forecasting next month's sales, with $R^2$ score, slope, equation, interactive plot, and explicit methodology disclaimer.
  - **Executive PDF Report Generator**: Compiles a 12-section publication-ready PDF report containing company KPIs, tables, and high-resolution charts tailored to the uploaded dataset.
  - **Reset / New File**: Clean state reset button to upload and analyze new datasets seamlessly.

- **Preserved Headless & Terminal CLI (`main.py`)**:
  - Full interactive menu (`python main.py`).
  - Automated batch execution flags (`--auto`, `--start-date`, `--end-date`, `--no-pdf`).

---

## CSV Dataset Flexibility & Supported Formats

The analyzer accepts CSV files with flexible column naming conventions:

| Standard Field | Accepted Column Name Variations | Description |
| :--- | :--- | :--- |
| **Date** *(Required)* | `Date`, `Order Date`, `Order_Date`, `Sales_Date`, `Sale Date` | Transaction date (YYYY-MM-DD or parseable format) |
| **Product** *(Required)* | `Product`, `Product Name`, `Product_Name`, `Item`, `Item_Name` | Product SKU or description |
| **Quantity** *(Required)* | `Quantity`, `Qty`, `Units`, `Units Sold` | Non-negative units purchased |
| **Price / Sales** *(Required)* | `Unit_Price`, `Price`, `Sales`, `Revenue`, `Total_Sales`, `Amount` | If only one is present, the other is automatically calculated (`Sales = Qty * Price`) |
| **Category** *(Optional)* | `Category`, `Product Category`, `Product_Category` | Merchandise category (defaults to `General` if omitted) |
| **Region** *(Optional)* | `Region`, `Territory`, `Location`, `Area` | Sales territory (regional analytics gracefully adapts if omitted) |

---

## Installation & Setup

### 1. Clone or Open the Repository
```bash
cd "sales-data-analyzer"
```

### 2. Create and Activate Virtual Environment

**Windows:**
```powershell
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## Usage

### 1. Interactive Web Dashboard (Recommended)

```bash
streamlit run dashboard.py
```

1. Open the local browser URL (typically `http://localhost:8501`).
2. Upload your own sales CSV or click **"Try Demo Dataset"**.
3. Review the raw data preview and click **"Clean & Analyze Data"**.
4. Adjust the date range filter and explore interactive charts.
5. Click **"Generate Executive PDF Report"** to download the business report.

---

### 2. Command-Line Interface (CLI)

#### Interactive Terminal Menu
```bash
python main.py
```

#### Automated Headless Batch Execution
```bash
# Run full dataset analysis and export PDF
python main.py --auto

# Run custom date slice
python main.py --start-date 2023-01-01 --end-date 2024-12-31

# Run fast terminal analysis without PDF
python main.py --auto --no-pdf
```

---

## Machine Learning & Forecasting Methodology

The forecasting module (`src/prediction.py`) fits an **Ordinary Least Squares (OLS) Simple Linear Regression** model on sequential monthly revenue:

$$\hat{y}_t = \beta_1 \cdot t + \beta_0$$

Where $t \in \{1, 2, \dots, N\}$ represents the chronological month index.

> [!WARNING]
> **Methodology Disclaimer**: Simple Linear Regression provides a baseline linear trend estimate. It assumes constant trajectory and does not account for complex non-linear seasonality, inventory stockouts, marketing promotions, or macroeconomic shifts.

---

## Running Automated Tests

Run the full test suite with Pytest:
```bash
pytest -v
```

Tests include coverage for:
- Column normalization and schema validation
- Duplicate detection and removal
- Missing value imputation (median/mode) and invalid date pruning
- Multi-year monthly and quarterly aggregations
- Top 5 products ranking
- CSVs without a Region column
- Small datasets with insufficient monthly data (< 3 months)
- Single-product and single-category datasets

---

## License

MIT License. Designed and engineered for production-grade retail data analytics.
