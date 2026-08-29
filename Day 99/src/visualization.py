"""Data visualization module using Matplotlib and Seaborn for sales reporting."""

import logging
from pathlib import Path
from typing import Optional, Dict, Any
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import pandas as pd
import numpy as np

import config
from src import analysis

logger = logging.getLogger("sales_analyzer.visualization")

# Apply clean professional styling defaults
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica", "sans-serif"]
plt.rcParams["axes.edgecolor"] = "#CBD5E1"
plt.rcParams["axes.linewidth"] = 0.8


def _currency_formatter(x, pos):
    """Format large numbers into clean currency strings ($12.5k, $1.2M)."""
    if abs(x) >= 1e6:
        return f"${x*1e-6:.1f}M"
    elif abs(x) >= 1e3:
        return f"${x*1e-3:.0f}k"
    else:
        return f"${x:.0f}"


def plot_monthly_sales_trend(df: pd.DataFrame, output_path: Path = config.CHART_MONTHLY_TREND) -> Path:
    """Generate monthly sales trend line chart."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    monthly_df = analysis.get_monthly_sales(df)

    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)

    if monthly_df.empty or "Sales" not in monthly_df.columns:
        ax.text(0.5, 0.5, "No Monthly Data Available", ha="center", va="center")
    else:
        x = range(len(monthly_df))
        ax.plot(
            x,
            monthly_df["Sales"],
            marker="o",
            markersize=4,
            linewidth=2.2,
            color=config.STYLE_PALETTE["primary"],
            label="Monthly Revenue",
        )
        ax.fill_between(x, monthly_df["Sales"], alpha=0.15, color=config.STYLE_PALETTE["secondary"])

        step = max(1, len(monthly_df) // 10)
        tick_locs = list(range(0, len(monthly_df), step))
        if len(monthly_df) - 1 not in tick_locs:
            tick_locs.append(len(monthly_df) - 1)
        ax.set_xticks(tick_locs)
        ax.set_xticklabels([monthly_df["Year_Month"].iloc[i] for i in tick_locs], rotation=35, ha="right", fontsize=9)
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(_currency_formatter))

    ax.set_title("Monthly Sales Trend", fontsize=13, fontweight="bold", pad=14, color=config.STYLE_PALETTE["dark"])
    ax.set_xlabel("Month", fontsize=10, labelpad=8, fontweight="medium")
    ax.set_ylabel("Sales ($)", fontsize=10, labelpad=8, fontweight="medium")
    ax.grid(True, linestyle="--", alpha=0.5, color=config.STYLE_PALETTE["grid"])
    fig.tight_layout()

    plt.savefig(output_path, dpi=300)
    plt.close(fig)
    logger.info(f"Saved monthly sales trend chart to {output_path}")
    return output_path


def plot_quarterly_sales(df: pd.DataFrame, output_path: Path = config.CHART_QUARTERLY_SALES) -> Path:
    """Generate quarterly sales bar chart."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    quarterly_df = analysis.get_quarterly_sales(df)

    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)

    if quarterly_df.empty or "Sales" not in quarterly_df.columns:
        ax.text(0.5, 0.5, "No Quarterly Data Available", ha="center", va="center")
    else:
        bars = ax.bar(
            quarterly_df["Year_Quarter"],
            quarterly_df["Sales"],
            color=config.STYLE_PALETTE["secondary"],
            edgecolor="#0369A1",
            width=0.6,
            alpha=0.9,
        )

        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.annotate(
                    f"${height/1000:.1f}k" if height >= 1000 else f"${height:.0f}",
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 4),
                    textcoords="offset points",
                    ha="center",
                    va="bottom",
                    fontsize=8,
                    fontweight="semibold",
                    color=config.STYLE_PALETTE["dark"],
                )

        ax.yaxis.set_major_formatter(ticker.FuncFormatter(_currency_formatter))
        plt.xticks(rotation=45, ha="right", fontsize=9)

    ax.set_title("Quarterly Sales Performance", fontsize=13, fontweight="bold", pad=14, color=config.STYLE_PALETTE["dark"])
    ax.set_xlabel("Quarter", fontsize=10, labelpad=8, fontweight="medium")
    ax.set_ylabel("Total Sales ($)", fontsize=10, labelpad=8, fontweight="medium")
    ax.grid(True, axis="y", linestyle="--", alpha=0.5, color=config.STYLE_PALETTE["grid"])
    fig.tight_layout()

    plt.savefig(output_path, dpi=300)
    plt.close(fig)
    logger.info(f"Saved quarterly sales chart to {output_path}")
    return output_path


def plot_top_products(df: pd.DataFrame, output_path: Path = config.CHART_TOP_PRODUCTS, top_n: int = 5) -> Path:
    """Generate horizontal bar chart for top N best-selling products."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    top_df = analysis.get_top_products(df, top_n=top_n)

    fig, ax = plt.subplots(figsize=(9, 4.8), dpi=300)

    if top_df.empty or "Sales" not in top_df.columns:
        ax.text(0.5, 0.5, "No Product Data Available", ha="center", va="center")
    else:
        plot_df = top_df.iloc[::-1].reset_index(drop=True)
        bars = ax.barh(
            plot_df["Product"],
            plot_df["Sales"],
            color=config.STYLE_PALETTE["primary"],
            edgecolor="#1E293B",
            height=0.55,
        )

        for bar in bars:
            width = bar.get_width()
            ax.annotate(
                f" ${_currency_formatter(width, None)[1:]}",
                xy=(width, bar.get_y() + bar.get_height() / 2),
                xytext=(5, 0),
                textcoords="offset points",
                ha="left",
                va="center",
                fontsize=9,
                fontweight="bold",
                color=config.STYLE_PALETTE["dark"],
            )

        ax.xaxis.set_major_formatter(ticker.FuncFormatter(_currency_formatter))
        max_val = max(top_df["Sales"]) if not top_df["Sales"].empty else 1.0
        ax.set_xlim(0, max_val * 1.18 if max_val > 0 else 100)

    ax.set_title(f"Top {len(top_df)} Best-Selling Products by Revenue", fontsize=13, fontweight="bold", pad=14, color=config.STYLE_PALETTE["dark"])
    ax.set_xlabel("Total Sales ($)", fontsize=10, labelpad=8, fontweight="medium")
    ax.set_ylabel("Product", fontsize=10, labelpad=8, fontweight="medium")
    ax.grid(True, axis="x", linestyle="--", alpha=0.5, color=config.STYLE_PALETTE["grid"])
    fig.tight_layout()

    plt.savefig(output_path, dpi=300)
    plt.close(fig)
    logger.info(f"Saved top products chart to {output_path}")
    return output_path


def plot_category_sales(df: pd.DataFrame, output_path: Path = config.CHART_CATEGORY_SALES) -> Path:
    """Generate bar chart of sales by product category."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cat_df = analysis.get_category_sales(df)

    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=300)

    if cat_df.empty or "Sales" not in cat_df.columns:
        ax.text(0.5, 0.5, "No Category Data Available", ha="center", va="center")
    else:
        colors = [config.STYLE_PALETTE["primary"], config.STYLE_PALETTE["secondary"], config.STYLE_PALETTE["accent"], config.STYLE_PALETTE["success"]]
        bar_colors = [colors[i % len(colors)] for i in range(len(cat_df))]

        bars = ax.bar(
            cat_df["Category"],
            cat_df["Sales"],
            color=bar_colors,
            edgecolor="#334155",
            width=0.5,
        )

        for bar, pct in zip(bars, cat_df["Percentage"]):
            height = bar.get_height()
            ax.annotate(
                f"${height/1000:.1f}k\n({pct:.1f}%)" if height >= 1000 else f"${height:.0f}\n({pct:.1f}%)",
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 4),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=8.5,
                fontweight="semibold",
                color=config.STYLE_PALETTE["dark"],
            )

        ax.yaxis.set_major_formatter(ticker.FuncFormatter(_currency_formatter))
        max_val = max(cat_df["Sales"]) if not cat_df["Sales"].empty else 1.0
        ax.set_ylim(0, max_val * 1.18 if max_val > 0 else 100)

    ax.set_title("Sales by Product Category", fontsize=13, fontweight="bold", pad=14, color=config.STYLE_PALETTE["dark"])
    ax.set_xlabel("Category", fontsize=10, labelpad=8, fontweight="medium")
    ax.set_ylabel("Total Sales ($)", fontsize=10, labelpad=8, fontweight="medium")
    ax.grid(True, axis="y", linestyle="--", alpha=0.5, color=config.STYLE_PALETTE["grid"])
    fig.tight_layout()

    plt.savefig(output_path, dpi=300)
    plt.close(fig)
    logger.info(f"Saved category sales chart to {output_path}")
    return output_path


def plot_regional_sales(df: pd.DataFrame, output_path: Path = config.CHART_REGIONAL_SALES) -> Optional[Path]:
    """Generate bar chart of sales by geographic region if region exists."""
    if "Region" not in df.columns:
        return None

    output_path.parent.mkdir(parents=True, exist_ok=True)
    reg_df = analysis.get_regional_sales(df)

    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=300)

    if reg_df.empty or "Sales" not in reg_df.columns:
        ax.text(0.5, 0.5, "No Regional Data Available", ha="center", va="center")
    else:
        bars = ax.bar(
            reg_df["Region"],
            reg_df["Sales"],
            color="#3B82F6",
            edgecolor="#1D4ED8",
            width=0.5,
        )

        for bar, pct in zip(bars, reg_df["Percentage"]):
            height = bar.get_height()
            ax.annotate(
                f"${height/1000:.1f}k\n({pct:.1f}%)" if height >= 1000 else f"${height:.0f}\n({pct:.1f}%)",
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 4),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=8.5,
                fontweight="semibold",
                color=config.STYLE_PALETTE["dark"],
            )

        ax.yaxis.set_major_formatter(ticker.FuncFormatter(_currency_formatter))
        max_val = max(reg_df["Sales"]) if not reg_df["Sales"].empty else 1.0
        ax.set_ylim(0, max_val * 1.18 if max_val > 0 else 100)

    ax.set_title("Sales Distribution by Region", fontsize=13, fontweight="bold", pad=14, color=config.STYLE_PALETTE["dark"])
    ax.set_xlabel("Region", fontsize=10, labelpad=8, fontweight="medium")
    ax.set_ylabel("Total Sales ($)", fontsize=10, labelpad=8, fontweight="medium")
    ax.grid(True, axis="y", linestyle="--", alpha=0.5, color=config.STYLE_PALETTE["grid"])
    fig.tight_layout()

    plt.savefig(output_path, dpi=300)
    plt.close(fig)
    logger.info(f"Saved regional sales chart to {output_path}")
    return output_path


def plot_correlation_heatmap(df: pd.DataFrame, output_path: Path = config.CHART_CORRELATION_HEATMAP) -> Path:
    """Generate annotated correlation heatmap for numeric features."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    corr_df = analysis.compute_correlations(df)

    fig, ax = plt.subplots(figsize=(6.5, 5), dpi=300)

    if corr_df.empty:
        ax.text(0.5, 0.5, "Insufficient numeric features for correlation", ha="center", va="center")
    else:
        sns.heatmap(
            corr_df,
            annot=True,
            fmt=".3f",
            cmap="Blues",
            cbar=True,
            square=True,
            linewidths=1.0,
            linecolor="white",
            annot_kws={"size": 10, "weight": "bold"},
            ax=ax,
        )

    ax.set_title("Numerical Variables Correlation Matrix", fontsize=12, fontweight="bold", pad=12, color=config.STYLE_PALETTE["dark"])
    fig.tight_layout()

    plt.savefig(output_path, dpi=300)
    plt.close(fig)
    logger.info(f"Saved correlation heatmap to {output_path}")
    return output_path


def plot_prediction(
    monthly_df: pd.DataFrame,
    pred_result: Dict[str, Any],
    output_path: Path = config.CHART_PREDICTION
) -> Path:
    """Generate regression chart showing historical monthly sales and prediction."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)

    if monthly_df.empty or not pred_result.get("is_valid", False):
        ax.text(0.5, 0.5, "Insufficient data for regression prediction plot", ha="center", va="center")
    else:
        n = len(monthly_df)
        x_hist = np.arange(1, n + 1)
        y_hist = monthly_df["Sales"].values

        ax.plot(
            x_hist,
            y_hist,
            marker="o",
            color=config.STYLE_PALETTE["primary"],
            linewidth=2,
            label="Historical Monthly Sales",
        )

        x_all = np.arange(1, n + 2)
        slope = pred_result["slope"]
        intercept = pred_result["intercept"]
        y_trend = slope * x_all + intercept

        ax.plot(
            x_all,
            y_trend,
            linestyle="--",
            color="#D97706",
            linewidth=2,
            label=f"Linear Trendline (R² = {pred_result['r2_score']:.2f})",
        )

        next_x = n + 1
        next_y = pred_result["predicted_sales"]
        ax.scatter(
            [next_x],
            [next_y],
            color=config.STYLE_PALETTE["danger"],
            s=120,
            zorder=5,
            edgecolors="black",
            linewidths=1.5,
            label=f"Forecast ({pred_result['next_period_label']}): ${next_y:,.0f}",
        )

        ax.annotate(
            f"Forecast:\n${next_y:,.0f}",
            xy=(next_x, next_y),
            xytext=(-35, 15),
            textcoords="offset points",
            fontweight="bold",
            color=config.STYLE_PALETTE["danger"],
            bbox=dict(boxstyle="round,pad=0.3", fc="#FEF2F2", ec=config.STYLE_PALETTE["danger"], lw=1),
            arrowprops=dict(arrowstyle="->", color=config.STYLE_PALETTE["danger"], lw=1.2),
        )

        all_labels = list(monthly_df["Year_Month"]) + [pred_result["next_period_label"]]
        step = max(1, len(all_labels) // 10)
        tick_locs = list(range(1, len(all_labels) + 1, step))
        if len(all_labels) not in tick_locs:
            tick_locs.append(len(all_labels))

        ax.set_xticks(tick_locs)
        ax.set_xticklabels([all_labels[i - 1] for i in tick_locs], rotation=35, ha="right", fontsize=9)
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(_currency_formatter))
        ax.legend(loc="upper left", frameon=True, facecolor="white", edgecolor="#E2E8F0")

    ax.set_title("Monthly Sales — Linear Regression Prediction", fontsize=13, fontweight="bold", pad=14, color=config.STYLE_PALETTE["dark"])
    ax.set_xlabel("Month", fontsize=10, labelpad=8, fontweight="medium")
    ax.set_ylabel("Sales ($)", fontsize=10, labelpad=8, fontweight="medium")
    ax.grid(True, linestyle="--", alpha=0.5, color=config.STYLE_PALETTE["grid"])
    fig.tight_layout()

    plt.savefig(output_path, dpi=300)
    plt.close(fig)
    logger.info(f"Saved prediction chart to {output_path}")
    return output_path


def generate_all_charts(
    df: pd.DataFrame,
    pred_result: Optional[Dict[str, Any]] = None
) -> Dict[str, Optional[Path]]:
    """Generate and save all analytical charts."""
    logger.info("Generating all visualization charts...")
    config.CHARTS_DIR.mkdir(parents=True, exist_ok=True)

    chart_paths = {
        "monthly_trend": plot_monthly_sales_trend(df),
        "quarterly_sales": plot_quarterly_sales(df),
        "top_products": plot_top_products(df),
        "category_sales": plot_category_sales(df),
        "regional_sales": plot_regional_sales(df) if "Region" in df.columns else None,
        "correlation_heatmap": plot_correlation_heatmap(df),
    }

    if pred_result is not None:
        monthly_df = analysis.get_monthly_sales(df)
        chart_paths["prediction"] = plot_prediction(monthly_df, pred_result)

    return chart_paths
