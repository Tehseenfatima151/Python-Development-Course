"""
Live Invoice Preview Widget for InvoicePro
Renders a pixel-perfect, high-DPI visual representation of the reference invoice in real-time
as the user edits data in the form. Supports Zoom in/out, Print, and PDF export.
"""
import os
from decimal import Decimal
from typing import Dict, Any, List, Optional
from datetime import date

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea, QFrame, QFileDialog
)
from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtGui import (
    QPainter, QColor, QFont, QPen, QBrush, QPixmap, QPainterPath, QPolygonF
)

from app.config import (
    COLOR_NAVY_PRIMARY, COLOR_NAVY_DARK, COLOR_RED_ACCENT, EXPORT_DIR
)
from app.services.pdf_service import PDFService
from app.utils.formatters import format_currency, format_date, format_quantity_display
from app.utils.num_to_words import amount_to_words
from app.utils.helpers import open_file_in_system_viewer, print_file_with_system_dialog
from app.ui.components.toast import ToastNotification


class InvoiceCanvas(QWidget):
    """A4 Canvas Widget rendered with QPainter matching reference invoice."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.invoice_data: Dict[str, Any] = {}
        self.items_data: List[Dict[str, Any]] = []
        self.company_data: Dict[str, Any] = {}
        
        # A4 standard aspect ratio: 595 x 842 points
        self.base_w = 595
        self.base_h = 842
        self.zoom_factor = 1.0

        self.update_canvas_size()

    def update_canvas_size(self):
        w = int(self.base_w * self.zoom_factor)
        h = int(self.base_h * self.zoom_factor)
        self.setFixedSize(w, h)
        self.update()

    def set_zoom(self, factor: float):
        self.zoom_factor = max(0.5, min(2.5, factor))
        self.update_canvas_size()

    def set_data(self, invoice_data: Dict[str, Any], items_data: List[Dict[str, Any]], company_data: Dict[str, Any]):
        self.invoice_data = invoice_data or {}
        self.items_data = items_data or []
        self.company_data = company_data or {}
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing)

        # Scale coordinate system to match base A4 points
        painter.scale(self.zoom_factor, self.zoom_factor)

        # Draw A4 Paper with shadow
        paper_rect = QRectF(0, 0, self.base_w, self.base_h)
        painter.fillRect(paper_rect, QColor("#FFFFFF"))

        # Margin guides: 36 pt left & right
        margin_x = 36.0
        margin_y = 28.0
        usable_w = self.base_w - 2 * margin_x # 523 pt

        navy_color = QColor(COLOR_NAVY_DARK)
        red_color = QColor(COLOR_RED_ACCENT)
        border_pen = QPen(QColor("#000000"), 0.8)
        text_color = QColor("#0F172A")
        text_navy = QColor("#002D62")

        # ==========================================
        # 1. HEADER SECTION
        # ==========================================
        comp_name = self.company_data.get("name", "POULTRY SMART TRADERS")
        comp_address = self.company_data.get("address", "23-A Gulshan Iqbal Alla Din Park, Karachi (Pak.)")
        comp_email = self.company_data.get("email", "poultrysmarttraders01@gmail.com")
        sales_coord = self.company_data.get("sales_coordinator_name", "Dennis")

        # Logo on the left
        logo_path = self.company_data.get("logo_path")
        if logo_path and os.path.exists(logo_path):
            pix = QPixmap(logo_path)
            if not pix.isNull():
                painter.drawPixmap(int(margin_x), int(margin_y), 130, 50, pix)
        else:
            # ── Vector logo: navy C-bracket + red vertical bar + red diamond ──
            x = margin_x
            y = margin_y
            # Scale: logo fits in ~44x58 pt box
            s = 0.80  # scale factor to fit in header

            painter.setPen(Qt.NoPen)

            # Navy top horizontal arm
            painter.setBrush(QBrush(navy_color))
            painter.drawRect(QRectF(x,          y,           44*s, 8*s))
            # Navy right vertical (top half)
            painter.drawRect(QRectF(x + 32*s,   y,           12*s, 26*s))
            # Navy middle horizontal
            painter.drawRect(QRectF(x,          y + 18*s,    40*s, 8*s))
            # Navy left vertical (bottom half)
            painter.drawRect(QRectF(x,          y + 18*s,    8*s,  26*s))
            # Navy bottom horizontal arm
            painter.drawRect(QRectF(x,          y + 36*s,    44*s, 8*s))

            # Red vertical bar (center I-beam)
            painter.setBrush(QBrush(red_color))
            painter.drawRect(QRectF(x + 14*s,   y + 4*s,     12*s, 36*s))

            # Red small diamond accent (bottom-left)
            painter.drawRect(QRectF(x,           y + 46*s,    6*s,  5*s))

            # Text labels
            painter.setPen(text_color)
            painter.setFont(QFont("Arial", 10, QFont.Bold))
            painter.drawText(int(x + 50), int(y + 14), "Poultry")
            painter.setPen(navy_color)
            painter.setFont(QFont("Arial", 11, QFont.Bold))
            painter.drawText(int(x + 50), int(y + 28), "SMART")
            painter.setPen(red_color)
            painter.setFont(QFont("Arial", 11, QFont.Bold))
            painter.drawText(int(x + 50), int(y + 43), "TRADERS")

        # Right company header
        painter.setPen(navy_color)
        painter.setFont(QFont("Arial", 15, QFont.Bold))
        painter.drawText(QRectF(margin_x, margin_y, usable_w, 22), Qt.AlignRight, comp_name)

        # Contact text (directly below company name, no divider line)
        contact_y = margin_y + 26
        painter.setPen(text_color)
        painter.setFont(QFont("Arial", 8))
        painter.drawText(QRectF(margin_x, contact_y, usable_w, 14), Qt.AlignRight, comp_address)
        painter.drawText(QRectF(margin_x, contact_y + 14, usable_w, 14), Qt.AlignRight, f"✉ {comp_email}")

        # ==========================================
        # 2. SALE INVOICE TITLE BANNER
        # ==========================================
        banner_y = margin_y + 60
        painter.fillRect(QRectF(margin_x, banner_y, usable_w, 20), navy_color)
        painter.setPen(QColor("#FFFFFF"))
        painter.setFont(QFont("Arial", 11, QFont.Bold))
        painter.drawText(QRectF(margin_x, banner_y, usable_w, 20), Qt.AlignCenter, "SALE INVOICE")

        # ==========================================
        # 3. METADATA GRID SECTION
        # ==========================================
        grid_y = banner_y + 20
        grid_h = 76.0
        painter.setPen(border_pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(QRectF(margin_x, grid_y, usable_w, grid_h))

        # Horizontal lines for rows
        r1_y = grid_y + 18
        r2_y = grid_y + 36
        r3_y = grid_y + 56
        painter.drawLine(QPointF(margin_x, r1_y), QPointF(margin_x + usable_w, r1_y))
        painter.drawLine(QPointF(margin_x, r2_y), QPointF(margin_x + usable_w, r2_y))
        painter.drawLine(QPointF(margin_x, r3_y), QPointF(margin_x + usable_w, r3_y))

        # Vertical column lines
        c1_w = 150.0
        c2_w = 140.0
        c3_w = usable_w - (c1_w + c2_w)

        # Row 1 & 2 columns
        painter.drawLine(QPointF(margin_x + 45, grid_y), QPointF(margin_x + 45, r2_y))
        painter.drawLine(QPointF(margin_x + c1_w, grid_y), QPointF(margin_x + c1_w, r2_y))
        painter.drawLine(QPointF(margin_x + c1_w + 60, grid_y), QPointF(margin_x + c1_w + 60, r2_y))
        painter.drawLine(QPointF(margin_x + c1_w + c2_w, grid_y), QPointF(margin_x + c1_w + c2_w, r3_y))
        painter.drawLine(QPointF(margin_x + c1_w + c2_w + 45, grid_y), QPointF(margin_x + c1_w + c2_w + 45, r2_y))

        # Row 3 Delivered To / Invoiced To line
        painter.drawLine(QPointF(margin_x + 85, r2_y), QPointF(margin_x + 85, r3_y))
        painter.drawLine(QPointF(margin_x + c1_w + c2_w + 70, r2_y), QPointF(margin_x + c1_w + c2_w + 70, r3_y))

        # Row 4 Address line
        painter.drawLine(QPointF(margin_x + 60, r3_y), QPointF(margin_x + 60, grid_y + grid_h))

        # Draw Labels and Values
        painter.setFont(QFont("Arial", 8, QFont.Bold))
        painter.setPen(text_color)
        painter.drawText(QRectF(margin_x + 4, grid_y + 2, 40, 15), Qt.AlignLeft | Qt.AlignVCenter, "No:")
        painter.drawText(QRectF(margin_x + c1_w + 4, grid_y + 2, 55, 15), Qt.AlignLeft | Qt.AlignVCenter, "Invoice #:")
        painter.drawText(QRectF(margin_x + c1_w + c2_w + 4, grid_y + 2, 40, 15), Qt.AlignLeft | Qt.AlignVCenter, "DC#:")

        painter.drawText(QRectF(margin_x + 4, r1_y + 2, 40, 15), Qt.AlignLeft | Qt.AlignVCenter, "Date:")
        painter.drawText(QRectF(margin_x + c1_w + 4, r1_y + 2, 55, 15), Qt.AlignLeft | Qt.AlignVCenter, "Order #:")
        painter.drawText(QRectF(margin_x + c1_w + c2_w + 4, r1_y + 2, 40, 15), Qt.AlignLeft | Qt.AlignVCenter, "DC#:")

        painter.drawText(QRectF(margin_x + 4, r2_y + 2, 80, 16), Qt.AlignLeft | Qt.AlignVCenter, "Delivered To:")
        painter.drawText(QRectF(margin_x + c1_w + c2_w + 4, r2_y + 2, 65, 16), Qt.AlignLeft | Qt.AlignVCenter, "Invoiced To:")
        painter.drawText(QRectF(margin_x + 4, r3_y + 2, 55, 16), Qt.AlignLeft | Qt.AlignVCenter, "Address:")

        # Values
        painter.setPen(text_navy)
        painter.setFont(QFont("Arial", 9, QFont.Bold))
        painter.drawText(QRectF(margin_x + 48, grid_y + 2, 95, 15), Qt.AlignLeft | Qt.AlignVCenter, str(self.invoice_data.get("manual_no") or ""))
        painter.drawText(QRectF(margin_x + c1_w + 64, grid_y + 2, 70, 15), Qt.AlignLeft | Qt.AlignVCenter, str(self.invoice_data.get("invoice_number") or ""))
        painter.drawText(QRectF(margin_x + c1_w + c2_w + 48, grid_y + 2, 170, 15), Qt.AlignLeft | Qt.AlignVCenter, str(self.invoice_data.get("dc_number_1") or ""))

        date_str = format_date(self.invoice_data.get("invoice_date") or date.today())
        painter.drawText(QRectF(margin_x + 48, r1_y + 2, 95, 15), Qt.AlignLeft | Qt.AlignVCenter, date_str)
        painter.drawText(QRectF(margin_x + c1_w + 64, r1_y + 2, 70, 15), Qt.AlignLeft | Qt.AlignVCenter, str(self.invoice_data.get("order_number") or ""))
        painter.drawText(QRectF(margin_x + c1_w + c2_w + 48, r1_y + 2, 170, 15), Qt.AlignLeft | Qt.AlignVCenter, str(self.invoice_data.get("dc_number_2") or ""))

        painter.drawText(QRectF(margin_x + 90, r2_y + 2, c1_w + c2_w - 90, 16), Qt.AlignLeft | Qt.AlignVCenter, str(self.invoice_data.get("delivered_to") or ""))
        painter.drawText(QRectF(margin_x + c1_w + c2_w + 74, r2_y + 2, 150, 16), Qt.AlignLeft | Qt.AlignVCenter, str(self.invoice_data.get("invoiced_to") or "Same"))
        painter.drawText(QRectF(margin_x + 64, r3_y + 2, usable_w - 68, 16), Qt.AlignLeft | Qt.AlignVCenter, str(self.invoice_data.get("address") or ""))

        # ==========================================
        # 4. DISPATCH INFORMATION SECTION
        # ==========================================
        disp_y = grid_y + grid_h
        disp_h = 18.0
        painter.setPen(border_pen)
        painter.drawRect(QRectF(margin_x, disp_y, usable_w, disp_h))
        painter.drawLine(QPointF(margin_x + 110, disp_y), QPointF(margin_x + 110, disp_y + disp_h))

        painter.setPen(text_color)
        painter.setFont(QFont("Arial", 8, QFont.Bold))
        painter.drawText(QRectF(margin_x + 4, disp_y + 2, 105, 14), Qt.AlignLeft | Qt.AlignVCenter, "Dispatch Information:")
        painter.setPen(text_navy)
        painter.setFont(QFont("Arial", 8.5, QFont.Bold))
        painter.drawText(QRectF(margin_x + 114, disp_y + 2, usable_w - 118, 14), Qt.AlignLeft | Qt.AlignVCenter, str(self.invoice_data.get("dispatch_info") or ""))

        # ==========================================
        # 5. PRODUCTS / ITEMS TABLE
        # ==========================================
        table_y = disp_y + disp_h + 4
        th_h = 20.0
        
        col_w = [32.0, 185.0, 60.0, 60.0, 48.0, 68.0, 70.27]
        col_x = [margin_x]
        for w in col_w:
            col_x.append(col_x[-1] + w)

        # Header background
        painter.fillRect(QRectF(margin_x, table_y, usable_w, th_h), navy_color)
        painter.setPen(QColor("#FFFFFF"))
        painter.setFont(QFont("Arial", 8, QFont.Bold))

        headers_titles = ["S No", "Name of Product", "Packing", "Qty", "Bonus", "Unit Rate\n(Rs.)", "Amount (Rs.)"]
        for idx, title in enumerate(headers_titles):
            align = Qt.AlignCenter
            if idx == 1:
                align = Qt.AlignLeft | Qt.AlignVCenter
            rect = QRectF(col_x[idx] + 2, table_y, col_w[idx] - 4, th_h)
            painter.drawText(rect, align, title)

        # Table rows
        row_h = 21.0
        row_count = max(len(self.items_data), 8)
        current_y = table_y + th_h

        painter.setPen(border_pen)

        for r in range(row_count):
            painter.drawRect(QRectF(margin_x, current_y, usable_w, row_h))
            for x in col_x[1:-1]:
                painter.drawLine(QPointF(x, current_y), QPointF(x, current_y + row_h))

            if r < len(self.items_data):
                item = self.items_data[r]
                sno = str(item.get("serial_no", r + 1))
                pname = str(item.get("product_name", ""))
                packing = str(item.get("packing", ""))
                qty_str = format_quantity_display(item.get("quantity_value", ""), item.get("quantity_unit", ""))
                bonus = str(item.get("bonus", "") or "")
                rate_str = format_currency(item.get("unit_rate", 0), decimals=0)
                amt_str = format_currency(item.get("amount", 0), decimals=0)

                painter.setPen(text_color)
                painter.setFont(QFont("Arial", 8.5, QFont.Bold))
                painter.drawText(QRectF(col_x[0], current_y, col_w[0], row_h), Qt.AlignCenter, sno)

                painter.setPen(text_navy)
                painter.setFont(QFont("Arial", 9, QFont.Bold))
                painter.drawText(QRectF(col_x[1] + 4, current_y, col_w[1] - 8, row_h), Qt.AlignLeft | Qt.AlignVCenter, pname)

                painter.setPen(text_color)
                painter.setFont(QFont("Arial", 8.5, QFont.Bold))
                painter.drawText(QRectF(col_x[2], current_y, col_w[2], row_h), Qt.AlignCenter, packing)
                painter.drawText(QRectF(col_x[3], current_y, col_w[3], row_h), Qt.AlignCenter, qty_str)
                painter.drawText(QRectF(col_x[4], current_y, col_w[4], row_h), Qt.AlignCenter, bonus)
                painter.drawText(QRectF(col_x[5] + 2, current_y, col_w[5] - 6, row_h), Qt.AlignRight | Qt.AlignVCenter, rate_str)
                painter.drawText(QRectF(col_x[6] + 2, current_y, col_w[6] - 6, row_h), Qt.AlignRight | Qt.AlignVCenter, amt_str)
            else:
                # Empty row placeholder
                painter.setPen(text_color)
                painter.setFont(QFont("Arial", 8.5, QFont.Bold))
                painter.drawText(QRectF(col_x[0], current_y, col_w[0], row_h), Qt.AlignCenter, str(r + 1))

            current_y += row_h

        # ==========================================
        # 6. RUPEES IN WORDS & TOTALS SECTION
        # ==========================================
        totals_y = current_y + 2
        totals_w = 238.27
        totals_x = margin_x + usable_w - totals_w
        words_w = usable_w - totals_w

        gross_amt = format_currency(self.invoice_data.get("gross_amount") or self.invoice_data.get("subtotal") or 0, decimals=0)
        disc_amt = format_currency(self.invoice_data.get("discount_amount") or 0, decimals=0) if self.invoice_data.get("discount_amount") else ""
        inv_amt = format_currency(self.invoice_data.get("invoice_amount") or self.invoice_data.get("total_amount") or 0, decimals=0)
        total_due = format_currency(self.invoice_data.get("total_due") or self.invoice_data.get("invoice_amount") or 0, decimals=0)
        words_val = str(self.invoice_data.get("amount_in_words") or amount_to_words(self.invoice_data.get("invoice_amount", 0)))

        # Rupees in words on left
        painter.setPen(text_color)
        painter.setFont(QFont("Arial", 9.5, QFont.Bold))
        painter.drawText(QRectF(margin_x, totals_y + 2, words_w - 10, 60), Qt.AlignLeft | Qt.TextWordWrap, f"Rupees: {words_val}")

        # Totals box on right
        tot_row_h = 16.0
        tot_labels = [("Gross Amount :", gross_amt, False), ("Discount:", disc_amt, False), ("Invoice Amount:", inv_amt, True), ("Total Due:", total_due, False)]

        curr_tot_y = totals_y
        for lbl, val, is_highlight in tot_labels:
            painter.setPen(border_pen)
            if is_highlight:
                painter.fillRect(QRectF(totals_x, curr_tot_y, totals_w, tot_row_h), navy_color)
                painter.setPen(QPen(QColor("#000000"), 0.8))
                painter.drawRect(QRectF(totals_x, curr_tot_y, totals_w, tot_row_h))
                painter.drawLine(QPointF(totals_x + 105, curr_tot_y), QPointF(totals_x + 105, curr_tot_y + tot_row_h))

                painter.setPen(QColor("#FFFFFF"))
                painter.setFont(QFont("Arial", 9, QFont.Bold))
                painter.drawText(QRectF(totals_x + 4, curr_tot_y + 1, 98, tot_row_h - 2), Qt.AlignLeft | Qt.AlignVCenter, lbl)
                painter.drawText(QRectF(totals_x + 108, curr_tot_y + 1, totals_w - 114, tot_row_h - 2), Qt.AlignRight | Qt.AlignVCenter, val)
            else:
                painter.drawRect(QRectF(totals_x, curr_tot_y, totals_w, tot_row_h))
                painter.drawLine(QPointF(totals_x + 105, curr_tot_y), QPointF(totals_x + 105, curr_tot_y + tot_row_h))

                painter.setPen(text_color)
                painter.setFont(QFont("Arial", 8.5, QFont.Bold))
                painter.drawText(QRectF(totals_x + 4, curr_tot_y + 1, 98, tot_row_h - 2), Qt.AlignLeft | Qt.AlignVCenter, lbl)
                painter.setPen(text_navy)
                painter.drawText(QRectF(totals_x + 108, curr_tot_y + 1, totals_w - 114, tot_row_h - 2), Qt.AlignRight | Qt.AlignVCenter, val)

            curr_tot_y += tot_row_h

        # ==========================================
        # 7. STAMP & SIGNATURE SECTION
        # ==========================================
        sign_y = curr_tot_y + 15
        stamp_size = 70.0
        stamp_cx = margin_x + usable_w - 200
        stamp_cy = sign_y + 35

        # Try to draw the actual stamp image (with background removed)
        stamp_path = self.company_data.get("stamp_path")
        if stamp_path and os.path.exists(stamp_path):
            try:
                from PIL import Image as PILImage
                import tempfile, numpy as np
                img = PILImage.open(stamp_path).convert("RGBA")
                arr = np.array(img, dtype=np.float32)
                h2, w2 = arr.shape[:2]
                corners = [arr[0,0,:3], arr[0,w2-1,:3], arr[h2-1,0,:3], arr[h2-1,w2-1,:3]]
                bg = np.mean(corners, axis=0)
                diff = np.sqrt(np.sum((arr[:,:,:3] - bg)**2, axis=2))
                arr[diff < 40, 3] = 0
                arr[diff >= 40, 3] = 255
                out = PILImage.fromarray(arr.astype(np.uint8), "RGBA")
                tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
                out.save(tmp.name, "PNG")
                tmp.close()
                stamp_pix = QPixmap(tmp.name)
                if not stamp_pix.isNull():
                    target = QRectF(stamp_cx - stamp_size / 2, stamp_cy - stamp_size / 2, stamp_size, stamp_size)
                    painter.drawPixmap(target.toRect(), stamp_pix)
            except Exception:
                # Fall through to vector stamp
                painter.setPen(QPen(navy_color, 1.2))
                painter.setBrush(Qt.NoBrush)
                painter.drawEllipse(QPointF(stamp_cx, stamp_cy), 32, 32)
                painter.drawEllipse(QPointF(stamp_cx, stamp_cy), 28, 28)
                painter.drawEllipse(QPointF(stamp_cx, stamp_cy), 20, 20)
        else:
            # Vector placeholder stamp
            painter.setPen(QPen(navy_color, 1.2))
            painter.setBrush(Qt.NoBrush)
            painter.drawEllipse(QPointF(stamp_cx, stamp_cy), 32, 32)
            painter.drawEllipse(QPointF(stamp_cx, stamp_cy), 28, 28)
            painter.drawEllipse(QPointF(stamp_cx, stamp_cy), 20, 20)
            painter.setFont(QFont("Arial", 5, QFont.Bold))
            painter.setPen(navy_color)
            painter.drawText(QRectF(stamp_cx - 20, stamp_cy - 16, 40, 10), Qt.AlignCenter, "POULTRY")
            painter.drawText(QRectF(stamp_cx - 20, stamp_cy - 8,  40, 10), Qt.AlignCenter, "SMART")
            painter.drawText(QRectF(stamp_cx - 20, stamp_cy,      40, 10), Qt.AlignCenter, "TRADERS")
            painter.setFont(QFont("Arial", 3.5))
            painter.drawText(QRectF(stamp_cx - 25, stamp_cy + 8,  50, 8),  Qt.AlignCenter, "Karachi (Pak.)")

        # Signature on right
        sig_x = margin_x + usable_w - 130
        sig_img_path = self.company_data.get("signature_path")

        if sig_img_path and os.path.exists(sig_img_path):
            # Draw custom signature image with background removed
            try:
                from PIL import Image as PILImage
                import tempfile, numpy as np
                img = PILImage.open(sig_img_path).convert("RGBA")
                arr = np.array(img, dtype=np.float32)
                h2, w2 = arr.shape[:2]
                corners = [arr[0,0,:3], arr[0,w2-1,:3], arr[h2-1,0,:3], arr[h2-1,w2-1,:3]]
                bg = np.mean(corners, axis=0)
                diff = np.sqrt(np.sum((arr[:,:,:3] - bg)**2, axis=2))
                arr[diff < 40, 3] = 0
                arr[diff >= 40, 3] = 255
                out = PILImage.fromarray(arr.astype(np.uint8), "RGBA")
                tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
                out.save(tmp.name, "PNG")
                tmp.close()
                sig_pix = QPixmap(tmp.name)
                if not sig_pix.isNull():
                    painter.drawPixmap(
                        QRectF(sig_x - 55, sign_y + 5, 130, 40).toRect(),
                        sig_pix
                    )
            except Exception:
                # Fall back to vector name
                painter.setFont(QFont("Times New Roman", 16, QFont.StyleItalic))
                painter.setPen(navy_color)
                painter.drawText(QRectF(sig_x - 30, sign_y + 15, 120, 25), Qt.AlignCenter, sales_coord)
        else:
            # Vector italic name
            painter.setFont(QFont("Times New Roman", 16, QFont.StyleItalic))
            painter.setPen(navy_color)
            painter.drawText(QRectF(sig_x - 30, sign_y + 15, 120, 25), Qt.AlignCenter, sales_coord)

        # Line and label always shown beneath signature
        painter.setPen(border_pen)
        painter.drawLine(QPointF(sig_x - 55, sign_y + 48), QPointF(sig_x + 75, sign_y + 48))

        painter.setFont(QFont("Arial", 8.5))
        painter.setPen(text_color)
        painter.drawText(QRectF(sig_x - 55, sign_y + 50, 130, 15), Qt.AlignCenter, "Sales Coordinator")

        # ==========================================
        # 8. BOTTOM DECORATIVE FOOTER SWOOSH
        # ==========================================
        # Red swoosh
        p_red_foot = QPainterPath()
        p_red_foot.moveTo(0, self.base_h)
        p_red_foot.lineTo(0, self.base_h - 24)
        p_red_foot.quadTo(self.base_w * 0.4, self.base_h - 32, self.base_w, self.base_h - 10)
        p_red_foot.lineTo(self.base_w, self.base_h)
        p_red_foot.closeSubpath()
        painter.fillPath(p_red_foot, QBrush(red_color))

        # Navy swoosh
        p_navy_foot = QPainterPath()
        p_navy_foot.moveTo(0, self.base_h)
        p_navy_foot.lineTo(0, self.base_h - 14)
        p_navy_foot.quadTo(self.base_w * 0.45, self.base_h - 20, self.base_w, self.base_h - 4)
        p_navy_foot.lineTo(self.base_w, self.base_h)
        p_navy_foot.closeSubpath()
        painter.fillPath(p_navy_foot, QBrush(navy_color))
        painter.end()


class InvoicePreviewWidget(QWidget):
    """Container widget with zoom controls, toolbar, and scrollable canvas."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.invoice_data: Dict[str, Any] = {}
        self.items_data: List[Dict[str, Any]] = []
        self.company_data: Dict[str, Any] = {}
        self.last_generated_pdf_path: Optional[str] = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        # Toolbar
        toolbar = QHBoxLayout()
        toolbar.setContentsMargins(8, 6, 8, 6)

        lbl_title = QLabel("Live Invoice Preview")
        lbl_title.setFont(QFont("Segoe UI", 11, QFont.Bold))
        lbl_title.setStyleSheet("color: #0A2540;")
        toolbar.addWidget(lbl_title)

        toolbar.addStretch()

        btn_zoom_out = QPushButton("🔍 -")
        btn_zoom_out.setToolTip("Zoom Out")
        btn_zoom_out.setFixedSize(36, 28)
        btn_zoom_out.clicked.connect(self.zoom_out)
        toolbar.addWidget(btn_zoom_out)

        self.lbl_zoom = QLabel("100%")
        self.lbl_zoom.setFont(QFont("Segoe UI", 9))
        toolbar.addWidget(self.lbl_zoom)

        btn_zoom_in = QPushButton("🔍 +")
        btn_zoom_in.setToolTip("Zoom In")
        btn_zoom_in.setFixedSize(36, 28)
        btn_zoom_in.clicked.connect(self.zoom_in)
        toolbar.addWidget(btn_zoom_in)

        btn_fit = QPushButton("Fit")
        btn_fit.setToolTip("Fit Width")
        btn_fit.setFixedSize(40, 28)
        btn_fit.clicked.connect(self.fit_to_width)
        toolbar.addWidget(btn_fit)

        btn_open_pdf = QPushButton("📄 Open PDF")
        btn_open_pdf.setFixedHeight(28)
        btn_open_pdf.setCursor(Qt.PointingHandCursor)
        btn_open_pdf.setStyleSheet("""
            QPushButton { background-color:#FFFFFF; color:#334155; font-size:12px;
                border:1px solid #CBD5E1; border-radius:5px; padding:4px 12px; }
            QPushButton:hover   { background-color:#F1F5F9; border-color:#94A3B8; }
        """)
        btn_open_pdf.clicked.connect(self.generate_and_open_pdf)
        toolbar.addWidget(btn_open_pdf)

        btn_print = QPushButton("🖨 Print")
        btn_print.setFixedHeight(28)
        btn_print.setCursor(Qt.PointingHandCursor)
        btn_print.setStyleSheet("""
            QPushButton { background-color:#FFFFFF; color:#334155; font-size:12px;
                border:1px solid #CBD5E1; border-radius:5px; padding:4px 12px; }
            QPushButton:hover   { background-color:#F1F5F9; border-color:#94A3B8; }
        """)
        btn_print.clicked.connect(self.print_invoice)
        toolbar.addWidget(btn_print)

        layout.addLayout(toolbar)

        # Scroll Area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(False)
        self.scroll_area.setAlignment(Qt.AlignCenter)
        self.scroll_area.setStyleSheet("background-color: #E2E8F0; border: none;")

        self.canvas = InvoiceCanvas()
        self.scroll_area.setWidget(self.canvas)
        layout.addWidget(self.scroll_area)

    def update_preview(self, invoice_data: Dict[str, Any], items_data: List[Dict[str, Any]], company_data: Dict[str, Any]):
        self.invoice_data = invoice_data
        self.items_data = items_data
        self.company_data = company_data
        self.canvas.set_data(invoice_data, items_data, company_data)

    def zoom_in(self):
        new_factor = self.canvas.zoom_factor + 0.15
        self.canvas.set_zoom(new_factor)
        self.lbl_zoom.setText(f"{int(self.canvas.zoom_factor * 100)}%")

    def zoom_out(self):
        new_factor = self.canvas.zoom_factor - 0.15
        self.canvas.set_zoom(new_factor)
        self.lbl_zoom.setText(f"{int(self.canvas.zoom_factor * 100)}%")

    def fit_to_width(self):
        """Fit the full A4 page within the visible viewport (width and height).
        Uses the more constraining dimension so nothing is clipped."""
        vp = self.scroll_area.viewport()
        avail_w = vp.width()  - 20
        avail_h = vp.height() - 20
        if avail_w > 50 and avail_h > 50:
            factor_w = avail_w / self.canvas.base_w
            factor_h = avail_h / self.canvas.base_h
            factor   = min(factor_w, factor_h)
            self.canvas.set_zoom(max(0.3, factor))
            self.lbl_zoom.setText(f"{int(self.canvas.zoom_factor * 100)}%")

    def generate_and_open_pdf(self):
        try:
            pdf_path = PDFService.generate_invoice_pdf(
                self.invoice_data,
                self.items_data,
                self.company_data
            )
            self.last_generated_pdf_path = pdf_path
            open_file_in_system_viewer(pdf_path)
            ToastNotification.show_toast(self.window(), "PDF generated and opened successfully!", "success")
        except Exception as e:
            ToastNotification.show_toast(self.window(), f"PDF generation error: {e}", "danger")

    def print_invoice(self):
        try:
            if not self.last_generated_pdf_path or not os.path.exists(self.last_generated_pdf_path):
                self.last_generated_pdf_path = PDFService.generate_invoice_pdf(
                    self.invoice_data,
                    self.items_data,
                    self.company_data
                )
            print_file_with_system_dialog(self.last_generated_pdf_path)
            ToastNotification.show_toast(self.window(), "Sending invoice to printer...", "info")
        except Exception as e:
            ToastNotification.show_toast(self.window(), f"Printing error: {e}", "danger")
