"""Data loading, sample generation, validation, and cleaning module for Sales Data Analyzer."""

import logging
from pathlib import Path
from typing import Dict, Any, Tuple
import numpy as np
import pandas as pd

import config

logger = logging.getLogger("sales_analyzer.data_cleaning")


def generate_sample_dataset(filepath: Path, num_records: int = 3500) -> Path:
    """
    Generate approximately 5 years of realistic retail sales data (2021-2025).
    Includes multiple products, categories, regions, seasonal variations,
    a few intentional missing values, and duplicate rows.
    """
    if filepath.exists():
        logger.info(f"Sample dataset already exists at {filepath}")
        return filepath

    filepath.parent.mkdir(parents=True, exist_ok=True)
    logger.info(f"Generating realistic 5-year sample dataset with {num_records} records at {filepath}")

    np.random.seed(42)

    catalog = {
        "Technology": [
            ("Laptop Pro 15", 1199.99),
            ("Smartphone Ultra", 899.99),
            ("4K Ultra HD Monitor", 349.99),
            ("Wireless Noise-Canceling Headphones", 199.99),
            ("Ergonomic Mechanical Keyboard", 129.99),
        ],
        "Furniture": [
            ("Executive Ergonomic Desk", 549.00),
            ("High-Back Mesh Chair", 249.50),
            ("Bookshelf 5-Tier", 149.00),
            ("Standing Desk Converter", 179.99),
            ("Conference Room Table", 799.00),
        ],
        "Office Supplies": [
            ("Multipurpose Copy Paper (Carton)", 42.50),
            ("Heavy-Duty Stapler & Staples", 24.99),
            ("Gel Pens Pack (24ct)", 18.75),
            ("Document Filing Cabinet Tray", 35.00),
            ("Self-Adhesive Sticky Notes Bulk", 15.50),
        ],
        "Electronics Accessories": [
            ("External SSD 1TB", 109.99),
            ("USB-C Fast Charging Hub", 49.99),
            ("Precision Wireless Mouse", 39.99),
            ("HD Streaming Webcam 1080p", 69.99),
            ("Braided HDMI 4K Cable (2-Pack)", 19.99),
        ],
    }

    regions = ["North", "South", "East", "West", "Central"]

    start_date = pd.Timestamp("2021-01-01")
    end_date = pd.Timestamp("2025-12-31")
    total_days = (end_date - start_date).days

    records = []
    for _ in range(num_records):
        category = np.random.choice(list(catalog.keys()), p=[0.35, 0.25, 0.20, 0.20])
        product_item = catalog[category][np.random.randint(0, len(catalog[category]))]
        product_name, base_price = product_item

        # Price fluctuation
        unit_price = round(base_price * np.random.uniform(0.95, 1.05), 2)
        quantity = int(np.random.choice([1, 2, 3, 4, 5, 8, 10, 15, 20], p=[0.40, 0.25, 0.15, 0.08, 0.05, 0.03, 0.02, 0.01, 0.01]))
        sales = round(quantity * unit_price, 2)

        day_offset = np.random.randint(0, total_days + 1)
        record_date = start_date + pd.Timedelta(days=day_offset)
        if record_date.month in [11, 12] and np.random.rand() > 0.3:
            sales = round(sales * 1.15, 2)

        region = np.random.choice(regions, p=[0.25, 0.20, 0.25, 0.15, 0.15])

        records.append({
            "Date": record_date.strftime("%Y-%m-%d"),
            "Product": product_name,
            "Category": category,
            "Quantity": quantity,
            "Unit_Price": unit_price,
            "Sales": sales,
            "Region": region,
        })

    df = pd.DataFrame(records)

    # Inject duplicates
    duplicates = df.sample(n=35, random_state=42)
    df = pd.concat([df, duplicates], ignore_index=True)

    # Inject missing values
    mask_cat = np.random.rand(len(df)) < 0.015
    df.loc[mask_cat, "Category"] = np.nan

    mask_reg = np.random.rand(len(df)) < 0.015
    df.loc[mask_reg, "Region"] = np.nan

    mask_sales = np.random.rand(len(df)) < 0.01
    df.loc[mask_sales, "Sales"] = np.nan

    mask_date = np.random.rand(len(df)) < 0.005
    df.loc[mask_date, "Date"] = "INVALID_DATE"

    df.to_csv(filepath, index=False)
    logger.info(f"Sample dataset saved with {len(df)} raw rows to {filepath}")
    return filepath


def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize dataframe column names matching common variations."""
    rename_dict = {}
    for col in df.columns:
        clean_col = str(col).strip().lower().replace(" ", "_").replace("-", "_")
        if clean_col in config.COLUMN_MAPPINGS:
            rename_dict[col] = config.COLUMN_MAPPINGS[clean_col]
    return df.rename(columns=rename_dict)


def validate_required_columns(df: pd.DataFrame) -> None:
    """Validate that core necessary columns exist or can be derived."""
    standard_df = standardize_column_names(df)

    # Core essential columns: Date, Product, Quantity
    essential = ["Date", "Product", "Quantity"]
    missing_essential = [col for col in essential if col not in standard_df.columns]
    if missing_essential:
        err_msg = (
            f"Missing essential column(s): {missing_essential}. "
            f"Present columns in dataset: {list(df.columns)}"
        )
        logger.error(err_msg)
        raise ValueError(err_msg)

    # Either Sales or Unit_Price must be present
    if "Sales" not in standard_df.columns and "Unit_Price" not in standard_df.columns:
        err_msg = (
            "Dataset must contain either a 'Sales' (Revenue/Amount) or 'Unit_Price' (Price) column."
        )
        logger.error(err_msg)
        raise ValueError(err_msg)


def clean_sales_data(filepath_or_df: Any) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Execute full data cleaning pipeline:
    1. Standardize columns
    2. Count & remove duplicates
    3. Detect & report missing values
    4. Handle missing values logically (median/recalculation for numeric, mode/Unknown for categories)
    5. Cleanse and parse dates
    6. Ensure numeric validity (non-negative)
    7. Sort chronologically
    8. Export cleaned CSV and return dataframe with comprehensive audit metrics.
    """
    logger.info("Starting data cleaning pipeline")

    if isinstance(filepath_or_df, (str, Path)):
        filepath = Path(filepath_or_df)
        if not filepath.exists():
            raise FileNotFoundError(f"Input file not found at: {filepath}")
        df = pd.read_csv(filepath)
    elif isinstance(filepath_or_df, pd.DataFrame):
        df = filepath_or_df.copy()
    else:
        raise TypeError("Input must be a file path or pandas DataFrame")

    if df.empty:
        raise ValueError("Dataset is empty. Cannot perform analysis on an empty file.")

    # 1. Standardize column names
    df = standardize_column_names(df)
    validate_required_columns(df)

    rows_before = len(df)
    missing_before = {str(k): int(v) for k, v in df.isnull().sum().items()}

    # 2. Duplicate Detection & Removal
    duplicate_count = int(df.duplicated().sum())
    if duplicate_count > 0:
        logger.info(f"Removing {duplicate_count} duplicate rows")
        df = df.drop_duplicates().reset_index(drop=True)

    # 3. Clean and Parse Dates
    invalid_dates_count = 0
    if "Date" in df.columns:
        date_series = pd.to_datetime(df["Date"], errors="coerce")
        invalid_dates_count = int(date_series.isna().sum())
        if invalid_dates_count > 0:
            logger.warning(f"Dropping {invalid_dates_count} rows with invalid dates")
        df["Date"] = date_series
        df = df.dropna(subset=["Date"]).reset_index(drop=True)

    # 4. Handle Numeric Columns
    for col in ["Quantity", "Unit_Price", "Sales"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # If Sales is missing, calculate from Quantity * Unit_Price
    if "Sales" not in df.columns or df["Sales"].isna().any():
        if "Quantity" in df.columns and "Unit_Price" in df.columns:
            calculated_sales = df["Quantity"] * df["Unit_Price"]
            if "Sales" not in df.columns:
                df["Sales"] = calculated_sales
            else:
                df["Sales"] = df["Sales"].fillna(calculated_sales)

    # If Unit_Price is missing, calculate from Sales / Quantity
    if "Unit_Price" not in df.columns or df["Unit_Price"].isna().any():
        if "Sales" in df.columns and "Quantity" in df.columns:
            safe_qty = df["Quantity"].replace(0, np.nan)
            calculated_price = (df["Sales"] / safe_qty).round(2)
            if "Unit_Price" not in df.columns:
                df["Unit_Price"] = calculated_price
            else:
                df["Unit_Price"] = df["Unit_Price"].fillna(calculated_price)

    # Handle remaining missing numeric values using median
    for num_col in ["Quantity", "Unit_Price", "Sales"]:
        if num_col in df.columns and df[num_col].isna().any():
            median_val = df[num_col].median()
            median_val = median_val if not pd.isna(median_val) else 0.0
            logger.info(f"Imputing missing values in '{num_col}' with median: {median_val}")
            df[num_col] = df[num_col].fillna(median_val)

    # 5. Non-negative values validation
    for num_col in ["Quantity", "Unit_Price", "Sales"]:
        if num_col in df.columns:
            df = df[df[num_col] >= 0].copy()

    # 6. Handle Categorical Columns
    if "Category" not in df.columns:
        df["Category"] = "General"
    else:
        df["Category"] = df["Category"].astype(str).str.strip().replace(["nan", "None", ""], np.nan)
        if df["Category"].isna().any():
            mode_cat = df["Category"].dropna().mode()
            fill_cat = mode_cat.iloc[0] if not mode_cat.empty else "General"
            df["Category"] = df["Category"].fillna(fill_cat)

    if "Product" in df.columns:
        df["Product"] = df["Product"].astype(str).str.strip().replace(["nan", "None", ""], np.nan)
        df["Product"] = df["Product"].fillna("Unknown Product")

    if "Region" in df.columns:
        df["Region"] = df["Region"].astype(str).str.strip().replace(["nan", "None", ""], np.nan)
        if df["Region"].isna().any():
            mode_reg = df["Region"].dropna().mode()
            fill_reg = mode_reg.iloc[0] if not mode_reg.empty else "Unknown"
            df["Region"] = df["Region"].fillna(fill_reg)

    # 7. Sort Chronologically
    if "Date" in df.columns:
        df = df.sort_values(by="Date").reset_index(drop=True)

    rows_after = len(df)
    missing_after = {str(k): int(v) for k, v in df.isnull().sum().items()}

    if rows_after == 0:
        raise ValueError("Data cleaning resulted in 0 valid records. Please check the raw data.")

    # 8. Save Cleaned Dataset
    config.CLEANED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(config.CLEANED_CSV_PATH, index=False)
    logger.info(f"Cleaned dataset saved successfully to {config.CLEANED_CSV_PATH}")

    total_missing_handled = int(sum(missing_before.values()) - sum(missing_after.values()))

    summary = {
        "rows_before": rows_before,
        "rows_after": rows_after,
        "duplicates_removed": duplicate_count,
        "invalid_dates_removed": invalid_dates_count,
        "missing_before": missing_before,
        "missing_after": missing_after,
        "missing_handled_count": max(0, total_missing_handled),
        "min_date": df["Date"].min().strftime("%Y-%m-%d") if "Date" in df.columns else None,
        "max_date": df["Date"].max().strftime("%Y-%m-%d") if "Date" in df.columns else None,
        "has_region": "Region" in df.columns,
        "total_records": len(df),
    }

    return df, summary
