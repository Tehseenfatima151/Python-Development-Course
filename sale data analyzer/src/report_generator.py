"""PDF Report generation module using ReportLab Platypus."""

import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
import pandas as pd

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    KeepTogether,
    HRFlowable,
)
from reportlab.pdfgen import canvas

import config
from src import analysis

logger = logging.getLogger("sales_analyzer.report_generator")


class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute and display accurate total page numbers."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages: int):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))

        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(36, 756, "Sales Data Analyzer — Executive Performance Report")
            self.drawRightString(576, 756, datetime.now().strftime("%Y-%m-%d"))
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.5)
            self.line(36, 750, 576, 750)

        # Footer (all pages)
        page_str = f"Page {self._pageNumber} of {total_pages}"
        self.drawString(36, 30, "Confidential — Retail Sales Performance & Forecasting")
        self.drawRightString(576, 30, page_str)
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(36, 42, 576, 42)

        self.restoreState()


def _build_styles() -> Dict[str, ParagraphStyle]:
    """Create custom typography and styles for the PDF report."""
    base_styles = getSampleStyleSheet()

    styles = {
        "DocTitle": ParagraphStyle(
            "DocTitle",
            parent=base_styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=22,
            leading=26,
            textColor=colors.HexColor("#1E3A8A"),
            alignment=0,
            spaceAfter=4,
        ),
        "DocSubtitle": ParagraphStyle(
            "DocSubtitle",
            parent=base_styles["Normal"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=13.5,
            textColor=colors.HexColor("#475569"),
            spaceAfter=10,
        ),
        "SectionHeader": ParagraphStyle(
            "SectionHeader",
            parent=base_styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=12.5,
            leading=16,
            textColor=colors.HexColor("#1E3A8A"),
            spaceBefore=10,
            spaceAfter=5,
        ),
        "SubsectionHeader": ParagraphStyle(
            "SubsectionHeader",
            parent=base_styles["Heading3"],
            fontName="Helvetica-Bold",
            fontSize=10,
            leading=13.5,
            textColor=colors.HexColor("#0F172A"),
            spaceBefore=6,
            spaceAfter=3,
        ),
        "Body": ParagraphStyle(
            "Body",
            parent=base_styles["Normal"],
            fontName="Helvetica",
            fontSize=8.5,
            leading=12,
            textColor=colors.HexColor("#334155"),
            spaceAfter=5,
        ),
        "Disclaimer": ParagraphStyle(
            "Disclaimer",
            parent=base_styles["Normal"],
            fontName="Helvetica-Oblique",
            fontSize=8,
            leading=11,
            textColor=colors.HexColor("#B45309"),
        ),
        "TableHeader": ParagraphStyle(
            "TableHeader",
            parent=base_styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8,
            leading=10.5,
            textColor=colors.white,
            alignment=1,
        ),
        "TableCell": ParagraphStyle(
            "TableCell",
            parent=base_styles["Normal"],
            fontName="Helvetica",
            fontSize=7.5,
            leading=10,
            textColor=colors.HexColor("#1E293B"),
            alignment=0,
        ),
        "TableCellCenter": ParagraphStyle(
            "TableCellCenter",
            parent=base_styles["Normal"],
            fontName="Helvetica",
            fontSize=7.5,
            leading=10,
            textColor=colors.HexColor("#1E293B"),
            alignment=1,
        ),
        "TableCellBold": ParagraphStyle(
            "TableCellBold",
            parent=base_styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=7.5,
            leading=10,
            textColor=colors.HexColor("#1E293B"),
            alignment=0,
        ),
        "KpiLabel": ParagraphStyle(
            "KpiLabel",
            parent=base_styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=7.5,
            leading=9.5,
            textColor=colors.HexColor("#64748B"),
            alignment=1,
        ),
        "KpiValue": ParagraphStyle(
            "KpiValue",
            parent=base_styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=15,
            textColor=colors.HexColor("#1E3A8A"),
            alignment=1,
        ),
    }
    return styles


def generate_pdf_report(
    df: pd.DataFrame,
    cleaning_summary: Dict[str, Any],
    pred_result: Dict[str, Any],
    chart_paths: Dict[str, Optional[Path]],
    dataset_name: str = "sales_data.csv",
    output_path: Path = config.PDF_REPORT_PATH,
    **kwargs: Any,
) -> Path:
    """Compile comprehensive executive sales report into professional PDF."""
    # Handle custom dataset name if passed in kwargs
    ds_name = kwargs.get("dataset_name", dataset_name)
    out_path = Path(kwargs.get("output_path", output_path))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    logger.info(f"Generating professional PDF report at {out_path}")

    doc = SimpleDocTemplate(
        str(out_path),
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=44,
        bottomMargin=44,
    )

    styles = _build_styles()
    story: List[Any] = []

    kpis = analysis.calculate_kpis(df)
    trends = analysis.analyze_sales_trend(df)
    start_date = kpis.get("date_range_start", "N/A")
    end_date = kpis.get("date_range_end", "N/A")
    generated_time = datetime.now().strftime("%B %d, %Y %I:%M %p")

    # 1. Cover Banner & Header
    story.append(Paragraph("SALES DATA ANALYSIS REPORT", styles["DocTitle"]))
    meta_text = (
        f"<b>Dataset:</b> {ds_name} &nbsp;|&nbsp; "
        f"<b>Analysis Period:</b> {start_date} &rarr; {end_date} &nbsp;|&nbsp; "
        f"<b>Generated:</b> {generated_time}"
    )
    story.append(Paragraph(meta_text, styles["DocSubtitle"]))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1E3A8A"), spaceAfter=10))

    # 2. Executive Summary KPI Dashboard Grid
    story.append(Paragraph("1. Executive Summary & Core KPIs", styles["SectionHeader"]))

    best_reg_display = kpis["best_region"] if kpis.get("has_region", False) and kpis["best_region"] != "N/A" else "N/A (No Region Column)"
    kpi_card_data = [
        [
            Paragraph("TOTAL REVENUE", styles["KpiLabel"]),
            Paragraph("TOTAL UNITS SOLD", styles["KpiLabel"]),
            Paragraph("TRANSACTIONS", styles["KpiLabel"]),
            Paragraph("AVG ORDER VALUE", styles["KpiLabel"]),
        ],
        [
            Paragraph(f"${kpis['total_sales']:,.2f}", styles["KpiValue"]),
            Paragraph(f"{kpis['total_quantity']:,}", styles["KpiValue"]),
            Paragraph(f"{kpis['total_transactions']:,}", styles["KpiValue"]),
            Paragraph(f"${kpis['average_sale']:,.2f}", styles["KpiValue"]),
        ],
        [
            Paragraph("TOP PRODUCT", styles["KpiLabel"]),
            Paragraph("TOP CATEGORY", styles["KpiLabel"]),
            Paragraph("TOP REGION", styles["KpiLabel"]),
            Paragraph("SALES TREND", styles["KpiLabel"]),
        ],
        [
            Paragraph(f"{kpis['best_product']}", styles["TableCellBold"]),
            Paragraph(f"{kpis['best_category']}", styles["TableCellBold"]),
            Paragraph(f"{best_reg_display}", styles["TableCellBold"]),
            Paragraph(f"{trends['trend_direction']} ({trends['growth_rate_pct']:+.1f}%)", styles["TableCellBold"]),
        ],
    ]

    kpi_table = Table(kpi_card_data, colWidths=[135, 135, 135, 135])
    kpi_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
            ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ])
    )
    story.append(kpi_table)
    story.append(Spacer(1, 10))

    # 3. Dataset Overview & Data Cleaning Audit
    story.append(Paragraph("2. Dataset Overview & Data Quality Audit", styles["SectionHeader"]))
    missing_before_count = sum(cleaning_summary.get("missing_before", {}).values())
    missing_after_count = sum(cleaning_summary.get("missing_after", {}).values())

    clean_table_data = [
        [
            Paragraph("Quality Metric", styles["TableHeader"]),
            Paragraph("Raw Ingestion", styles["TableHeader"]),
            Paragraph("Post-Cleaning", styles["TableHeader"]),
            Paragraph("Operational Resolution", styles["TableHeader"]),
        ],
        [
            Paragraph("Total Records", styles["TableCellBold"]),
            Paragraph(f"{cleaning_summary.get('rows_before', 0):,}", styles["TableCellCenter"]),
            Paragraph(f"{cleaning_summary.get('rows_after', 0):,}", styles["TableCellCenter"]),
            Paragraph("Invalid dates and unrecoverable records pruned", styles["TableCell"]),
        ],
        [
            Paragraph("Duplicate Rows", styles["TableCellBold"]),
            Paragraph(f"{cleaning_summary.get('duplicates_removed', 0):,}", styles["TableCellCenter"]),
            Paragraph("0", styles["TableCellCenter"]),
            Paragraph("Exact record duplicates identified and removed", styles["TableCell"]),
        ],
        [
            Paragraph("Missing Values", styles["TableCellBold"]),
            Paragraph(f"{missing_before_count:,}", styles["TableCellCenter"]),
            Paragraph(f"{missing_after_count:,}", styles["TableCellCenter"]),
            Paragraph("Numeric imputed with median; Categories with mode", styles["TableCell"]),
        ],
        [
            Paragraph("Invalid Dates", styles["TableCellBold"]),
            Paragraph(f"{cleaning_summary.get('invalid_dates_removed', 0):,}", styles["TableCellCenter"]),
            Paragraph("0", styles["TableCellCenter"]),
            Paragraph("Unparseable dates dropped to preserve time series", styles["TableCell"]),
        ],
    ]
    clean_table = Table(clean_table_data, colWidths=[120, 85, 85, 250])
    clean_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
            ("TOPPADDING", (0, 0), (-1, -1), 3.5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ])
    )
    story.append(clean_table)
    story.append(Spacer(1, 10))

    # 4. Monthly Sales Trajectory
    story.append(Paragraph("3. Monthly Sales Trajectory", styles["SectionHeader"]))
    if chart_paths.get("monthly_trend") and Path(chart_paths["monthly_trend"]).exists():
        story.append(Image(str(chart_paths["monthly_trend"]), width=540, height=205))
        story.append(Spacer(1, 5))

    monthly_df = analysis.get_monthly_sales(df)
    if not monthly_df.empty:
        story.append(Paragraph("Recent Monthly Breakdown (Latest Periods):", styles["SubsectionHeader"]))
        recent_monthly = monthly_df.tail(6)
        m_rows = [[
            Paragraph("Month", styles["TableHeader"]),
            Paragraph("Sales ($)", styles["TableHeader"]),
            Paragraph("Quantity", styles["TableHeader"]),
            Paragraph("Avg Order ($)", styles["TableHeader"]),
            Paragraph("Transactions", styles["TableHeader"]),
        ]]
        for _, row in recent_monthly.iterrows():
            m_rows.append([
                Paragraph(str(row["Year_Month"]), styles["TableCellCenter"]),
                Paragraph(f"${row['Sales']:,.2f}", styles["TableCellCenter"]),
                Paragraph(f"{int(row['Quantity']):,}", styles["TableCellCenter"]),
                Paragraph(f"${row['Average_Sale']:,.2f}", styles["TableCellCenter"]),
                Paragraph(f"{int(row['Transactions']):,}", styles["TableCellCenter"]),
            ])
        m_table = Table(m_rows, colWidths=[108, 108, 108, 108, 108])
        m_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
            ])
        )
        story.append(m_table)
    story.append(Spacer(1, 10))

    # 5. Quarterly Sales & Product Performance
    story.append(Paragraph("4. Quarterly & Product Performance", styles["SectionHeader"]))
    if chart_paths.get("quarterly_sales") and Path(chart_paths["quarterly_sales"]).exists():
        story.append(Image(str(chart_paths["quarterly_sales"]), width=540, height=195))
        story.append(Spacer(1, 6))

    top_df = analysis.get_top_products(df, top_n=5)
    if not top_df.empty:
        story.append(Paragraph("Top Best-Selling Products by Revenue:", styles["SubsectionHeader"]))
        top_rows = [[
            Paragraph("Rank", styles["TableHeader"]),
            Paragraph("Product Name", styles["TableHeader"]),
            Paragraph("Category", styles["TableHeader"]),
            Paragraph("Total Revenue", styles["TableHeader"]),
            Paragraph("Units Sold", styles["TableHeader"]),
            Paragraph("Avg Unit Price", styles["TableHeader"]),
        ]]
        for _, row in top_df.iterrows():
            top_rows.append([
                Paragraph(f"#{int(row['Rank'])}", styles["TableCellCenter"]),
                Paragraph(str(row["Product"]), styles["TableCellBold"]),
                Paragraph(str(row["Category"]), styles["TableCell"]),
                Paragraph(f"${row['Sales']:,.2f}", styles["TableCellCenter"]),
                Paragraph(f"{int(row['Quantity']):,}", styles["TableCellCenter"]),
                Paragraph(f"${row['Average_Price']:,.2f}", styles["TableCellCenter"]),
            ])
        top_table = Table(top_rows, colWidths=[35, 165, 110, 80, 75, 75])
        top_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
                ("TOPPADDING", (0, 0), (-1, -1), 3.5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
            ])
        )
        story.append(top_table)
        story.append(Spacer(1, 6))

    if chart_paths.get("top_products") and Path(chart_paths["top_products"]).exists():
        story.append(Image(str(chart_paths["top_products"]), width=540, height=190))
        story.append(Spacer(1, 10))

    # 6. Category and Regional Breakdown
    story.append(Paragraph("5. Category & Regional Distribution", styles["SectionHeader"]))
    cat_df = analysis.get_category_sales(df)
    reg_df = analysis.get_regional_sales(df)

    has_reg_chart = chart_paths.get("regional_sales") and Path(chart_paths["regional_sales"]).exists()
    has_cat_chart = chart_paths.get("category_sales") and Path(chart_paths["category_sales"]).exists()

    if has_cat_chart and has_reg_chart:
        chart_table = Table([
            [
                Image(str(chart_paths["category_sales"]), width=265, height=160),
                Image(str(chart_paths["regional_sales"]), width=265, height=160),
            ]
        ], colWidths=[270, 270])
        chart_table.setStyle(TableStyle([("ALIGN", (0, 0), (-1, -1), "CENTER"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
        story.append(chart_table)
    elif has_cat_chart:
        story.append(Image(str(chart_paths["category_sales"]), width=540, height=190))
        story.append(Paragraph("<i>Note: Regional analysis could not be performed because the uploaded dataset does not contain a Region/Territory column.</i>", styles["Body"]))
    story.append(Spacer(1, 10))

    # 7. Correlation Analysis
    story.append(Paragraph("6. Numerical Variable Correlation Analysis", styles["SectionHeader"]))
    corr_df = analysis.compute_correlations(df)
    if chart_paths.get("correlation_heatmap") and Path(chart_paths["correlation_heatmap"]).exists():
        story.append(Image(str(chart_paths["correlation_heatmap"]), width=380, height=210))
        story.append(Spacer(1, 4))

    q_sales_corr = corr_df.loc["Quantity", "Sales"] if not corr_df.empty and "Quantity" in corr_df.index and "Sales" in corr_df.columns else 0.0
    p_sales_corr = corr_df.loc["Unit_Price", "Sales"] if not corr_df.empty and "Unit_Price" in corr_df.index and "Sales" in corr_df.columns else 0.0

    corr_text = (
        f"<b>Correlation Insights:</b> In the analyzed dataset, the Pearson correlation between Unit Price and Sales is "
        f"<b>{p_sales_corr:.3f}</b>, while Quantity sold and Sales exhibits a correlation of <b>{q_sales_corr:.3f}</b>. "
        f"{'Unit Price represents a stronger revenue driver than order volume alone.' if abs(p_sales_corr) >= abs(q_sales_corr) else 'Order volume represents a stronger revenue driver than unit price.'}"
    )
    story.append(Paragraph(corr_text, styles["Body"]))
    story.append(Spacer(1, 10))

    # 8. Predictive Sales Forecasting
    story.append(Paragraph("7. Predictive Sales Forecasting (Simple Linear Regression)", styles["SectionHeader"]))
    if pred_result.get("is_valid", False):
        pred_table_data = [
            [
                Paragraph("Target Forecast Period", styles["TableHeader"]),
                Paragraph("Predicted Revenue ($)", styles["TableHeader"]),
                Paragraph("Model Fit (R² Score)", styles["TableHeader"]),
                Paragraph("Monthly Trajectory Slope", styles["TableHeader"]),
            ],
            [
                Paragraph(f"<b>{pred_result['next_period_label']}</b>", styles["TableCellCenter"]),
                Paragraph(f"<b>${pred_result['predicted_sales']:,.2f}</b>", styles["TableCellCenter"]),
                Paragraph(f"<b>{pred_result['r2_score']:.4f}</b>", styles["TableCellCenter"]),
                Paragraph(f"<b>${pred_result['slope']:+,.2f} / mo</b>", styles["TableCellCenter"]),
            ],
        ]
        pred_table = Table(pred_table_data, colWidths=[135, 135, 135, 135])
        pred_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
                ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#FEF3C7")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ])
        )
        story.append(pred_table)
        story.append(Spacer(1, 5))

        if chart_paths.get("prediction") and Path(chart_paths["prediction"]).exists():
            story.append(Image(str(chart_paths["prediction"]), width=540, height=205))
            story.append(Spacer(1, 5))
    else:
        story.append(Paragraph(f"<b>Warning:</b> {pred_result.get('error_message', 'Prediction unavailable.')}", styles["Body"]))

    disclaimer_box = Table(
        [[Paragraph(f"<b>Notice & Model Disclaimer:</b> {pred_result.get('disclaimer', config.MIN_OBSERVATIONS_FOR_REGRESSION)}", styles["Disclaimer"])]],
        colWidths=[540],
    )
    disclaimer_box.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFFBEB")),
            ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#F59E0B")),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ])
    )
    story.append(disclaimer_box)
    story.append(Spacer(1, 10))

    # 9. Business Insights & Strategic Conclusions
    story.append(Paragraph("8. Data-Driven Business Insights & Conclusion", styles["SectionHeader"]))
    reg_insight = f"Region <b>{kpis['best_region']}</b> represents the top sales territory." if kpis.get("has_region", False) and kpis['best_region'] != "N/A" else "Regional distribution was omitted due to missing region fields in the uploaded file."
    
    conclusion_text = (
        f"<b>1. Financial Performance:</b> Over the evaluated period ({start_date} to {end_date}), the business logged "
        f"<b>${kpis['total_sales']:,.2f}</b> across <b>{kpis['total_transactions']:,}</b> orders with an average sale of "
        f"<b>${kpis['average_sale']:,.2f}</b>.<br/>"
        f"<b>2. Catalog Drivers:</b> Product <b>{kpis['best_product']}</b> generated top revenue within the <b>{kpis['best_category']}</b> merchandise category.<br/>"
        f"<b>3. Territory Performance:</b> {reg_insight}<br/>"
        f"<b>4. Forecast Trajectory:</b> Sequential OLS regression forecasts revenue of "
        f"<b>${pred_result.get('predicted_sales', 0):,.2f}</b> for <b>{pred_result.get('next_period_label', 'Next Month')}</b> "
        f"with a monthly rate of change of <b>${pred_result.get('slope', 0):+,.2f}/mo</b>."
    )
    story.append(Paragraph(conclusion_text, styles["Body"]))

    doc.build(story, canvasmaker=NumberedCanvas)
    logger.info(f"PDF report generated successfully at {out_path}")
    return out_path
