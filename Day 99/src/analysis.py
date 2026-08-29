"""Sales data analysis module providing KPIs, aggregations, trend analysis, and correlations."""

import logging
from typing import Dict, Any, List
import pandas as pd
import numpy as np

logger = logging.getLogger("sales_analyzer.analysis")


def filter_by_date_range(df: pd.DataFrame, start_date: str, end_date: str) -> pd.DataFrame:
    """Filter dataframe within a specific date range [start_date, end_date] inclusive."""
    if df.empty or "Date" not in df.columns:
        return df

    start_ts = pd.to_datetime(start_date)
    end_ts = pd.to_datetime(end_date)

    filtered_df = df[(df["Date"] >= start_ts) & (df["Date"] <= end_ts)].copy()
    logger.info(f"Filtered dataset from {start_date} to {end_date}: {len(filtered_df)} records found")
    return filtered_df.reset_index(drop=True)


def calculate_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """Calculate core high-level sales KPIs."""
    if df.empty:
        return {
            "total_sales": 0.0,
            "total_quantity": 0,
            "total_transactions": 0,
            "average_sale": 0.0,
            "min_sale": 0.0,
            "max_sale": 0.0,
            "best_product": "N/A",
            "best_product_sales": 0.0,
            "best_category": "N/A",
            "best_category_sales": 0.0,
            "best_region": "N/A",
            "best_region_sales": 0.0,
            "date_range_start": "N/A",
            "date_range_end": "N/A",
            "avg_monthly_sales": 0.0,
            "has_region": False,
        }

    total_sales = float(df["Sales"].sum()) if "Sales" in df.columns else 0.0
    total_qty = int(df["Quantity"].sum()) if "Quantity" in df.columns else 0
    total_trans = int(len(df))
    avg_sale = float(df["Sales"].mean()) if "Sales" in df.columns and len(df) > 0 else 0.0
    min_sale = float(df["Sales"].min()) if "Sales" in df.columns and len(df) > 0 else 0.0
    max_sale = float(df["Sales"].max()) if "Sales" in df.columns and len(df) > 0 else 0.0

    # Best product by revenue
    if "Product" in df.columns and "Sales" in df.columns:
        product_group = df.groupby("Product")["Sales"].sum()
        best_product = str(product_group.idxmax()) if not product_group.empty else "N/A"
        best_product_sales = float(product_group.max()) if not product_group.empty else 0.0
    else:
        best_product = "N/A"
        best_product_sales = 0.0

    # Best category
    if "Category" in df.columns and "Sales" in df.columns:
        cat_group = df.groupby("Category")["Sales"].sum()
        best_category = str(cat_group.idxmax()) if not cat_group.empty else "N/A"
        best_category_sales = float(cat_group.max()) if not cat_group.empty else 0.0
    else:
        best_category = "N/A"
        best_category_sales = 0.0

    # Best region
    has_region = "Region" in df.columns
    if has_region and "Sales" in df.columns:
        reg_group = df.groupby("Region")["Sales"].sum()
        best_region = str(reg_group.idxmax()) if not reg_group.empty else "N/A"
        best_region_sales = float(reg_group.max()) if not reg_group.empty else 0.0
    else:
        best_region = "N/A"
        best_region_sales = 0.0

    # Date range
    min_date = df["Date"].min().strftime("%Y-%m-%d") if "Date" in df.columns and not df["Date"].isna().all() else "N/A"
    max_date = df["Date"].max().strftime("%Y-%m-%d") if "Date" in df.columns and not df["Date"].isna().all() else "N/A"

    # Monthly average sales
    monthly_df = get_monthly_sales(df)
    avg_monthly_sales = float(monthly_df["Sales"].mean()) if not monthly_df.empty and "Sales" in monthly_df.columns else 0.0

    return {
        "total_sales": total_sales,
        "total_quantity": total_qty,
        "total_transactions": total_trans,
        "average_sale": avg_sale,
        "min_sale": min_sale,
        "max_sale": max_sale,
        "best_product": best_product,
        "best_product_sales": best_product_sales,
        "best_category": best_category,
        "best_category_sales": best_category_sales,
        "best_region": best_region,
        "best_region_sales": best_region_sales,
        "date_range_start": min_date,
        "date_range_end": max_date,
        "avg_monthly_sales": avg_monthly_sales,
        "has_region": has_region,
    }


def get_monthly_sales(df: pd.DataFrame) -> pd.DataFrame:
    """Group sales chronologically by Year-Month."""
    if df.empty or "Date" not in df.columns:
        return pd.DataFrame(columns=["Year_Month", "Sales", "Quantity", "Average_Sale", "Transactions"])

    temp = df.copy()
    temp["Year_Month"] = temp["Date"].dt.to_period("M").astype(str)

    monthly = temp.groupby("Year_Month").agg(
        Sales=("Sales", "sum"),
        Quantity=("Quantity", "sum"),
        Average_Sale=("Sales", "mean"),
        Transactions=("Sales", "count"),
    ).reset_index()

    monthly["Sales"] = monthly["Sales"].round(2)
    monthly["Average_Sale"] = monthly["Average_Sale"].round(2)
    monthly = monthly.sort_values(by="Year_Month").reset_index(drop=True)
    return monthly


def get_quarterly_sales(df: pd.DataFrame) -> pd.DataFrame:
    """Group sales chronologically by Year-Quarter (e.g. 2024Q1)."""
    if df.empty or "Date" not in df.columns:
        return pd.DataFrame(columns=["Year_Quarter", "Sales", "Quantity", "Average_Sale", "Transactions"])

    temp = df.copy()
    temp["Year_Quarter"] = temp["Date"].dt.to_period("Q").astype(str)

    quarterly = temp.groupby("Year_Quarter").agg(
        Sales=("Sales", "sum"),
        Quantity=("Quantity", "sum"),
        Average_Sale=("Sales", "mean"),
        Transactions=("Sales", "count"),
    ).reset_index()

    quarterly["Sales"] = quarterly["Sales"].round(2)
    quarterly["Average_Sale"] = quarterly["Average_Sale"].round(2)
    quarterly = quarterly.sort_values(by="Year_Quarter").reset_index(drop=True)
    return quarterly


def get_top_products(df: pd.DataFrame, top_n: int = 5) -> pd.DataFrame:
    """Identify top N best-selling products based on total sales revenue."""
    if df.empty or "Product" not in df.columns:
        return pd.DataFrame(columns=["Rank", "Product", "Category", "Sales", "Quantity", "Average_Price"])

    group_cols = ["Product"]
    if "Category" in df.columns:
        group_cols.append("Category")

    agg_dict = {
        "Sales": ("Sales", "sum"),
        "Quantity": ("Quantity", "sum"),
    }
    if "Unit_Price" in df.columns:
        agg_dict["Average_Price"] = ("Unit_Price", "mean")

    grouped = df.groupby(group_cols).agg(**agg_dict).reset_index()

    if "Category" not in grouped.columns:
        grouped["Category"] = "General"
    if "Average_Price" not in grouped.columns:
        grouped["Average_Price"] = (grouped["Sales"] / grouped["Quantity"]).round(2)

    top_df = grouped.sort_values(by="Sales", ascending=False).head(top_n).reset_index(drop=True)
    top_df.insert(0, "Rank", range(1, len(top_df) + 1))
    top_df["Sales"] = top_df["Sales"].round(2)
    top_df["Average_Price"] = top_df["Average_Price"].round(2)
    return top_df


def get_category_sales(df: pd.DataFrame) -> pd.DataFrame:
    """Compute total revenue, quantity, and market share by category."""
    if df.empty or "Category" not in df.columns:
        return pd.DataFrame(columns=["Category", "Sales", "Quantity", "Percentage"])

    cat_df = df.groupby("Category").agg(
        Sales=("Sales", "sum"),
        Quantity=("Quantity", "sum"),
        Transactions=("Sales", "count"),
    ).reset_index()

    total_sales = cat_df["Sales"].sum()
    cat_df["Percentage"] = (cat_df["Sales"] / total_sales * 100).round(2) if total_sales > 0 else 0.0
    cat_df["Sales"] = cat_df["Sales"].round(2)
    return cat_df.sort_values(by="Sales", ascending=False).reset_index(drop=True)


def get_regional_sales(df: pd.DataFrame) -> pd.DataFrame:
    """Compute total revenue, quantity, and market share by region."""
    if df.empty or "Region" not in df.columns:
        return pd.DataFrame(columns=["Region", "Sales", "Quantity", "Percentage"])

    reg_df = df.groupby("Region").agg(
        Sales=("Sales", "sum"),
        Quantity=("Quantity", "sum"),
        Transactions=("Sales", "count"),
    ).reset_index()

    total_sales = reg_df["Sales"].sum()
    reg_df["Percentage"] = (reg_df["Sales"] / total_sales * 100).round(2) if total_sales > 0 else 0.0
    reg_df["Sales"] = reg_df["Sales"].round(2)
    return reg_df.sort_values(by="Sales", ascending=False).reset_index(drop=True)


def analyze_sales_trend(df: pd.DataFrame) -> Dict[str, Any]:
    """Analyze sales trend by comparing historical early period vs recent period."""
    monthly = get_monthly_sales(df)
    n_months = len(monthly)

    if n_months < 2:
        return {
            "trend_direction": "Stable / Insufficient Data",
            "growth_rate_pct": 0.0,
            "early_avg_sales": float(df["Sales"].mean()) if not df.empty and "Sales" in df.columns else 0.0,
            "recent_avg_sales": float(df["Sales"].mean()) if not df.empty and "Sales" in df.columns else 0.0,
            "description": "Insufficient monthly periods to establish longitudinal trend.",
        }

    half_point = max(1, n_months // 2)
    early_period = monthly.iloc[:half_point]
    recent_period = monthly.iloc[half_point:]

    early_avg = float(early_period["Sales"].mean())
    recent_avg = float(recent_period["Sales"].mean())

    if early_avg > 0:
        growth_pct = ((recent_avg - early_avg) / early_avg) * 100.0
    else:
        growth_pct = 0.0

    if growth_pct > 5.0:
        direction = "Increasing"
    elif growth_pct < -5.0:
        direction = "Decreasing"
    else:
        direction = "Relatively stable"

    return {
        "trend_direction": direction,
        "growth_rate_pct": round(growth_pct, 2),
        "early_avg_sales": round(early_avg, 2),
        "recent_avg_sales": round(recent_avg, 2),
        "early_period_label": f"{early_period.iloc[0]['Year_Month']} to {early_period.iloc[-1]['Year_Month']}",
        "recent_period_label": f"{recent_period.iloc[0]['Year_Month']} to {recent_period.iloc[-1]['Year_Month']}",
        "description": f"Sales are {direction.lower()} with a {growth_pct:+.2f}% change comparing early period to recent period.",
    }


def compute_correlations(df: pd.DataFrame) -> pd.DataFrame:
    """Compute Pearson correlation matrix dynamically for available numeric columns."""
    if df.empty:
        return pd.DataFrame()
    numeric_cols = [c for c in ["Quantity", "Unit_Price", "Sales"] if c in df.columns and pd.api.types.is_numeric_dtype(df[c])]
    if len(numeric_cols) < 2:
        return pd.DataFrame()
    return df[numeric_cols].corr().round(4)
