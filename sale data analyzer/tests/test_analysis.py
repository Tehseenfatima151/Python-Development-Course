"""Unit tests for sales analysis and aggregations."""

import pytest
import pandas as pd
import numpy as np
from src import analysis


@pytest.fixture
def sample_sales_df():
    data = {
        "Date": pd.to_datetime(["2023-01-15", "2023-02-10", "2023-03-20", "2023-04-05", "2023-11-12"]),
        "Product": ["Laptop Pro", "Mouse", "Monitor 4K", "Laptop Pro", "Desk"],
        "Category": ["Technology", "Technology", "Technology", "Technology", "Furniture"],
        "Quantity": [2, 10, 1, 1, 3],
        "Unit_Price": [1000.0, 20.0, 400.0, 1000.0, 200.0],
        "Sales": [2000.0, 200.0, 400.0, 1000.0, 600.0],
        "Region": ["North", "North", "South", "East", "West"],
    }
    return pd.DataFrame(data)


def test_calculate_kpis(sample_sales_df):
    kpis = analysis.calculate_kpis(sample_sales_df)
    assert kpis["total_sales"] == 4200.0
    assert kpis["total_quantity"] == 17
    assert kpis["total_transactions"] == 5
    assert kpis["average_sale"] == 840.0
    assert kpis["best_product"] == "Laptop Pro"
    assert kpis["best_category"] == "Technology"


def test_monthly_and_quarterly_sales(sample_sales_df):
    monthly = analysis.get_monthly_sales(sample_sales_df)
    assert len(monthly) == 5  # Jan, Feb, Mar, Apr, Nov
    assert "Year_Month" in monthly.columns
    assert "Sales" in monthly.columns

    quarterly = analysis.get_quarterly_sales(sample_sales_df)
    assert "Year_Quarter" in quarterly.columns
    assert "2023Q1" in list(quarterly["Year_Quarter"])
    assert "2023Q4" in list(quarterly["Year_Quarter"])


def test_top_products(sample_sales_df):
    top_prods = analysis.get_top_products(sample_sales_df, top_n=2)
    assert len(top_prods) == 2
    assert top_prods.iloc[0]["Product"] == "Laptop Pro"
    assert top_prods.iloc[0]["Sales"] == 3000.0


def test_date_range_filtering(sample_sales_df):
    filtered = analysis.filter_by_date_range(sample_sales_df, "2023-01-01", "2023-02-28")
    assert len(filtered) == 2
    assert list(filtered["Product"]) == ["Laptop Pro", "Mouse"]
