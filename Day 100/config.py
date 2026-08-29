"""Configuration settings for the Sales Data Analyzer application."""

from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
CHARTS_DIR = OUTPUT_DIR / "charts"
REPORTS_DIR = OUTPUT_DIR / "reports"
CLEANED_DATA_DIR = OUTPUT_DIR / "cleaned_data"
LOGS_DIR = BASE_DIR / "logs"

# Input / Output File Paths
INPUT_CSV_PATH = DATA_DIR / "sales_data.csv"
CLEANED_CSV_PATH = CLEANED_DATA_DIR / "cleaned_sales_data.csv"
PDF_REPORT_PATH = REPORTS_DIR / "sales_analysis_report.pdf"
LOG_FILE_PATH = LOGS_DIR / "app.log"

# Chart File Paths
CHART_MONTHLY_TREND = CHARTS_DIR / "monthly_sales_trend.png"
CHART_QUARTERLY_SALES = CHARTS_DIR / "quarterly_sales.png"
CHART_TOP_PRODUCTS = CHARTS_DIR / "top_5_products.png"
CHART_CATEGORY_SALES = CHARTS_DIR / "category_sales.png"
CHART_REGIONAL_SALES = CHARTS_DIR / "regional_sales.png"
CHART_CORRELATION_HEATMAP = CHARTS_DIR / "correlation_heatmap.png"
CHART_PREDICTION = CHARTS_DIR / "sales_prediction.png"

# Required Columns and Column Name Standardizations
REQUIRED_COLUMNS = ["Date", "Product", "Category", "Quantity", "Unit_Price", "Sales", "Region"]
COLUMN_MAPPINGS = {
    "date": "Date",
    "order_date": "Date",
    "sales_date": "Date",
    "product": "Product",
    "product_name": "Product",
    "item": "Product",
    "category": "Category",
    "product_category": "Category",
    "quantity": "Quantity",
    "qty": "Quantity",
    "units": "Quantity",
    "unit_price": "Unit_Price",
    "price": "Unit_Price",
    "sales": "Sales",
    "revenue": "Sales",
    "total_sales": "Sales",
    "region": "Region",
    "location": "Region",
    "territory": "Region",
}

# Prediction Settings
MIN_OBSERVATIONS_FOR_REGRESSION = 3

# Visual Palette & Styling
STYLE_PALETTE = {
    "primary": "#1E3A8A",      # Deep Navy Blue
    "secondary": "#0284C7",    # Sky Blue
    "accent": "#F59E0B",       # Amber Gold
    "success": "#10B981",      # Emerald Green
    "danger": "#EF4444",       # Coral Red
    "dark": "#1F2937",         # Charcoal
    "light": "#F8FAFC",        # Off White
    "grid": "#E2E8F0",         # Slate border
}

def ensure_directories():
    """Ensure all required directories exist."""
    for directory in [DATA_DIR, OUTPUT_DIR, CHARTS_DIR, REPORTS_DIR, CLEANED_DATA_DIR, LOGS_DIR]:
        directory.mkdir(parents=True, exist_ok=True)
