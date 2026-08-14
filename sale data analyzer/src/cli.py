"""Command-Line Interface and interactive user terminal menus."""

import sys
from datetime import datetime
from typing import Tuple, Optional
import pandas as pd

from src import analysis, prediction


def print_banner():
    """Display stylized header banner."""
    print("=" * 60)
    print("               SALES DATA ANALYZER               ")
    print("   Enterprise Retail Analytics & Sales Forecasting")
    print("=" * 60)


def print_menu():
    """Display main menu options."""
    print("\nSelect an option:")
    print(" [1] Run Complete Analysis & Generate PDF Report (Full Dataset)")
    print(" [2] Run Custom Date Range Analysis & Generate PDF Report")
    print(" [3] View Quick Terminal KPI Summary")
    print(" [4] View Data Cleaning & Integrity Summary")
    print(" [5] Exit")
    print("-" * 60)


def print_kpi_summary(df: pd.DataFrame):
    """Display formatted KPI summary in terminal."""
    kpis = analysis.calculate_kpis(df)
    trend = analysis.analyze_sales_trend(df)
    top_5 = analysis.get_top_products(df, top_n=5)

    print("\n" + "=" * 60)
    print("                     SALES SUMMARY                      ")
    print("=" * 60)
    print(f" Date Range:       {kpis['date_range_start']}  -->  {kpis['date_range_end']}")
    print(f" Total Revenue:    ${kpis['total_sales']:,.2f}")
    print(f" Total Quantity:   {kpis['total_quantity']:,} units")
    print(f" Transactions:     {kpis['total_transactions']:,}")
    print(f" Average Sale:     ${kpis['average_sale']:,.2f}")
    print(f" Min Sale:         ${kpis['min_sale']:,.2f}  |  Max Sale: ${kpis['max_sale']:,.2f}")
    print(f" Best Product:     {kpis['best_product']} (${kpis['best_product_sales']:,.2f})")
    print(f" Best Category:    {kpis['best_category']} (${kpis['best_category_sales']:,.2f})")
    print(f" Best Region:      {kpis['best_region']} (${kpis['best_region_sales']:,.2f})")
    print(f" Sales Trend:      {trend['trend_direction']} ({trend['growth_rate_pct']:+.2f}%)")
    print("-" * 60)

    print("\nTOP 5 BEST-SELLING PRODUCTS:")
    print(f"{'Rank':<5} | {'Product':<32} | {'Category':<20} | {'Sales':<12} | {'Quantity':<8}")
    print("-" * 85)
    for _, row in top_5.iterrows():
        print(f"#{int(row['Rank']):<4} | {str(row['Product']):<32} | {str(row['Category']):<20} | ${row['Sales']:>10,.2f} | {int(row['Quantity']):>8,}")
    print("=" * 85)


def print_prediction_summary(pred_result: dict):
    """Display regression forecast in terminal."""
    print("\n" + "=" * 60)
    print("              NEXT MONTH SALES PREDICTION               ")
    print("=" * 60)
    if pred_result.get("is_valid", False):
        print(f" Forecast Period:  {pred_result['next_period_label']}")
        print(f" Predicted Sales:  ${pred_result['predicted_sales']:,.2f}")
        print(f" Model:            {pred_result['model_description']}")
        print(f" Model Fit (R²):   {pred_result['r2_score']:.4f}")
        print(f" Growth Slope:     ${pred_result['slope']:+,.2f} per month")
        print(f" Equation:         {pred_result.get('equation', '')}")
    else:
        print(f" Prediction Warning: {pred_result.get('error_message', 'Prediction unavailable.')}")
    print("-" * 60)
    print(" NOTICE:")
    print(f" {pred_result.get('disclaimer', '')}")
    print("=" * 60)


def print_cleaning_summary(summary: dict):
    """Display data cleaning metrics."""
    print("\n" + "=" * 60)
    print("            DATA CLEANING & INTEGRITY REPORT            ")
    print("=" * 60)
    print(f" Raw Rows Loaded:        {summary.get('rows_before', 0):,}")
    print(f" Duplicate Rows Removed: {summary.get('duplicates_removed', 0):,}")
    print(f" Cleaned Valid Rows:     {summary.get('rows_after', 0):,}")
    print(f" Date Span:              {summary.get('min_date', 'N/A')} to {summary.get('max_date', 'N/A')}")
    print("\n Missing Values Detected (Raw):")
    for col, count in summary.get("missing_before", {}).items():
        if count > 0:
            print(f"   - {col:<15}: {count} missing (handled)")
    print("=" * 60)


def prompt_custom_date_range(min_date_str: str, max_date_str: str) -> Tuple[str, str]:
    """Prompt user for a valid start and end date with validation loop."""
    print(f"\nAvailable data range: {min_date_str}  -->  {max_date_str}")
    min_dt = datetime.strptime(min_date_str, "%Y-%m-%d")
    max_dt = datetime.strptime(max_date_str, "%Y-%m-%d")

    while True:
        try:
            start_input = input("\nEnter start date (YYYY-MM-DD) [or press Enter for min]: ").strip()
            if not start_input:
                start_date = min_date_str
            else:
                start_dt = datetime.strptime(start_input, "%Y-%m-%d")
                if start_dt > max_dt:
                    print(f" Error: Start date {start_input} is after the latest dataset date ({max_date_str}).")
                    continue
                start_date = start_input

            end_input = input("Enter end date   (YYYY-MM-DD) [or press Enter for max]: ").strip()
            if not end_input:
                end_date = max_date_str
            else:
                end_dt = datetime.strptime(end_input, "%Y-%m-%d")
                if end_dt < min_dt:
                    print(f" Error: End date {end_input} is before the earliest dataset date ({min_date_str}).")
                    continue
                end_date = end_input

            # Check start <= end
            start_dt_val = datetime.strptime(start_date, "%Y-%m-%d")
            end_dt_val = datetime.strptime(end_date, "%Y-%m-%d")
            if start_dt_val > end_dt_val:
                print(f" Error: Start date ({start_date}) cannot be after end date ({end_date}). Please re-enter.")
                continue

            return start_date, end_date

        except ValueError:
            print(" Invalid date format. Please use the YYYY-MM-DD format (e.g. 2023-01-01).")
        except (KeyboardInterrupt, EOFError):
            print("\nInput cancelled. Returning default full range.")
            return min_date_str, max_date_str


def print_completion_banner(cleaned_path, charts_dir, report_path, log_path):
    """Print standard finish summary with paths."""
    print("\n" + "=" * 60)
    print("              ANALYSIS COMPLETED SUCCESSFULLY           ")
    print("=" * 60)
    print(f"\n Cleaned Data:\n   {cleaned_path}")
    print(f"\n Charts Directory:\n   {charts_dir}")
    print(f"\n PDF Report:\n   {report_path}")
    print(f"\n Application Logs:\n   {log_path}")
    print("=" * 60 + "\n")
