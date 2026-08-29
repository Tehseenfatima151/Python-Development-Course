"""Unit tests for data cleaning, generation, and validation."""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
from src import data_cleaning


def test_standardize_column_names():
    raw_df = pd.DataFrame({
        "order_date": ["2023-01-01"],
        "product_name": ["Laptop"],
        "qty": [2],
        "price": [999.0],
        "revenue": [1998.0],
        "territory": ["North"],
        "category": ["Tech"],
    })
    standardized = data_cleaning.standardize_column_names(raw_df)
    assert "Date" in standardized.columns
    assert "Product" in standardized.columns
    assert "Quantity" in standardized.columns
    assert "Unit_Price" in standardized.columns
    assert "Sales" in standardized.columns
    assert "Region" in standardized.columns
    assert "Category" in standardized.columns


def test_clean_sales_data_pipeline(tmp_path):
    # Construct raw dataframe with duplicates, missing values, and invalid dates
    raw_data = {
        "Date": ["2023-01-01", "2023-01-02", "2023-01-02", "INVALID_DATE", "2023-01-04", "2023-01-05"],
        "Product": ["Laptop", "Mouse", "Mouse", "Desk", "Chair", "Laptop"],
        "Category": ["Tech", "Tech", "Tech", np.nan, "Furniture", "Tech"],
        "Quantity": [2, 5, 5, 1, np.nan, 3],
        "Unit_Price": [1000.0, 20.0, 20.0, 200.0, 150.0, np.nan],
        "Sales": [2000.0, 100.0, 100.0, 200.0, np.nan, 3000.0],
        "Region": ["North", "South", "South", "West", np.nan, "East"],
    }
    df = pd.DataFrame(raw_data)
    csv_file = tmp_path / "test_raw_sales.csv"
    df.to_csv(csv_file, index=False)

    cleaned_df, summary = data_cleaning.clean_sales_data(csv_file)

    # 1. Duplicates removed (row index 2 was exact duplicate)
    assert summary["duplicates_removed"] >= 1

    # 2. Invalid date dropped
    assert "INVALID_DATE" not in cleaned_df["Date"].astype(str).values

    # 3. No remaining missing values
    assert sum(summary["missing_after"].values()) == 0

    # 4. Correct data types
    assert pd.api.types.is_datetime64_any_dtype(cleaned_df["Date"])
    assert pd.api.types.is_numeric_dtype(cleaned_df["Quantity"])
    assert pd.api.types.is_numeric_dtype(cleaned_df["Unit_Price"])
    assert pd.api.types.is_numeric_dtype(cleaned_df["Sales"])


def test_calculate_sales_if_missing(tmp_path):
    raw_data = {
        "Date": ["2023-01-01", "2023-01-02"],
        "Product": ["Pen", "Notebook"],
        "Category": ["Office", "Office"],
        "Quantity": [10, 5],
        "Unit_Price": [2.5, 4.0],
        "Region": ["East", "West"],
    }
    df = pd.DataFrame(raw_data)
    csv_file = tmp_path / "test_no_sales.csv"
    df.to_csv(csv_file, index=False)

    cleaned_df, summary = data_cleaning.clean_sales_data(csv_file)
    assert "Sales" in cleaned_df.columns
    assert list(cleaned_df["Sales"]) == [25.0, 20.0]
