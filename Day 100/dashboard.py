"""Sales Data Analyzer - Premium SaaS Business Intelligence & Analytics Dashboard."""

import io
from datetime import datetime, date
from pathlib import Path
from typing import Optional, Dict, Any, Tuple
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

import config
from src import data_cleaning, analysis, visualization, prediction, report_generator

# -----------------------------------------------------------------------------
# Streamlit Page Configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Sales Data Analyzer | Enterprise Business Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------------------------------------
# Custom CSS Design System — Fixed & Improved
# -----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    /* Remove default top padding */
    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 2rem !important;
    }

    .stApp {
        background-color: #F1F5F9;
    }

    /* ── SIDEBAR ──────────────────────────────── */
    section[data-testid="stSidebar"] > div:first-child {
        background-color: #0F172A !important;
    }
    section[data-testid="stSidebar"] {
        background-color: #0F172A !important;
    }
    /* Force ALL sidebar text to light color */
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown li,
    section[data-testid="stSidebar"] .stMarkdown span,
    section[data-testid="stSidebar"] .stMarkdown a,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] small,
    section[data-testid="stSidebar"] div {
        color: #CBD5E1 !important;
    }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] strong,
    section[data-testid="stSidebar"] b {
        color: #FFFFFF !important;
    }
    section[data-testid="stSidebar"] hr {
        border-color: #1E293B !important;
    }
    section[data-testid="stSidebar"] .stButton > button {
        background-color: #1E3A8A !important;
        color: #FFFFFF !important;
        border: 1px solid #2563EB !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        font-size: 0.82rem !important;
    }
    section[data-testid="stSidebar"] .stButton > button:hover {
        background-color: #2563EB !important;
    }

    /* ── HEADER BANNER ───────────────────────── */
    .header-banner {
        background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 100%);
        border-radius: 12px;
        padding: 24px 32px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 16px rgba(15, 23, 42, 0.18);
    }
    .header-left h1 {
        font-size: 1.75rem;
        font-weight: 800;
        color: #FFFFFF;
        letter-spacing: -0.02em;
        margin: 0 0 3px 0;
        line-height: 1.2;
    }
    .header-left .subtitle {
        font-size: 0.92rem;
        font-weight: 600;
        color: #93C5FD;
        margin: 0 0 6px 0;
    }
    .header-left .tagline {
        font-size: 0.82rem;
        color: #94A3B8;
        margin: 0;
    }
    .header-right {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        gap: 10px;
    }
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 5px 13px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        white-space: nowrap;
    }
    .status-waiting  { background-color: rgba(255,255,255,0.1); color: #94A3B8; border: 1px solid rgba(255,255,255,0.15); }
    .status-loaded   { background-color: rgba(59,130,246,0.25); color: #93C5FD; border: 1px solid rgba(59,130,246,0.4); }
    .status-ready    { background-color: rgba(22,163,74,0.25);  color: #86EFAC; border: 1px solid rgba(22,163,74,0.4); }
    /* Workflow Steps shown in header */
    .workflow-steps {
        display: flex;
        align-items: center;
        gap: 4px;
        flex-wrap: wrap;
    }
    .wf-step {
        font-size: 0.72rem;
        font-weight: 600;
        color: #94A3B8;
        padding: 3px 8px;
        border-radius: 4px;
        background: rgba(255,255,255,0.06);
        white-space: nowrap;
    }
    .wf-step.active {
        color: #BFDBFE;
        background: rgba(37,99,235,0.3);
    }
    .wf-arrow { color: #475569; font-size: 0.7rem; }

    /* Compact Dataset Status Bar */
    .dataset-status-bar {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-left: 4px solid #2563EB;
        border-radius: 8px;
        padding: 12px 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 24px;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.03);
    }
    .dataset-info-text {
        font-size: 0.9rem;
        color: #0F172A;
        font-weight: 500;
    }
    .dataset-filename {
        font-weight: 700;
        color: #2563EB;
    }

    /* Section Cards & Headers */
    .section-header-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #0F172A;
        letter-spacing: -0.01em;
        margin-bottom: 2px;
    }
    .section-header-sub {
        font-size: 0.85rem;
        color: #64748B;
        margin-bottom: 16px;
    }

    /* KPI Cards */
    .kpi-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 16px 18px;
        box-shadow: 0 1px 3px 0 rgba(15, 23, 42, 0.04);
        position: relative;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .kpi-card:hover {
        box-shadow: 0 4px 6px -1px rgba(15, 23, 42, 0.08);
    }
    .kpi-label {
        font-size: 0.72rem;
        font-weight: 700;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 1.55rem;
        font-weight: 800;
        color: #0F172A;
        letter-spacing: -0.02em;
        line-height: 1.2;
    }
    .kpi-sub {
        font-size: 0.76rem;
        font-weight: 600;
        color: #16A34A;
        margin-top: 6px;
    }

    /* Insight Cards */
    .insight-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-left: 3.5px solid #2563EB;
        border-radius: 8px;
        padding: 14px 16px;
        height: 100%;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.03);
    }
    .insight-label {
        font-size: 0.72rem;
        font-weight: 700;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    .insight-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #0F172A;
        margin-top: 2px;
        margin-bottom: 4px;
    }
    .insight-desc {
        font-size: 0.8rem;
        color: #475569;
        margin: 0;
    }

    /* Data Quality Scorecard Badges */
    .audit-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 14px;
        text-align: center;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.03);
    }
    .audit-val {
        font-size: 1.35rem;
        font-weight: 800;
        color: #0F172A;
    }
    .audit-lbl {
        font-size: 0.7rem;
        font-weight: 700;
        color: #64748B;
        text-transform: uppercase;
        margin-top: 4px;
    }

    /* Forecast Highlight Card */
    .forecast-card {
        background-color: #FFFFFF;
        border: 1.5px solid #2563EB;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 12px -2px rgba(37, 99, 235, 0.08);
        margin-bottom: 16px;
    }
    .forecast-val {
        font-size: 2.1rem;
        font-weight: 800;
        color: #2563EB;
        letter-spacing: -0.02em;
    }

    /* Disclaimer Box */
    .disclaimer-box {
        background-color: #FFFBEB;
        border: 1px solid #FDE68A;
        border-left: 4px solid #D97706;
        padding: 12px 16px;
        border-radius: 6px;
        color: #92400E;
        font-size: 0.82rem;
        line-height: 1.4;
        margin-top: 14px;
    }
    
    /* ── SIDEBAR RADIO NAVIGATION MENU ───────────────── */
    div[data-testid="stSidebar"] div[data-testid="stRadio"] > label {
        display: none !important;
    }
    div[data-testid="stSidebar"] div[data-testid="stRadio"] > div[role="radiogroup"] {
        gap: 3px !important;
    }
    div[data-testid="stSidebar"] div[data-testid="stRadio"] label[data-baseweb="radio"] {
        background-color: transparent !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
        margin: 0 !important;
        width: 100% !important;
        cursor: pointer !important;
        transition: all 0.15s ease !important;
        border: 1px solid transparent !important;
    }
    div[data-testid="stSidebar"] div[data-testid="stRadio"] label[data-baseweb="radio"]:hover {
        background-color: rgba(255, 255, 255, 0.08) !important;
    }
    div[data-testid="stSidebar"] div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) {
        background-color: rgba(37, 99, 235, 0.22) !important;
        border-left: 3.5px solid #2563EB !important;
    }
    div[data-testid="stSidebar"] div[data-testid="stRadio"] label[data-baseweb="radio"] > div:first-child {
        display: none !important;
    }
    div[data-testid="stSidebar"] div[data-testid="stRadio"] label[data-baseweb="radio"] div:last-child p {
        color: #94A3B8 !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        margin: 0 !important;
    }
    div[data-testid="stSidebar"] div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) div:last-child p {
        color: #BFDBFE !important;
        font-weight: 700 !important;
    }

    /* Hide Streamlit Header Clutter */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)


def reset_app_state():
    """Clear session state keys when uploading a new file or resetting."""
    keys_to_clear = [
        "raw_df",
        "cleaned_df",
        "cleaning_summary",
        "dataset_name",
        "is_demo",
        "data_cleaned",
        "pdf_bytes",
    ]
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]


def inspect_raw_dataset(df: pd.DataFrame, filename: str) -> Dict[str, Any]:
    """Inspect raw dataset before cleaning."""
    std_df = data_cleaning.standardize_column_names(df.copy())
    total_cells = df.shape[0] * df.shape[1] if df.shape[1] > 0 else 1
    missing_cells = int(df.isnull().sum().sum())
    missing_pct = round((missing_cells / total_cells) * 100, 2)
    duplicate_rows = int(df.duplicated().sum())

    min_date_str, max_date_str = "N/A", "N/A"
    if "Date" in std_df.columns:
        parsed_dates = pd.to_datetime(std_df["Date"], errors="coerce").dropna()
        if not parsed_dates.empty:
            min_date_str = parsed_dates.min().strftime("%Y-%m-%d")
            max_date_str = parsed_dates.max().strftime("%Y-%m-%d")

    return {
        "filename": filename,
        "rows": len(df),
        "columns": list(df.columns),
        "col_count": len(df.columns),
        "missing_cells": missing_cells,
        "missing_pct": missing_pct,
        "duplicate_rows": duplicate_rows,
        "date_range": f"{min_date_str} – {max_date_str}",
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
    }


def main():
    config.ensure_directories()

    dataset_loaded = "raw_df" in st.session_state and st.session_state["raw_df"] is not None
    data_cleaned = st.session_state.get("data_cleaned", False)

    # Status Badge State
    if not dataset_loaded:
        status_html = '<span class="status-badge status-waiting">○ Waiting for Dataset</span>'
    elif not data_cleaned:
        status_html = '<span class="status-badge status-loaded">● Dataset Loaded</span>'
    else:
        status_html = '<span class="status-badge status-ready">● Analysis Ready</span>'

    # -------------------------------------------------------------------------
    # Header Banner (Dark Navy Gradient)
    # -------------------------------------------------------------------------
    # Determine active workflow step for breadcrumb
    if not dataset_loaded:
        wf_active = 0
    elif not data_cleaned:
        wf_active = 1
    else:
        wf_active = 3

    def wf(label, idx):
        cls = "wf-step active" if idx <= wf_active else "wf-step"
        return f'<span class="{cls}">{label}</span>'

    wf_html = (
        wf("01 Upload", 0) + '<span class="wf-arrow"> › </span>' +
        wf("02 Clean", 1) + '<span class="wf-arrow"> › </span>' +
        wf("03 Analyze", 2) + '<span class="wf-arrow"> › </span>' +
        wf("04 Forecast", 3) + '<span class="wf-arrow"> › </span>' +
        wf("05 Export PDF", 4)
    )

    # Inline SVG brand logo (bar chart analytics icon)
    brand_logo_svg = """
    <svg width="36" height="36" viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg" style="display:inline-block;vertical-align:middle;margin-right:10px;flex-shrink:0;">
      <rect width="36" height="36" rx="8" fill="#2563EB"/>
      <rect x="7" y="20" width="5" height="9" rx="1.5" fill="white" opacity="0.9"/>
      <rect x="15.5" y="13" width="5" height="16" rx="1.5" fill="white"/>
      <rect x="24" y="7" width="5" height="22" rx="1.5" fill="white" opacity="0.75"/>
      <path d="M9.5 19L18 12L26.5 6" stroke="#93C5FD" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="2 2"/>
    </svg>"""

    st.markdown(
        f"""
        <div class="header-banner">
            <div class="header-left">
                <div style="display:flex; align-items:center; gap:4px; margin-bottom:6px;">
                    {brand_logo_svg}
                    <h1 style="margin:0; display:inline;">Sales Data Analyzer</h1>
                </div>
                <div class="subtitle">Retail Sales Intelligence &amp; Forecasting Platform</div>
                <div class="tagline">Upload your raw CSV &rarr; Clean, Analyze, Forecast &amp; Export a professional business report in minutes.</div>
                <div class="workflow-steps" style="margin-top: 12px;">{wf_html}</div>
            </div>
            <div class="header-right">
                {status_html}
                <div style="font-size: 0.72rem; color: #94A3B8; text-align: right; line-height: 1.6;">
                    Python &bull; Pandas &bull; Scikit-learn<br>Plotly &bull; ReportLab
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # -------------------------------------------------------------------------
    # Sidebar — Enterprise Interactive Navigation
    # -------------------------------------------------------------------------
    with st.sidebar:
        # Brand Header
        st.markdown(
            """
            <div style="display:flex;align-items:center;gap:8px;padding:12px 0 14px 0;border-bottom:1px solid #1E293B;margin-bottom:14px;">
                <svg width="30" height="30" viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect width="36" height="36" rx="8" fill="#2563EB"/>
                    <rect x="7" y="20" width="5" height="9" rx="1.5" fill="white" opacity="0.9"/>
                    <rect x="15.5" y="13" width="5" height="16" rx="1.5" fill="white"/>
                    <rect x="24" y="7" width="5" height="22" rx="1.5" fill="white" opacity="0.75"/>
                </svg>
                <div>
                    <div style="font-size:1.15rem;font-weight:900;color:#FFFFFF;line-height:1;letter-spacing:-0.01em;">SALES</div>
                    <div style="font-size:0.72rem;font-weight:700;color:#3B82F6;letter-spacing:0.1em;margin-top:1px;">DATA ANALYZER</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Navigation Menu
        st.markdown(
            '<div style="font-size:0.65rem;font-weight:700;color:#64748B;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px;padding-left:4px;">NAVIGATION</div>',
            unsafe_allow_html=True,
        )

        nav_options = [
            "📊 Overview & KPIs",
            "📈 Sales Trends",
            "🏷️ Products & Categories",
            "🌍 Regional Analysis",
            "✅ Data Quality Audit",
            "🔮 Forecast & ML",
            "📄 Report & Export",
            "🚀 Full Dashboard (All Views)",
        ]

        if data_cleaned:
            selected_view = st.radio(
                "Select View",
                options=nav_options,
                index=0,
                key="active_dashboard_view",
                label_visibility="collapsed",
            )
        else:
            selected_view = "📊 Overview & KPIs"
            # Locked preview before analysis
            locked_html = "".join([
                f'<div style="display:flex;align-items:center;gap:8px;padding:7px 10px;border-radius:6px;margin-bottom:2px;opacity:0.35;cursor:not-allowed;">'
                f'<span style="font-size:0.83rem;color:#94A3B8;">{opt}</span></div>'
                for opt in nav_options
            ])
            st.markdown(
                f"""
                {locked_html}
                <div style="font-size:0.72rem;color:#64748B;padding:8px 10px;background:rgba(37,99,235,0.08);border-radius:6px;margin-top:8px;border-left:2px solid #334155;line-height:1.4;">
                    Upload &amp; analyze a CSV to activate live navigation.
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Data Source Status
        if dataset_loaded:
            ds_name = st.session_state.get("dataset_name", "Uploaded CSV")
            is_demo = st.session_state.get("is_demo", False)
            source_lbl = "Demo Dataset" if is_demo else "Custom Upload"
            st.markdown(
                f"""
                <div style="border-top:1px solid #1E293B;padding-top:12px;margin-top:16px;">
                    <div style="font-size:0.65rem;font-weight:700;color:#64748B;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px;padding-left:4px;">DATA SOURCE</div>
                    <div style="font-size:0.78rem;color:#94A3B8;margin-bottom:3px;padding-left:4px;">
                        Source: <span style="color:#CBD5E1;font-weight:600;">{source_lbl}</span>
                    </div>
                    <div style="font-size:0.75rem;color:#3B82F6;font-weight:600;word-break:break-all;padding-left:4px;">{ds_name}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)
            if st.button("⟳ Upload New Dataset", use_container_width=True, key="sidebar_reset_btn"):
                reset_app_state()
                st.rerun()

        # Footer
        st.markdown(
            """
            <div style="margin-top:24px;font-size:0.68rem;color:#475569;line-height:1.6;padding-top:12px;border-top:1px solid #1E293B;">
                Python &bull; Pandas &bull; Scikit-learn<br>Plotly &bull; ReportLab
            </div>
            """,
            unsafe_allow_html=True,
        )


    # -------------------------------------------------------------------------
    # Screen 1: Centered Upload Panel (When no dataset is loaded)
    # -------------------------------------------------------------------------
    if not dataset_loaded:
        st.markdown("<br>", unsafe_allow_html=True)
        up_col1, up_col2, up_col3 = st.columns([1, 3, 1])

        with up_col2:
            st.markdown(
                """
                <div style="background-color: #FFFFFF; border: 1.5px dashed #CBD5E1; border-radius: 12px; padding: 32px; text-align: center; box-shadow: 0 2px 4px 0 rgba(0,0,0,0.03);">
                    <div style="font-size: 2.2rem; margin-bottom: 8px;">📥</div>
                    <div style="font-size: 1.25rem; font-weight: 800; color: #0F172A;">UPLOAD YOUR SALES DATA</div>
                    <p style="font-size: 0.88rem; color: #64748B; margin-top: 4px; margin-bottom: 16px;">
                        Drop your CSV file here or browse your computer to generate instant insights.
                    </p>
                    <div style="font-size: 0.78rem; font-weight: 600; color: #2563EB; background-color: #EFF6FF; display: inline-block; padding: 4px 12px; border-radius: 12px; margin-bottom: 12px;">
                        Supported Format: CSV (.csv)
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            uploaded_file = st.file_uploader(
                "Select CSV File",
                type=["csv"],
                label_visibility="collapsed",
            )

            if uploaded_file is not None:
                try:
                    df = pd.read_csv(uploaded_file)
                    st.session_state["raw_df"] = df
                    st.session_state["dataset_name"] = uploaded_file.name
                    st.session_state["is_demo"] = False
                    st.session_state["data_cleaned"] = False
                    st.rerun()
                except Exception as e:
                    st.error(f"Error parsing uploaded CSV file: {e}")

            st.markdown("<div style='text-align: center; color: #94A3B8; font-weight: 600; margin: 16px 0;'>── OR ──</div>", unsafe_allow_html=True)

            if st.button("✨ Try Demo Dataset (5-Year Retail Sales)", use_container_width=True, type="secondary"):
                if not config.INPUT_CSV_PATH.exists():
                    data_cleaning.generate_sample_dataset(config.INPUT_CSV_PATH)
                df = pd.read_csv(config.INPUT_CSV_PATH)
                st.session_state["raw_df"] = df
                st.session_state["dataset_name"] = "demo_sales_data.csv"
                st.session_state["is_demo"] = True
                st.session_state["data_cleaned"] = False
                st.rerun()

        st.stop()

    # -------------------------------------------------------------------------
    # Screen 2: Dataset Loaded -> Compact Status Bar & Validation/Cleaning
    # -------------------------------------------------------------------------
    raw_df = st.session_state["raw_df"]
    dataset_name = st.session_state.get("dataset_name", "sales_data.csv")
    is_demo = st.session_state.get("is_demo", False)
    raw_inspection = inspect_raw_dataset(raw_df, dataset_name)

    # Compact Status Bar
    st.markdown(
        f"""
        <div class="dataset-status-bar">
            <div class="dataset-info-text">
                ✓ <b>Dataset Loaded:</b> <span class="dataset-filename">{dataset_name}</span> &nbsp;|&nbsp; 
                <b>{raw_inspection['rows']:,} records</b> &nbsp;|&nbsp; 
                <b>Span:</b> {raw_inspection['date_range']}
            </div>
            <div>
                <span style="font-size: 0.78rem; font-weight: 600; color: #64748B;">{'🟡 Demo Mode' if is_demo else '🟢 Custom User Data'}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Validate Schema
    try:
        data_cleaning.validate_required_columns(raw_df)
    except Exception as val_err:
        st.error(f"❌ **Schema Validation Error:** {val_err}")
        st.info("Supported Columns: Date, Product, Quantity, Unit_Price / Sales, Category (optional), Region (optional).")
        if st.button("Upload a Different Dataset"):
            reset_app_state()
            st.rerun()
        st.stop()

    # Pre-Cleaning Raw Data Inspector & Cleaning Trigger
    if not data_cleaned:
        with st.expander("🔍 Pre-Cleaning Dataset Inspection & Raw Preview", expanded=True):
            s_c1, s_c2, s_c3, s_c4 = st.columns(4)
            with s_c1:
                st.metric("Total Rows", f"{raw_inspection['rows']:,}")
            with s_c2:
                st.metric("Total Columns", f"{raw_inspection['col_count']}")
            with s_c3:
                st.metric("Duplicate Rows", f"{raw_inspection['duplicate_rows']:,}")
            with s_c4:
                st.metric("Missing Cells", f"{raw_inspection['missing_cells']:,} ({raw_inspection['missing_pct']}%)")

            st.markdown(f"**Detected Columns:** `{', '.join(raw_inspection['columns'])}`")
            st.markdown("**First 10 Raw Rows:**")
            st.dataframe(raw_df.head(10), use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col_cln1, col_cln2, col_cln3 = st.columns([1, 2, 1])
        with col_cln2:
            if st.button("🚀 Clean & Analyze Data", type="primary", use_container_width=True):
                with st.spinner("Executing data cleaning pipeline..."):
                    cleaned_df, cleaning_summary = data_cleaning.clean_sales_data(raw_df)
                    st.session_state["cleaned_df"] = cleaned_df
                    st.session_state["cleaning_summary"] = cleaning_summary
                    st.session_state["data_cleaned"] = True
                    st.rerun()
        st.stop()

    # -------------------------------------------------------------------------
    # Post-Cleaning Active Data State
    # -------------------------------------------------------------------------
    cleaned_df = st.session_state["cleaned_df"]
    cleaning_summary = st.session_state["cleaning_summary"]

    # -------------------------------------------------------------------------
    # Date Range Filter Bar
    # -------------------------------------------------------------------------
    min_avail_date = cleaned_df["Date"].min().date()
    max_avail_date = cleaned_df["Date"].max().date()

    with st.container():
        f_c1, f_c2, f_c3 = st.columns([2, 2, 3])
        with f_c1:
            start_date_val = st.date_input(
                "Start Date",
                value=min_avail_date,
                min_value=min_avail_date,
                max_value=max_avail_date,
                key="bi_start_date",
            )
        with f_c2:
            end_date_val = st.date_input(
                "End Date",
                value=max_avail_date,
                min_value=min_avail_date,
                max_value=max_avail_date,
                key="bi_end_date",
            )
        with f_c3:
            st.markdown("<div style='font-size: 0.78rem; font-weight: 700; color: #64748B; text-transform: uppercase; margin-bottom: 8px;'>Quick Date Presets</div>", unsafe_allow_html=True)
            p_c1, p_c2, p_c3 = st.columns(3)
            with p_c1:
                if st.button("Full Dataset", use_container_width=True):
                    st.session_state["bi_start_date"] = min_avail_date
                    st.session_state["bi_end_date"] = max_avail_date
                    st.rerun()
            with p_c2:
                if st.button("Last 2 Years", use_container_width=True):
                    st.session_state["bi_start_date"] = max(min_avail_date, date(max_avail_date.year - 2, max_avail_date.month, max_avail_date.day))
                    st.session_state["bi_end_date"] = max_avail_date
                    st.rerun()
            with p_c3:
                if st.button("Last 1 Year", use_container_width=True):
                    st.session_state["bi_start_date"] = max(min_avail_date, date(max_avail_date.year - 1, max_avail_date.month, max_avail_date.day))
                    st.session_state["bi_end_date"] = max_avail_date
                    st.rerun()

    if start_date_val > end_date_val:
        st.error("Start Date cannot be after End Date.")
        st.stop()

    start_str = start_date_val.strftime("%Y-%m-%d")
    end_str = end_date_val.strftime("%Y-%m-%d")

    filtered_df = analysis.filter_by_date_range(cleaned_df, start_str, end_str)

    if filtered_df.empty:
        st.warning(f"No transactions found between {start_str} and {end_str}. Please expand your date filter.")
        st.stop()

    # Calculate analytics
    kpis = analysis.calculate_kpis(filtered_df)
    trends = analysis.analyze_sales_trend(filtered_df)
    pred_result = prediction.predict_next_month_sales(filtered_df)

    # Visibility flags based on sidebar navigation selection
    show_all = (selected_view == "🚀 Full Dashboard (All Views)")
    show_overview = show_all or (selected_view == "📊 Overview & KPIs")
    show_trends = show_all or (selected_view == "📈 Sales Trends")
    show_products = show_all or (selected_view == "🏷️ Products & Categories")
    show_regional = show_all or (selected_view == "🌍 Regional Analysis")
    show_quality = show_all or (selected_view == "✅ Data Quality Audit")
    show_forecast = show_all or (selected_view == "🔮 Forecast & ML")
    show_report = show_all or (selected_view == "📄 Report & Export")

    st.markdown("<br>", unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # 1. Executive Overview & Key Insights
    # -------------------------------------------------------------------------
    if show_overview:
        st.markdown('<div id="sec-overview"></div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="section-header-title">EXECUTIVE OVERVIEW</div>
            <div class="section-header-sub">Quick snapshot of your sales performance</div>
            """,
            unsafe_allow_html=True,
        )

        kpi_c1, kpi_c2, kpi_c3, kpi_c4 = st.columns(4)
        rev = kpis["total_sales"]
        rev_str = f"${rev*1e-6:.2f}M" if rev >= 1e6 else f"${rev*1e-3:.1f}k" if rev >= 1e3 else f"${rev:,.2f}"

        with kpi_c1:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-label">Total Revenue</div>
                    <div class="kpi-value">{rev_str}</div>
                    <div class="kpi-sub">${kpis['total_sales']:,.2f} total</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with kpi_c2:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-label">Transactions</div>
                    <div class="kpi-value">{kpis['total_transactions']:,}</div>
                    <div class="kpi-sub">orders completed</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with kpi_c3:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-label">Units Sold</div>
                    <div class="kpi-value">{kpis['total_quantity']:,}</div>
                    <div class="kpi-sub">total item volume</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with kpi_c4:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-label">Avg. Order Value</div>
                    <div class="kpi-value">${kpis['average_sale']:,.2f}</div>
                    <div class="kpi-sub">Trend: {trends['trend_direction']} ({trends['growth_rate_pct']:+.1f}%)</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            """
            <div class="section-header-title">KEY BUSINESS INSIGHTS</div>
            <div class="section-header-sub">Data-driven performance highlights</div>
            """,
            unsafe_allow_html=True,
        )

        ins_c1, ins_c2, ins_c3 = st.columns(3)
        best_p_val = kpis["best_product"]
        best_p_rev = kpis["best_product_sales"]
        best_c_val = kpis["best_category"]
        best_r_val = kpis["best_region"] if kpis.get("has_region", False) and kpis["best_region"] != "N/A" else "N/A"

        with ins_c1:
            st.markdown(
                f"""
                <div class="insight-card">
                    <div class="insight-label">Top Product</div>
                    <div class="insight-title">{best_p_val}</div>
                    <div class="insight-desc">{best_p_val} generated highest product revenue (${best_p_rev:,.2f}).</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with ins_c2:
            st.markdown(
                f"""
                <div class="insight-card">
                    <div class="insight-label">Top Category</div>
                    <div class="insight-title">{best_c_val}</div>
                    <div class="insight-desc">{best_c_val} leads overall department sales.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with ins_c3:
            reg_desc = f"{best_r_val} generated highest revenue contribution." if best_r_val != "N/A" else "Regional data unavailable."
            st.markdown(
                f"""
                <div class="insight-card">
                    <div class="insight-label">Top Region</div>
                    <div class="insight-title">{best_r_val}</div>
                    <div class="insight-desc">{reg_desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("<br><br>", unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # 2. Sales Performance
    # -------------------------------------------------------------------------
    if show_trends:
        st.markdown('<div id="sec-sales"></div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="section-header-title">SALES PERFORMANCE</div>
            <div class="section-header-sub">Historical monthly sales trajectory vs quarterly comparisons</div>
            """,
            unsafe_allow_html=True,
        )

        chart_c1, chart_c2 = st.columns([65, 35])
        monthly_df = analysis.get_monthly_sales(filtered_df)
        quarterly_df = analysis.get_quarterly_sales(filtered_df)

        with chart_c1:
            st.markdown("##### Monthly Sales Trend")
            if not monthly_df.empty:
                fig_m = px.line(
                    monthly_df,
                    x="Year_Month",
                    y="Sales",
                    markers=True,
                    labels={"Year_Month": "Month", "Sales": "Revenue ($)"},
                )
                fig_m.update_traces(line_color="#2563EB", line_width=3, marker=dict(size=6, color="#0F172A"))
                fig_m.update_layout(
                    plot_bgcolor="#FFFFFF",
                    paper_bgcolor="#FFFFFF",
                    hovermode="x unified",
                    margin=dict(l=10, r=10, t=20, b=10),
                    height=340,
                    xaxis=dict(gridcolor="#F1F5F9", showgrid=True),
                    yaxis=dict(gridcolor="#F1F5F9", showgrid=True),
                )
                st.plotly_chart(fig_m, use_container_width=True)

        with chart_c2:
            st.markdown("##### Quarterly Performance")
            if not quarterly_df.empty:
                fig_q = px.bar(
                    quarterly_df,
                    x="Year_Quarter",
                    y="Sales",
                    text_auto=".2s",
                    labels={"Year_Quarter": "Quarter", "Sales": "Revenue ($)"},
                    color_discrete_sequence=["#0F172A"],
                )
                fig_q.update_traces(textposition="outside", textfont_size=10)
                fig_q.update_layout(
                    plot_bgcolor="#FFFFFF",
                    paper_bgcolor="#FFFFFF",
                    margin=dict(l=10, r=10, t=20, b=10),
                    height=340,
                    xaxis=dict(gridcolor="#F1F5F9", showgrid=False),
                    yaxis=dict(gridcolor="#F1F5F9", showgrid=True),
                )
                st.plotly_chart(fig_q, use_container_width=True)

        st.markdown("<br><br>", unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # 3. Product Performance
    # -------------------------------------------------------------------------
    if show_products:
        st.markdown('<div id="sec-products"></div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="section-header-title">PRODUCT PERFORMANCE</div>
            <div class="section-header-sub">Best-selling products leaderboard and category revenue share</div>
            """,
            unsafe_allow_html=True,
        )

        prod_c1, prod_c2 = st.columns(2)
        top_5_df = analysis.get_top_products(filtered_df, top_n=5)
        cat_df = analysis.get_category_sales(filtered_df)

        with prod_c1:
            st.markdown(f"##### Top {len(top_5_df)} Best-Selling Products")
            if not top_5_df.empty:
                fig_tp = px.bar(
                    top_5_df.sort_values(by="Sales", ascending=True),
                    x="Sales",
                    y="Product",
                    orientation="h",
                    text_auto=".2s",
                    color_discrete_sequence=["#2563EB"],
                    labels={"Sales": "Revenue ($)", "Product": "Product"},
                )
                fig_tp.update_layout(
                    plot_bgcolor="#FFFFFF",
                    paper_bgcolor="#FFFFFF",
                    margin=dict(l=10, r=10, t=20, b=10),
                    height=300,
                    xaxis=dict(gridcolor="#F1F5F9", showgrid=True),
                    yaxis=dict(gridcolor="#F1F5F9", showgrid=False),
                )
                st.plotly_chart(fig_tp, use_container_width=True)

        with prod_c2:
            st.markdown("##### Sales by Category")
            if not cat_df.empty:
                fig_cat = px.pie(
                    cat_df,
                    names="Category",
                    values="Sales",
                    hole=0.55,
                    color_discrete_sequence=["#0F172A", "#2563EB", "#D97706", "#16A34A", "#64748B"],
                )
                fig_cat.update_traces(textposition="inside", textinfo="percent+label")
                fig_cat.update_layout(
                    plot_bgcolor="#FFFFFF",
                    paper_bgcolor="#FFFFFF",
                    margin=dict(l=10, r=10, t=20, b=10),
                    height=300,
                )
                st.plotly_chart(fig_cat, use_container_width=True)

        with st.expander("📋 View Expandable Product & Category Tables"):
            tbl_c1, tbl_c2 = st.columns(2)
            with tbl_c1:
                st.markdown("**Top Products Leaderboard:**")
                st.dataframe(
                    top_5_df.style.format({"Sales": "${:,.2f}", "Quantity": "{:,}", "Average_Price": "${:,.2f}"}),
                    hide_index=True,
                    use_container_width=True,
                )
            with tbl_c2:
                st.markdown("**Category Breakdown:**")
                st.dataframe(
                    cat_df.style.format({"Sales": "${:,.2f}", "Quantity": "{:,}", "Percentage": "{:.1f}%"}),
                    hide_index=True,
                    use_container_width=True,
                )

        st.markdown("<br><br>", unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # 4. Regional Performance
    # -------------------------------------------------------------------------
    if show_regional:
        st.markdown('<div id="sec-regional"></div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="section-header-title">REGIONAL PERFORMANCE</div>
            <div class="section-header-sub">Geographic revenue distribution across territories</div>
            """,
            unsafe_allow_html=True,
        )

        if "Region" in filtered_df.columns:
            reg_df = analysis.get_regional_sales(filtered_df)
            if not reg_df.empty:
                fig_reg = px.bar(
                    reg_df,
                    x="Region",
                    y="Sales",
                    color="Region",
                    text_auto=".2s",
                    labels={"Sales": "Total Revenue ($)", "Region": "Sales Territory"},
                    color_discrete_sequence=px.colors.qualitative.Prism,
                )
                fig_reg.update_traces(textposition="outside")
                fig_reg.update_layout(
                    plot_bgcolor="#FFFFFF",
                    paper_bgcolor="#FFFFFF",
                    margin=dict(l=10, r=10, t=20, b=10),
                    height=320,
                    xaxis=dict(gridcolor="#F1F5F9", showgrid=False),
                    yaxis=dict(gridcolor="#F1F5F9", showgrid=True),
                )
                st.plotly_chart(fig_reg, use_container_width=True)

                top_reg_name = reg_df.iloc[0]["Region"]
                top_reg_pct = reg_df.iloc[0]["Percentage"]
                st.markdown(f"💡 *Insight: **{top_reg_name}** generated the highest revenue contribution ({top_reg_pct:.1f}% market share).*")
        else:
            st.info("ℹ️ Regional analysis is unavailable because no Region/Territory column was detected in the uploaded dataset.")

        st.markdown("<br><br>", unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # 5. Data Quality Audit Section
    # -------------------------------------------------------------------------
    if show_quality:
        st.markdown('<div id="sec-quality"></div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="section-header-title">DATA QUALITY & CLEANING</div>
            <div class="section-header-sub">Audit metrics applied prior to analysis to ensure data reliability</div>
            """,
            unsafe_allow_html=True,
        )

        aud_c1, aud_c2, aud_c3, aud_c4, aud_c5 = st.columns(5)

        with aud_c1:
            st.markdown(
                f"""
                <div class="audit-card">
                    <div class="audit-val">{cleaning_summary.get('rows_before', 0):,}</div>
                    <div class="audit-lbl">RAW RECORDS</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with aud_c2:
            st.markdown(
                f"""
                <div class="audit-card">
                    <div class="audit-val" style="color: #16A34A;">{cleaning_summary.get('duplicates_removed', 0):,}</div>
                    <div class="audit-lbl">DUPLICATES REMOVED</div>
                    <div style="font-size: 0.72rem; color: #16A34A; font-weight: 600; margin-top: 2px;">✓ Clean</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with aud_c3:
            st.markdown(
                f"""
                <div class="audit-card">
                    <div class="audit-val" style="color: #2563EB;">{cleaning_summary.get('missing_handled_count', 0):,}</div>
                    <div class="audit-lbl">MISSING VALUES HANDLED</div>
                    <div style="font-size: 0.72rem; color: #2563EB; font-weight: 600; margin-top: 2px;">✓ Imputed</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with aud_c4:
            st.markdown(
                f"""
                <div class="audit-card">
                    <div class="audit-val" style="color: #D97706;">{cleaning_summary.get('invalid_dates_removed', 0):,}</div>
                    <div class="audit-lbl">INVALID RECORDS</div>
                    <div style="font-size: 0.72rem; color: #D97706; font-weight: 600; margin-top: 2px;">! Pruned</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with aud_c5:
            st.markdown(
                f"""
                <div class="audit-card">
                    <div class="audit-val" style="color: #0F172A;">{cleaning_summary.get('rows_after', 0):,}</div>
                    <div class="audit-lbl">CLEAN RECORDS</div>
                    <div style="font-size: 0.72rem; color: #16A34A; font-weight: 600; margin-top: 2px;">✓ Validated</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("<div style='font-size: 0.8rem; color: #64748B; margin-top: 10px;'>Cleaning operations were applied before analysis to improve data reliability.</div>", unsafe_allow_html=True)
        st.markdown("<br><br>", unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # Correlation Analysis Section (Shown with Overview or All)
    # -------------------------------------------------------------------------
    if show_overview or show_all:
        st.markdown(
            """
            <div class="section-header-title">CORRELATION ANALYSIS</div>
            <div class="section-header-sub">Statistical relationships between numerical variables</div>
            """,
            unsafe_allow_html=True,
        )

        corr_df = analysis.compute_correlations(filtered_df)

        if not corr_df.empty:
            cr_col1, cr_col2 = st.columns([6, 4])

            with cr_col1:
                fig_corr = px.imshow(
                    corr_df,
                    text_auto=".3f",
                    aspect="auto",
                    color_continuous_scale="Blues",
                )
                fig_corr.update_layout(
                    plot_bgcolor="#FFFFFF",
                    paper_bgcolor="#FFFFFF",
                    margin=dict(l=10, r=10, t=10, b=10),
                    height=280,
                )
                st.plotly_chart(fig_corr, use_container_width=True)

            with cr_col2:
                st.markdown(
                    """
                    <div style="background-color: #FFFFFF; border: 1px solid #E2E8F0; border-left: 4px solid #2563EB; border-radius: 8px; padding: 18px; height: 100%;">
                        <div style="font-size: 0.72rem; font-weight: 700; color: #64748B; text-transform: uppercase;">KEY CORRELATION INSIGHT</div>
                    """,
                    unsafe_allow_html=True,
                )
                p_c = corr_df.loc["Unit_Price", "Sales"] if "Unit_Price" in corr_df.index and "Sales" in corr_df.columns else 0.0
                q_c = corr_df.loc["Quantity", "Sales"] if "Quantity" in corr_df.index and "Sales" in corr_df.columns else 0.0

                if abs(p_c) >= abs(q_c):
                    corr_statement = f"Unit Price and Sales exhibit a Pearson correlation coefficient of <b>{p_c:.3f}</b>. High-ticket price items represent the dominant driver of total revenue volume."
                else:
                    corr_statement = f"Quantity sold and Sales exhibit a Pearson correlation coefficient of <b>{q_c:.3f}</b>. Order volume represents the dominant driver of total revenue."

                st.markdown(f"<div style='font-size: 0.88rem; color: #0F172A; margin-top: 8px; line-height: 1.5;'>{corr_statement}</div></div>", unsafe_allow_html=True)

        st.markdown("<br><br>", unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # 6. Forecast Section
    # -------------------------------------------------------------------------
    if show_forecast:
        st.markdown('<div id="sec-forecast"></div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="section-header-title">SALES FORECAST</div>
            <div class="section-header-sub">Basic Machine Learning Forecast — Simple Linear Regression</div>
            """,
            unsafe_allow_html=True,
        )

        if pred_result.get("is_valid", False):
            st.markdown(
                f"""
                <div class="forecast-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <div style="font-size: 0.8rem; font-weight: 700; color: #64748B; text-transform: uppercase;">NEXT MONTH FORECAST ({pred_result['next_period_label']})</div>
                        <div style="font-size: 0.75rem; font-weight: 600; color: #2563EB; background-color: #EFF6FF; padding: 2px 10px; border-radius: 12px;">Simple Linear Regression</div>
                    </div>
                    <div class="forecast-val">${pred_result['predicted_sales']:,.2f}</div>
                    <div style="display: flex; gap: 24px; margin-top: 14px; padding-top: 12px; border-top: 1px solid #F1F5F9;">
                        <div>
                            <span style="font-size: 0.72rem; color: #64748B; font-weight: 600;">R² SCORE:</span>
                            <span style="font-size: 0.85rem; font-weight: 700; color: #0F172A; margin-left: 4px;">{pred_result['r2_score']:.4f}</span>
                        </div>
                        <div>
                            <span style="font-size: 0.72rem; color: #64748B; font-weight: 600;">SLOPE:</span>
                            <span style="font-size: 0.85rem; font-weight: 700; color: #0F172A; margin-left: 4px;">${pred_result['slope']:+,.2f}/mo</span>
                        </div>
                        <div>
                            <span style="font-size: 0.72rem; color: #64748B; font-weight: 600;">MODEL:</span>
                            <span style="font-size: 0.85rem; font-weight: 700; color: #0F172A; margin-left: 4px;">Baseline OLS Trend</span>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Plotly Regression Plot
            monthly_pred_df = analysis.get_monthly_sales(filtered_df)
            n_pts = len(monthly_pred_df)
            y_vals = monthly_pred_df["Sales"].values

            slope = pred_result["slope"]
            intercept = pred_result["intercept"]
            x_all = np.arange(1, n_pts + 2)
            y_trend = slope * x_all + intercept
            x_labels = list(monthly_pred_df["Year_Month"]) + [pred_result["next_period_label"]]

            fig_reg = go.Figure()
            fig_reg.add_trace(go.Scatter(
                x=list(range(1, n_pts + 1)),
                y=y_vals,
                mode="lines+markers",
                name="Historical Monthly Sales",
                line=dict(color="#0F172A", width=2.5),
                marker=dict(size=5, color="#0F172A"),
            ))
            fig_reg.add_trace(go.Scatter(
                x=list(range(1, n_pts + 2)),
                y=y_trend,
                mode="lines",
                name=f"Linear Trendline (R² = {pred_result['r2_score']:.2f})",
                line=dict(color="#D97706", width=2, dash="dash"),
            ))
            fig_reg.add_trace(go.Scatter(
                x=[n_pts + 1],
                y=[pred_result["predicted_sales"]],
                mode="markers+text",
                name=f"Forecast ({pred_result['next_period_label']})",
                marker=dict(size=12, color="#2563EB", symbol="diamond"),
                text=[f"${pred_result['predicted_sales']:,.0f}"],
                textposition="top center",
            ))

            step = max(1, len(x_labels) // 12)
            tick_idx = list(range(1, len(x_labels) + 1, step))
            if len(x_labels) not in tick_idx:
                tick_idx.append(len(x_labels))

            fig_reg.update_layout(
                plot_bgcolor="#FFFFFF",
                paper_bgcolor="#FFFFFF",
                xaxis=dict(
                    tickmode="array",
                    tickvals=tick_idx,
                    ticktext=[x_labels[i - 1] for i in tick_idx],
                    gridcolor="#F1F5F9",
                ),
                yaxis=dict(gridcolor="#F1F5F9"),
                margin=dict(l=10, r=10, t=10, b=10),
                height=340,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            )
            st.plotly_chart(fig_reg, use_container_width=True)

        else:
            st.warning(f"Forecasting Notice: {pred_result.get('error_message', 'Insufficient historical monthly data.')}")

        st.markdown(
            f"""
            <div class="disclaimer-box">
                <b>Notice & Methodology Disclaimer:</b><br>
                Simple Linear Regression is used as a baseline trend model. Forecast accuracy may be limited because the model does not account for seasonality, holidays, promotions, market volatility, or external factors.
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<br><br>", unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # 7. Report & Export Section
    # -------------------------------------------------------------------------
    if show_report:
        st.markdown('<div id="sec-report"></div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="section-header-title">REPORT & EXPORT</div>
            <div class="section-header-sub">Take your analysis with you — PDF report & cleaned CSV download.</div>
            """,
            unsafe_allow_html=True,
        )

        rep_col1, rep_col2 = st.columns(2)

        with rep_col1:
            st.markdown(
                """
                <div style="background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 10px; padding: 20px; box-shadow: 0 1px 3px 0 rgba(0,0,0,0.04);">
                    <div style="font-weight: 700; color: #0F172A; font-size: 1.05rem;">📄 Executive PDF Business Report</div>
                    <p style="font-size: 0.83rem; color: #64748B; margin-top: 4px; margin-bottom: 16px;">
                        Publication-grade PDF containing executive KPIs, data quality audits, monthly/quarterly tables, product leaderboards, correlation heatmaps, linear regression forecast, and strategic business findings.
                    </p>
                """,
                unsafe_allow_html=True,
            )

            if st.button("🚀 Compile Executive PDF Report", type="primary", use_container_width=True):
                with st.spinner("Rendering charts and compiling PDF report..."):
                    chart_paths = visualization.generate_all_charts(filtered_df, pred_result)
                    pdf_path = report_generator.generate_pdf_report(
                        df=filtered_df,
                        cleaning_summary=cleaning_summary,
                        pred_result=pred_result,
                        chart_paths=chart_paths,
                        dataset_name=dataset_name,
                        output_path=config.PDF_REPORT_PATH,
                    )
                    with open(pdf_path, "rb") as f:
                        st.session_state["pdf_bytes"] = f.read()
                    st.success("✓ Executive PDF Report ready!")

            if st.session_state.get("pdf_bytes") is not None:
                st.markdown("<div style='font-size: 0.8rem; color: #16A34A; font-weight: 600; margin-top: 8px;'>✓ Report ready</div>", unsafe_allow_html=True)
                st.download_button(
                    label="📥 Download sales_analysis_report.pdf",
                    data=st.session_state["pdf_bytes"],
                    file_name="sales_analysis_report.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )

            st.markdown("</div>", unsafe_allow_html=True)

        with rep_col2:
            st.markdown(
                """
                <div style="background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 10px; padding: 20px; box-shadow: 0 1px 3px 0 rgba(0,0,0,0.04);">
                    <div style="font-weight: 700; color: #0F172A; font-size: 1.05rem;">📊 Cleaned Dataset Export</div>
                    <p style="font-size: 0.83rem; color: #64748B; margin-top: 4px; margin-bottom: 16px;">
                        Download the preprocessed, deduplicated, and validated CSV file ready for spreadsheet modeling or database ingestion.
                    </p>
                """,
                unsafe_allow_html=True,
            )

            cleaned_csv_export = cleaned_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Download cleaned_sales_data.csv",
                data=cleaned_csv_export,
                file_name="cleaned_sales_data.csv",
                mime="text/csv",
                use_container_width=True,
            )

            st.markdown("</div>", unsafe_allow_html=True)



if __name__ == "__main__":
    main()
