"""Unit tests for linear regression forecasting module."""

import pytest
import pandas as pd
from src import prediction


def test_predict_next_month_sales_valid():
    # 6 sequential monthly periods with increasing trend
    dates = pd.date_range(start="2024-01-01", periods=6, freq="MS")
    sales = [10000.0, 12000.0, 14000.0, 16000.0, 18000.0, 20000.0]

    df = pd.DataFrame({
        "Date": dates,
        "Quantity": [10] * 6,
        "Unit_Price": [100.0] * 6,
        "Sales": sales,
        "Product": ["Item A"] * 6,
        "Category": ["Tech"] * 6,
        "Region": ["North"] * 6,
    })

    result = prediction.predict_next_month_sales(df)

    assert result["is_valid"] is True
    assert result["r2_score"] > 0.99  # Perfectly linear data
    assert result["slope"] == pytest.approx(2000.0, rel=1e-2)
    assert result["predicted_sales"] == pytest.approx(22000.0, rel=1e-2)
    assert result["next_period_label"] == "2024-07"


def test_predict_insufficient_data():
    # Only 1 month of data
    df = pd.DataFrame({
        "Date": pd.to_datetime(["2024-01-15"]),
        "Quantity": [2],
        "Unit_Price": [50.0],
        "Sales": [100.0],
        "Product": ["Item A"],
        "Category": ["Tech"],
        "Region": ["North"],
    })

    result = prediction.predict_next_month_sales(df)
    assert result["is_valid"] is False
    assert "Insufficient historical data" in result["error_message"]
