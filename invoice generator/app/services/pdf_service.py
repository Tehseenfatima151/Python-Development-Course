"""
PDF Generation Service for InvoicePro
Faithfully recreates the visual design, structure, typography, and hierarchy of the reference invoice
using ReportLab vector elements and tables. Completely dynamic and multi-page capable.
"""
import os
import logging
from pathlib import Path
from decimal import Decimal
from typing import Dict, Any, List, Optional
from datetime import date

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, KeepTogether
)
from reportlab.graphics.shapes import Drawing, Circle, String, Group, Rect, Line, Polygon, Path as RLPath
from reportlab.pdfgen import canvas

from app.config import EXPORT_DIR, COLOR_NAVY_PRIMARY, COLOR_NAVY_DARK, COLOR_RED_ACCENT
from app.utils.formatters import format_currency, format_date, format_quantity_display
from app.utils.num_to_words import amount_to_words

logger = logging.getLogger(__name__)

# Color Definitions
NAVY_COLOR = colors.HexColor(COLOR_NAVY_DARK)
NAVY_BG = colors.HexColor(COLOR_NAVY_PRIMARY)
RED_COLOR = colors.HexColor(COLOR_RED_ACCENT)
BORDER_DARK = colors.HexColor("#000000")
BORDER_LIGHT = colors.HexColor("#CBD5E1")
TEXT_DARK = colors.HexColor("#0F172A")
TEXT_MUTED = colors.HexColor("#475569")
TEXT_NAVY = colors.HexColor("#002D62")


class NumberedCanvas(canvas.Canvas):
    """Custom canvas that draws running footer accents, page numbers, and decorative waves."""
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

    def draw_page_decorations(self, page_count: int):
        page_w, page_h = A4
        
        # Bottom decorative swoosh/accent lines (Navy & Red stripes matching reference)
        self.saveState()
        
        # Red curved swoosh
        red_path = self.beginPath()
        red_path.moveTo(0, 0)
        red_path.lineTo(0, 24)
        red_path.curveTo(page_w * 0.3, 30, page_w * 0.6, 6, page_w, 10)
        red_path.lineTo(page_w, 0)
        red_path.close()
        self.setFillColor(RED_COLOR)
        self.drawPath(red_path, fill=1, stroke=0)

        # Navy curved swoosh
        navy_path = self.beginPath()
        navy_path.moveTo(0, 0)
        navy_path.lineTo(0, 14)
        navy_path.curveTo(page_w * 0.35, 18, page_w * 0.7, 2, page_w, 4)
        navy_path.lineTo(page_w, 0)
        navy_path.close()
        self.setFillColor(NAVY_COLOR)
        self.drawPath(navy_path, fill=1, stroke=0)

        # Page numbering (if multi-page)
        if page_count > 1:
            self.setFont("Helvetica", 8)
            self.setFillColor(TEXT_MUTED)
            self.drawRightString(page_w - 36, 28, f"Page {self._pageNumber} of {page_count}")

        self.restoreState()


def create_stamp_drawing(company_name: str = "POULTRY SMART TRADERS", city: str = "Karachi (Pak.)") -> Drawing:
    """Generates a high-quality circular company stamp/seal badge."""
    d = Drawing(100, 100)
    center_x, center_y, radius = 50, 50, 42

    # Outer double circle
    d.add(Circle(center_x, center_y, radius, fillColor=None, strokeColor=NAVY_COLOR, strokeWidth=1.5))
    d.add(Circle(center_x, center_y, radius - 4, fillColor=None, strokeColor=NAVY_COLOR, strokeWidth=0.8))

    # Inner circle
    d.add(Circle(center_x, center_y, radius - 12, fillColor=None, strokeColor=NAVY_COLOR, strokeWidth=0.8))

    # Decorative stars / dots
    d.add(String(14, 48, "*", fontName="Helvetica-Bold", fontSize=12, fillColor=NAVY_COLOR))
    d.add(String(81, 48, "*", fontName="Helvetica-Bold", fontSize=12, fillColor=NAVY_COLOR))

    # Text inside stamp
    d.add(String(50, 77, "POULTRY", fontName="Helvetica-Bold", fontSize=7, textAnchor="middle", fillColor=NAVY_COLOR))
    d.add(String(50, 52, "SMART", fontName="Helvetica-Bold", fontSize=8, textAnchor="middle", fillColor=NAVY_COLOR))
    d.add(String(50, 43, "TRADERS", fontName="Helvetica-Bold", fontSize=8, textAnchor="middle", fillColor=NAVY_COLOR))
    d.add(String(50, 31, "23-A Gulshan", fontName="Helvetica", fontSize=4.5, textAnchor="middle", fillColor=NAVY_COLOR))
    d.add(String(50, 25, city, fontName="Helvetica", fontSize=4.5, textAnchor="middle", fillColor=NAVY_COLOR))
    d.add(String(50, 14, "poultrysmarttraders01@gmail.com", fontName="Helvetica", fontSize=4.2, textAnchor="middle", fillColor=NAVY_COLOR))

    return d


def create_signature_drawing(coordinator_name: str = "Dennis", title: str = "Sales Coordinator") -> Drawing:
    """Generates an elegant signature and title block."""
    d = Drawing(150, 60)
    
    # Signature text script
    d.add(String(75, 28, coordinator_name, fontName="Times-Italic", fontSize=22, textAnchor="middle", fillColor=NAVY_COLOR))

    # Horizontal signature line
    d.add(Line(15, 18, 135, 18, strokeColor=BORDER_DARK, strokeWidth=0.8))

    # Title under line
    d.add(String(75, 6, title, fontName="Helvetica", fontSize=9, textAnchor="middle", fillColor=TEXT_DARK))

    return d


def create_logo_drawing(company_name: str = "POULTRY SMART TRADERS") -> Drawing:
    """
    Generates the ST brand logo — navy C-bracket + red vertical bar + red diamond.
    Matches the actual Poultry Smart Traders logo mark.
    """
    d = Drawing(140, 58)

    # ── Navy outer S/C-bracket shape ─────────────────────────────────
    # Top horizontal arm (going right)
    d.add(Polygon(
        points=[4, 58, 44, 58, 44, 50, 4, 50],
        fillColor=NAVY_COLOR, strokeColor=None
    ))
    # Right vertical arm (top half)
    d.add(Polygon(
        points=[36, 58, 44, 58, 44, 34, 36, 34],
        fillColor=NAVY_COLOR, strokeColor=None
    ))
    # Middle horizontal connector (going left)
    d.add(Polygon(
        points=[4, 34, 36, 34, 36, 26, 4, 26],
        fillColor=NAVY_COLOR, strokeColor=None
    ))
    # Left vertical arm (bottom half)
    d.add(Polygon(
        points=[4, 26, 12, 26, 12, 8, 4, 8],
        fillColor=NAVY_COLOR, strokeColor=None
    ))
    # Bottom horizontal arm (going right)
    d.add(Polygon(
        points=[4, 8, 44, 8, 44, 16, 4, 16],
        fillColor=NAVY_COLOR, strokeColor=None
    ))

    # ── Red vertical bar (center I-beam) ─────────────────────────────
    d.add(Polygon(
        points=[18, 52, 30, 52, 30, 12, 18, 12],
        fillColor=RED_COLOR, strokeColor=None
    ))

    # ── Red diamond accent (bottom-left) ─────────────────────────────
    d.add(Polygon(
        points=[4, 4, 10, 4, 10, 0, 4, 0],
        fillColor=RED_COLOR, strokeColor=None
    ))

    # ── Company name text ─────────────────────────────────────────────
    d.add(String(52, 44, "Poultry",  fontName="Helvetica-Bold", fontSize=12,
                 fillColor=TEXT_DARK))
    d.add(String(52, 28, "SMART",    fontName="Helvetica-Bold", fontSize=13,
                 fillColor=NAVY_COLOR))
    d.add(String(52, 13, "TRADERS",  fontName="Helvetica-Bold", fontSize=13,
                 fillColor=RED_COLOR))

    return d


def _make_transparent_background(image_path: str) -> str:
    """
    Removes the background from a stamp or signature image.
    Uses flood-fill from corners to detect the background color,
    then makes pixels close to that color transparent.
    Works for both dark (black) and light (white/cream) backgrounds.
    Returns path to a temp PNG with transparent background.
    """
    try:
        from PIL import Image as PILImage
        import tempfile
        import numpy as np

        img = PILImage.open(image_path).convert("RGBA")
        arr = np.array(img, dtype=np.float32)

        # Sample the four corners to detect background color
        h, w = arr.shape[:2]
        corners = [
            arr[0, 0, :3],
            arr[0, w - 1, :3],
            arr[h - 1, 0, :3],
            arr[h - 1, w - 1, :3],
        ]
        bg_color = np.mean(corners, axis=0)  # Average corner color = background

        # Calculate per-pixel distance from background color
        diff = np.sqrt(np.sum((arr[:, :, :3] - bg_color) ** 2, axis=2))

        # Pixels within threshold of background color become transparent
        tolerance = 40.0
        mask = diff < tolerance

        result = arr.copy()
        result[mask, 3] = 0  # transparent
        result[~mask, 3] = 255  # fully opaque

        out_img = PILImage.fromarray(result.astype(np.uint8), "RGBA")
        tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        out_img.save(tmp.name, "PNG")
        tmp.close()
        return tmp.name

    except ImportError:
        # numpy not available, fall back to simple dark-pixel removal
        try:
            from PIL import Image as PILImage
            import tempfile

            img = PILImage.open(image_path).convert("RGBA")
            data = img.getdata()
            new_data = []
            for r, g, b, a in data:
                # Remove very dark (black bg) or very light (white bg) pixels
                is_dark  = r < 60 and g < 60 and b < 60
                is_light = r > 220 and g > 220 and b > 220
                if is_dark or is_light:
                    new_data.append((r, g, b, 0))
                else:
                    new_data.append((r, g, b, a))
            img.putdata(new_data)
            tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
            img.save(tmp.name, "PNG")
            tmp.close()
            return tmp.name
        except Exception:
            return image_path

    except Exception as e:
        logger.warning(f"Background removal failed for {image_path}: {e}")
        return image_path


class PDFService:
    @staticmethod
    def generate_invoice_pdf(
        invoice_data: Dict[str, Any],
        items_data: List[Dict[str, Any]],
        company_data: Optional[Dict[str, Any]] = None,
        output_path: Optional[str] = None
    ) -> str:
        """
        Generates a professional A4 PDF invoice strictly following the reference template layout.
        Returns the absolute filepath of the generated PDF.
        """
        if not output_path:
            inv_num = invoice_data.get("invoice_number", "draft")
            filename = f"Invoice_{inv_num}.pdf"
            output_path = str(EXPORT_DIR / filename)

        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            leftMargin=36,
            rightMargin=36,
            topMargin=28,
            bottomMargin=45
        )

        usable_width = 523.27  # A4 width (595.27) - 2 * 36

        company = company_data or {}
        comp_name = company.get("name", "POULTRY SMART TRADERS")
        comp_address = company.get("address", "23-A Gulshan Iqbal Alla Din Park, Karachi (Pak.)")
        comp_email = company.get("email", "poultrysmarttraders01@gmail.com")
        comp_phone = company.get("phone", "")
        sales_coord = company.get("sales_coordinator_name", "Dennis")

        elements = []

        # ==========================================
        # 1. HEADER SECTION
        # ==========================================
        logo_path = company.get("logo_path")
        if logo_path and os.path.exists(logo_path):
            try:
                logo_cell = RLImage(logo_path, width=130, height=52)
            except Exception:
                logo_cell = create_logo_drawing(comp_name)
        else:
            logo_cell = create_logo_drawing(comp_name)

        header_text_style = ParagraphStyle(
            "HeaderText",
            fontName="Helvetica-Bold",
            fontSize=16,
            leading=18,
            textColor=NAVY_COLOR,
            alignment=2
        )
        contact_style = ParagraphStyle(
            "HeaderContact",
            fontName="Helvetica",
            fontSize=8,
            leading=11,
            textColor=TEXT_DARK,
            alignment=2
        )

        contact_lines = [comp_address]
        if comp_email:
            contact_lines.append(f"<font color='{COLOR_RED_ACCENT}'>&#9993;</font> {comp_email}")
        if comp_phone:
            contact_lines.append(f"Tel: {comp_phone}")

        right_header_flowables = [
            Paragraph(f"<b>{comp_name}</b>", header_text_style),
            Spacer(1, 6),
            Paragraph("<br/>".join(contact_lines), contact_style)
        ]

        header_table = Table(
            [[logo_cell, right_header_flowables]],
            colWidths=[150, usable_width - 150]
        )
        header_table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        elements.append(header_table)
        elements.append(Spacer(1, 4))

        # ==========================================
        # 2. SALE INVOICE TITLE BANNER
        # ==========================================
        banner_style = ParagraphStyle(
            "BannerText",
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=15,
            textColor=colors.white,
            alignment=1
        )
        banner_title = invoice_data.get("title", "SALE INVOICE")
        banner_table = Table(
            [[Paragraph(banner_title, banner_style)]],
            colWidths=[usable_width],
            rowHeights=[20]
        )
        banner_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), NAVY_BG),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ]))
        elements.append(banner_table)

        # ==========================================
        # 3. METADATA GRID SECTION
        # ==========================================
        meta_label_style = ParagraphStyle("MetaLabel", fontName="Helvetica-Bold", fontSize=8.5, leading=10, textColor=TEXT_DARK)
        meta_val_style = ParagraphStyle("MetaVal", fontName="Helvetica-Bold", fontSize=9.5, leading=11, textColor=TEXT_NAVY)

        no_val = str(invoice_data.get("manual_no") or "")
        inv_num_val = str(invoice_data.get("invoice_number") or "")
        dc_1_val = str(invoice_data.get("dc_number_1") or "")
        dc_2_val = str(invoice_data.get("dc_number_2") or "")
        order_num_val = str(invoice_data.get("order_number") or "")
        date_val = format_date(invoice_data.get("invoice_date") or date.today())
        delivered_to_val = str(invoice_data.get("delivered_to") or "")
        invoiced_to_val = str(invoice_data.get("invoiced_to") or "Same")
        address_val = str(invoice_data.get("address") or "")

        meta_grid_data = [
            [
                Paragraph("No:", meta_label_style),
                Paragraph(no_val, meta_val_style),
                Paragraph("Invoice #:", meta_label_style),
                Paragraph(inv_num_val, meta_val_style),
                Paragraph("DC#:", meta_label_style),
                Paragraph(dc_1_val, meta_val_style),
            ],
            [
                Paragraph("Date:", meta_label_style),
                Paragraph(date_val, meta_val_style),
                Paragraph("Order #:", meta_label_style),
                Paragraph(order_num_val, meta_val_style),
                Paragraph("DC#:", meta_label_style),
                Paragraph(dc_2_val, meta_val_style),
            ],
            [
                Paragraph("Delivered To:", meta_label_style),
                Paragraph(delivered_to_val, meta_val_style),
                "",
                "",
                Paragraph("Invoiced To:", meta_label_style),
                Paragraph(invoiced_to_val, meta_val_style),
            ],
            [
                Paragraph("Address:", meta_label_style),
                Paragraph(address_val, meta_val_style),
                "", "", "", ""
            ]
        ]

        meta_table = Table(
            meta_grid_data,
            colWidths=[55, 95, 60, 80, 55, 178.27]
        )
        meta_table.setStyle(TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.7, BORDER_DARK),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ("SPAN", (1, 2), (3, 2)),
            ("SPAN", (1, 3), (5, 3)),
        ]))
        elements.append(meta_table)

        # ==========================================
        # 4. DISPATCH INFORMATION SECTION
        # ==========================================
        dispatch_val = str(invoice_data.get("dispatch_info") or "")
        dispatch_table = Table(
            [
                [
                    Paragraph("Dispatch Information:", meta_label_style),
                    Paragraph(dispatch_val, meta_val_style)
                ]
            ],
            colWidths=[110, usable_width - 110]
        )
        dispatch_table.setStyle(TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.7, BORDER_DARK),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ]))
        elements.append(dispatch_table)
        elements.append(Spacer(1, 4))

        # ==========================================
        # 5. PRODUCTS / ITEMS TABLE
        # ==========================================
        th_style = ParagraphStyle("TH", fontName="Helvetica-Bold", fontSize=8.5, leading=10, textColor=colors.white, alignment=1)
        th_left = ParagraphStyle("THL", fontName="Helvetica-Bold", fontSize=8.5, leading=10, textColor=colors.white, alignment=1)
        
        td_center = ParagraphStyle("TDC", fontName="Helvetica-Bold", fontSize=8.5, leading=10, textColor=TEXT_DARK, alignment=1)
        td_prod = ParagraphStyle("TDP", fontName="Helvetica-Bold", fontSize=9, leading=11, textColor=TEXT_NAVY, alignment=0)
        td_right = ParagraphStyle("TDR", fontName="Helvetica-Bold", fontSize=9, leading=11, textColor=TEXT_DARK, alignment=2)

        table_headers = [
            Paragraph("S No", th_style),
            Paragraph("Name of Product", th_left),
            Paragraph("Packing", th_style),
            Paragraph("Qty", th_style),
            Paragraph("Bonus", th_style),
            Paragraph("Unit Rate<br/>(Rs.)", th_style),
            Paragraph("Amount (Rs.)", th_style),
        ]

        items_rows = [table_headers]
        col_widths = [32, 185, 60, 60, 48, 68, 70.27]

        row_count = max(len(items_data), 8)

        for i in range(row_count):
            if i < len(items_data):
                item = items_data[i]
                sno = str(item.get("serial_no", i + 1))
                prod_name = str(item.get("product_name", ""))
                packing = str(item.get("packing", ""))
                qty_str = format_quantity_display(item.get("quantity_value", ""), item.get("quantity_unit", ""))
                bonus_str = str(item.get("bonus", "") or "")
                rate_str = format_currency(item.get("unit_rate", 0), decimals=0)
                amount_str = format_currency(item.get("amount", 0), decimals=0)

                items_rows.append([
                    Paragraph(sno, td_center),
                    Paragraph(prod_name, td_prod),
                    Paragraph(packing, td_center),
                    Paragraph(qty_str, td_center),
                    Paragraph(bonus_str, td_center),
                    Paragraph(rate_str, td_right),
                    Paragraph(amount_str, td_right),
                ])
            else:
                sno = str(i + 1)
                items_rows.append([
                    Paragraph(sno, td_center),
                    "", "", "", "", "", ""
                ])

        items_table = Table(
            items_rows,
            colWidths=col_widths,
            repeatRows=1
        )
        items_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), NAVY_BG),
            ("GRID", (0, 0), (-1, -1), 0.7, BORDER_DARK),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ]))
        elements.append(items_table)

        # ==========================================
        # 6. RUPEES IN WORDS & TOTALS SECTION
        # ==========================================
        gross_amt = format_currency(invoice_data.get("gross_amount") or invoice_data.get("subtotal") or 0, decimals=0)
        disc_amt = format_currency(invoice_data.get("discount_amount") or 0, decimals=0) if invoice_data.get("discount_amount") else ""
        inv_amt = format_currency(invoice_data.get("invoice_amount") or invoice_data.get("total_amount") or 0, decimals=0)
        total_due_amt = format_currency(invoice_data.get("total_due") or invoice_data.get("invoice_amount") or 0, decimals=0)
        
        words_val = str(invoice_data.get("amount_in_words") or "")
        if not words_val:
            words_val = amount_to_words(invoice_data.get("invoice_amount", 0), currency_name="", system="south_asian")

        words_style = ParagraphStyle(
            "WordsText",
            fontName="Helvetica-Bold",
            fontSize=9.5,
            leading=13,
            textColor=TEXT_DARK
        )
        total_label_style = ParagraphStyle("TotLbl", fontName="Helvetica-Bold", fontSize=8.5, leading=10, textColor=TEXT_DARK)
        total_val_style = ParagraphStyle("TotVal", fontName="Helvetica-Bold", fontSize=9.5, leading=11, textColor=TEXT_NAVY, alignment=2)
        total_val_white = ParagraphStyle("TotValW", fontName="Helvetica-Bold", fontSize=10, leading=12, textColor=colors.white, alignment=2)
        total_lbl_white = ParagraphStyle("TotLblW", fontName="Helvetica-Bold", fontSize=9, leading=11, textColor=colors.white)

        totals_right_table = Table(
            [
                [Paragraph("Gross Amount :", total_label_style), Paragraph(gross_amt, total_val_style)],
                [Paragraph("Discount:", total_label_style), Paragraph(disc_amt, total_val_style)],
                [Paragraph("Invoice Amount:", total_lbl_white), Paragraph(inv_amt, total_val_white)],
                [Paragraph("Total Due:", total_label_style), Paragraph(total_due_amt, total_val_style)],
            ],
            colWidths=[105, 133.27]
        )
        totals_right_table.setStyle(TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.7, BORDER_DARK),
            ("BACKGROUND", (0, 2), (1, 2), NAVY_BG),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ]))

        left_words_content = [
            Paragraph(f"<b>Rupees:</b> {words_val}", words_style)
        ]

        bottom_totals_table = Table(
            [[left_words_content, totals_right_table]],
            colWidths=[usable_width - 238.27, 238.27]
        )
        bottom_totals_table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ]))

        elements.append(bottom_totals_table)
        elements.append(Spacer(1, 10))

        # ==========================================
        # 7. STAMP & SIGNATURE SECTION
        # ==========================================
        stamp_path = company.get("stamp_path")
        if stamp_path and os.path.exists(stamp_path):
            try:
                clean_stamp_path = _make_transparent_background(stamp_path)
                stamp_cell = RLImage(clean_stamp_path, width=80, height=80)
            except Exception:
                stamp_cell = create_stamp_drawing(comp_name)
        else:
            stamp_cell = create_stamp_drawing(comp_name)

        signature_path = company.get("signature_path")
        if signature_path and os.path.exists(signature_path):
            try:
                clean_sig_path = _make_transparent_background(signature_path)
                sig_img = RLImage(clean_sig_path, width=130, height=55)

                # Build a mini-table: [image] / [line] / [Sales Coordinator label]
                _lbl_style = ParagraphStyle(
                    "SigLabel",
                    fontName="Helvetica",
                    fontSize=8.5,
                    leading=10,
                    textColor=TEXT_DARK,
                    alignment=1  # center
                )
                sig_line = Table(
                    [[""]],
                    colWidths=[140],
                    rowHeights=[0.8]
                )
                sig_line.setStyle(TableStyle([
                    ("LINEABOVE", (0, 0), (-1, -1), 0.8, BORDER_DARK),
                    ("TOPPADDING",    (0, 0), (-1, -1), 0),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                ]))

                signature_cell = Table(
                    [[sig_img],
                     [sig_line],
                     [Paragraph("Sales Coordinator", _lbl_style)]],
                    colWidths=[140]
                )
                signature_cell.setStyle(TableStyle([
                    ("ALIGN",         (0, 0), (-1, -1), "CENTER"),
                    ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
                    ("LEFTPADDING",   (0, 0), (-1, -1), 0),
                    ("RIGHTPADDING",  (0, 0), (-1, -1), 0),
                    ("TOPPADDING",    (0, 0), (-1, -1), 2),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                ]))

            except Exception:
                signature_cell = create_signature_drawing(sales_coord, "Sales Coordinator")
        else:
            signature_cell = create_signature_drawing(sales_coord, "Sales Coordinator")

        footer_sign_table = Table(
            [["", stamp_cell, signature_cell]],
            colWidths=[usable_width - 280, 120, 160]
        )
        footer_sign_table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
            ("ALIGN", (1, 0), (1, 0), "CENTER"),
            ("ALIGN", (2, 0), (2, 0), "CENTER"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ]))

        elements.append(KeepTogether([footer_sign_table]))

        doc.build(elements, canvasmaker=NumberedCanvas)
        logger.info(f"Successfully generated invoice PDF at: {output_path}")
        return output_path
