"""Unit tests for edge cases: missing region, single product, small datasets, etc."""

import pytest
import pandas as pd
import numpy as np
from src import data_cleaning, analysis, prediction, visualization, report_generator
import config


def test_csv_without_region(tmp_path):
    """Test full pipeline when Region column is absent in user's CSV."""
    raw_df = pd.DataFrame({
        "Date": ["2023-01-15", "2023-02-15", "2023-03-15", "2023-04-15"],
        "Product": ["Widget A", "Widget B", "Widget A", "Widget B"],
        "Category": ["Hardware", "Hardware", "Hardware", "Hardware"],
        "Quantity": [10, 5, 8, 12],
        "Unit_Price": [20.0, 50.0, 20.0, 50.0],
        "Sales": [200.0, 250.0, 160.0, 600.0],
    })
    csv_file = tmp_path / "no_region.csv"
    raw_df.to_csv(csv_file, index=False)

    cleaned_df, summary = data_cleaning.clean_sales_data(csv_file)
    assert summary["has_region"] is False
    assert "Region" not in cleaned_df.columns

    kpis = analysis.calculate_kpis(cleaned_df)
    assert kpis["best_region"] == "N/A"
    assert kpis["has_region"] is False

    reg_sales = analysis.get_regional_sales(cleaned_df)
    assert reg_sales.empty

    # Chart generation shouldn't crash
    chart_paths = visualization.generate_all_charts(cleaned_df)
    assert chart_paths["regional_sales"] is None

    # PDF generation shouldn't crash
    pred_res = prediction.predict_next_month_sales(cleaned_df)
    pdf_path = report_generator.generate_pdf_report(
        df=cleaned_df,
        cleaning_summary=summary,
        pred_result=pred_res,
        chart_paths=chart_paths,
        dataset_name="no_region.csv",
        output_path=tmp_path / "no_region_report.pdf",
    )
    assert pdf_path.exists()


def test_insufficient_monthly_observations(tmp_path):
    """Test regression when observations < 3 months."""
    raw_df = pd.DataFrame({
        "Date": ["2024-01-10", "2024-01-20"],
        "Product": ["Tool A", "Tool B"],
        "Quantity": [1, 2],
        "Unit_Price": [100.0, 50.0],
        "Sales": [100.0, 100.0],
    })
    cleaned_df, summary = data_cleaning.clean_sales_data(raw_df)
    pred_res = prediction.predict_next_month_sales(cleaned_df)

    assert pred_res["is_valid"] is False
    assert "Insufficient historical data" in pred_res["error_message"]


def test_single_product_and_category(tmp_path):
    """Test dataset containing only one product and one category."""
    dates = pd.date_range("2023-01-01", periods=6, freq="MS")
    raw_df = pd.DataFrame({
        "Date": dates,
        "Product": ["Solo Product"] * 6,
        "Category": ["Solo Category"] * 6,
        "Quantity": [5] * 6,
        "Unit_Price": [10.0] * 6,
        "Sales": [50.0] * 6,
    })
    cleaned_df, summary = data_cleaning.clean_sales_data(raw_df)
    top_5 = analysis.get_top_products(cleaned_df, top_n=5)
    assert len(top_5) == 1
    assert top_5.iloc[0]["Product"] == "Solo Product"

    cat_sales = analysis.get_category_sales(cleaned_df)
    assert len(cat_sales) == 1
    assert cat_sales.iloc[0]["Percentage"] == 100.0
