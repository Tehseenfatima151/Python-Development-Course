"""
Editable Products & Items Table Widget for InvoicePro — Redesigned
Columns: S No | Product | Packing | Qty [val][unit▼] | Billing Qty | Bonus | Unit Rate | Amount | Actions
Internal data model is unchanged: quantity_value, quantity_unit, billing_quantity preserved.
Signals and get_items_data()/set_items_data() interfaces are backward-compatible.
"""
from decimal import Decimal
from typing import List, Dict, Any

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QHeaderView, QLineEdit, QDoubleSpinBox, QComboBox,
    QLabel, QFrame, QSizePolicy
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QColor

from app.services.calculation_service import CalculationService, to_decimal
from app.utils.formatters import format_currency


# ──────────────────────────────────────────────────────────────────────────────
# Compact Qty widget: [spinbox] [unit combo] side by side
# ──────────────────────────────────────────────────────────────────────────────
class QtyWidget(QWidget):
    """Compact Qty + Unit control: [ 12.00 ] [ kg ▼ ]"""
    changed = Signal()

    def __init__(self, qty_val: float = 1.0, unit: str = "kg", parent=None):
        super().__init__(parent)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(2, 1, 2, 1)
        lay.setSpacing(2)

        self.spin = QDoubleSpinBox()
        self.spin.setRange(0.01, 999999.99)
        self.spin.setDecimals(2)
        self.spin.setValue(qty_val)
        self.spin.setButtonSymbols(QDoubleSpinBox.NoButtons)
        self.spin.setFixedWidth(62)
        self.spin.setStyleSheet(
            "QDoubleSpinBox { border: 1px solid #CBD5E1; border-radius: 3px;"
            " padding: 2px 4px; background: white; }"
        )
        lay.addWidget(self.spin)

        self.combo = QComboBox()
        self.combo.setEditable(True)
        self.combo.addItems(["kg", "liter", "pcs", "bags", "boxes", "bottles", "grams", "ml", "ton"])
        self.combo.setCurrentText(unit if unit else "kg")
        self.combo.setFixedWidth(62)
        self.combo.lineEdit().setPlaceholderText("unit")
        self.combo.setStyleSheet(
            "QComboBox { border: 1px solid #CBD5E1; border-radius: 3px;"
            " padding: 2px 4px; background: white; }"
            "QComboBox::drop-down { border: none; width: 16px; }"
        )
        lay.addWidget(self.combo)

        self.spin.valueChanged.connect(lambda: self.changed.emit())
        self.combo.currentTextChanged.connect(lambda: self.changed.emit())

    def value(self) -> float:
        return self.spin.value()

    def unit(self) -> str:
        return self.combo.currentText().strip()

    def set_value(self, val: float, unit: str):
        self.spin.blockSignals(True)
        self.combo.blockSignals(True)
        self.spin.setValue(val)
        self.combo.setCurrentText(unit if unit else "kg")
        self.spin.blockSignals(False)
        self.combo.blockSignals(False)


# ──────────────────────────────────────────────────────────────────────────────
# Main Items Table Widget
# ──────────────────────────────────────────────────────────────────────────────
class ItemsTableWidget(QWidget):
    """
    Professional editable line-items table for invoice creation.

    Visible columns (9):
        0  S No
        1  Product
        2  Packing
        3  Qty (QtyWidget: value + unit combo)
        4  Billing Qty
        5  Bonus
        6  Unit Rate (Rs.)
        7  Amount (Rs.)       ← auto-calculated, read-only
        8  Actions            ← duplicate / delete

    Internal data model preserves:
        quantity_value, quantity_unit, billing_quantity, bonus, unit_rate, amount
    """
    items_changed = Signal()

    # Column index constants
    COL_SNO        = 0
    COL_PRODUCT    = 1
    COL_PACKING    = 2
    COL_QTY        = 3   # QtyWidget
    COL_BILLING    = 4   # QDoubleSpinBox
    COL_BONUS      = 5
    COL_RATE       = 6   # QDoubleSpinBox
    COL_AMOUNT     = 7   # read-only QTableWidgetItem
    COL_ACTIONS    = 8

    HEADERS = ["#", "Product / Item Name", "Packing", "Qty", "Billing Qty", "Bonus", "Unit Rate", "Amount", ""]

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    # ──────────────────────────────────────────────────────────────────────────
    def _setup_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Card frame ────────────────────────────────────────────────────────
        card = QFrame()
        card.setObjectName("itemsCard")
        card.setStyleSheet(
            "#itemsCard { background: #FFFFFF; border: 1px solid #E2E8F0;"
            " border-radius: 8px; }"
        )
        card_lay = QVBoxLayout(card)
        card_lay.setContentsMargins(0, 0, 0, 0)
        card_lay.setSpacing(0)

        # ── Top bar ───────────────────────────────────────────────────────────
        top_bar = QWidget()
        top_bar.setStyleSheet("background: #0A2540; border-radius: 8px 8px 0 0;")
        top_bar_lay = QHBoxLayout(top_bar)
        top_bar_lay.setContentsMargins(12, 8, 12, 8)

        lbl_heading = QLabel("📦  Products / Line Items")
        lbl_heading.setFont(QFont("Segoe UI", 10, QFont.Bold))
        lbl_heading.setStyleSheet("color: white; background: transparent;")
        top_bar_lay.addWidget(lbl_heading)
        top_bar_lay.addStretch()

        self.btn_add = QPushButton("＋  Add Product")
        self.btn_add.setFixedHeight(30)
        self.btn_add.setCursor(Qt.PointingHandCursor)
        self.btn_add.setStyleSheet(
            "QPushButton { background: #C8102E; color: white; border: none;"
            " border-radius: 5px; padding: 4px 16px; font-weight: bold; font-size: 13px; }"
            "QPushButton:hover { background: #a50d24; }"
        )
        self.btn_add.clicked.connect(self.add_empty_row)
        top_bar_lay.addWidget(self.btn_add)

        btn_clear = QPushButton("Clear All")
        btn_clear.setFixedHeight(30)
        btn_clear.setCursor(Qt.PointingHandCursor)
        btn_clear.setStyleSheet(
            "QPushButton { background: transparent; color: #94A3B8; border: 1px solid #475569;"
            " border-radius: 5px; padding: 4px 12px; font-size: 12px; }"
            "QPushButton:hover { background: #1E3A8A; color: white; border-color: #1E3A8A; }"
        )
        btn_clear.clicked.connect(self.clear_all_rows)
        top_bar_lay.addWidget(btn_clear)

        card_lay.addWidget(top_bar)

        # ── Table ──────────────────────────────────────────────────────────────
        self.table = QTableWidget()
        self.table.setColumnCount(len(self.HEADERS))
        self.table.setHorizontalHeaderLabels(self.HEADERS)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setEditTriggers(QTableWidget.AllEditTriggers)
        self.table.setShowGrid(True)
        self.table.setGridStyle(Qt.SolidLine)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Row height
        self.table.verticalHeader().setDefaultSectionSize(36)
        self.table.setMinimumHeight(180)

        # Header styling
        header = self.table.horizontalHeader()
        header.setDefaultAlignment(Qt.AlignCenter)
        header.setHighlightSections(False)
        header.setStyleSheet(
            "QHeaderView::section {"
            " background-color: #1E3A8A; color: white;"
            " font-weight: bold; font-size: 11px;"
            " border: none; border-right: 1px solid #2D4EA2;"
            " padding: 5px 4px; }"
        )

        # Column widths & resize modes
        header.setSectionResizeMode(self.COL_SNO,     QHeaderView.Fixed)
        header.setSectionResizeMode(self.COL_PRODUCT, QHeaderView.Stretch)
        header.setSectionResizeMode(self.COL_PACKING, QHeaderView.Fixed)
        header.setSectionResizeMode(self.COL_QTY,     QHeaderView.Fixed)
        header.setSectionResizeMode(self.COL_BILLING, QHeaderView.Fixed)
        header.setSectionResizeMode(self.COL_BONUS,   QHeaderView.Fixed)
        header.setSectionResizeMode(self.COL_RATE,    QHeaderView.Fixed)
        header.setSectionResizeMode(self.COL_AMOUNT,  QHeaderView.Fixed)
        header.setSectionResizeMode(self.COL_ACTIONS, QHeaderView.Fixed)

        self.table.setColumnWidth(self.COL_SNO,     36)
        self.table.setColumnWidth(self.COL_PACKING,  72)
        self.table.setColumnWidth(self.COL_QTY,     138)  # QtyWidget: 62+62+2+padding
        self.table.setColumnWidth(self.COL_BILLING,  82)
        self.table.setColumnWidth(self.COL_BONUS,    58)
        self.table.setColumnWidth(self.COL_RATE,     92)
        self.table.setColumnWidth(self.COL_AMOUNT,   96)
        self.table.setColumnWidth(self.COL_ACTIONS,  58)

        self.table.setStyleSheet(
            "QTableWidget { border: none; background: #FFFFFF; gridline-color: #E2E8F0; }"
            "QTableWidget::item { padding: 2px 6px; }"
            "QTableWidget::item:alternate { background: #F8FAFC; }"
            "QTableWidget::item:selected { background: #DBEAFE; color: #0A2540; }"
        )

        card_lay.addWidget(self.table)
        root.addWidget(card)

    # ──────────────────────────────────────────────────────────────────────────
    # Public API
    # ──────────────────────────────────────────────────────────────────────────
    def add_empty_row(self):
        self.add_item_row({
            "product_name":    "",
            "packing":         "1kg",
            "quantity_value":  1.0,
            "quantity_unit":   "kg",
            "billing_quantity": 1.0,
            "bonus":           "",
            "unit_rate":       0.0,
            "amount":          0.0,
        })

    def add_item_row(self, data: Dict[str, Any]):
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setRowHeight(row, 36)

        # 0 ── S No (auto, read-only)
        sno = QTableWidgetItem(str(row + 1))
        sno.setTextAlignment(Qt.AlignCenter)
        sno.setFlags(Qt.ItemIsEnabled)
        sno.setFont(QFont("Segoe UI", 9, QFont.Bold))
        sno.setBackground(QColor("#F1F5F9"))
        self.table.setItem(row, self.COL_SNO, sno)

        # 1 ── Product Name
        edit_name = QLineEdit(str(data.get("product_name", "")))
        edit_name.setPlaceholderText("Enter product or item name")
        edit_name.setStyleSheet(
            "QLineEdit { border: none; border-bottom: 1px solid #CBD5E1;"
            " padding: 4px 6px; background: transparent; }"
            "QLineEdit:focus { border-bottom: 2px solid #0A2540; }"
        )
        edit_name.textChanged.connect(lambda: self._on_row_changed(row))
        self.table.setCellWidget(row, self.COL_PRODUCT, edit_name)

        # 2 ── Packing
        edit_packing = QLineEdit(str(data.get("packing", "")))
        edit_packing.setPlaceholderText("e.g. 1kg")
        edit_packing.setAlignment(Qt.AlignCenter)
        edit_packing.setStyleSheet(
            "QLineEdit { border: none; border-bottom: 1px solid #CBD5E1;"
            " padding: 4px 4px; background: transparent; }"
            "QLineEdit:focus { border-bottom: 2px solid #0A2540; }"
        )
        edit_packing.textChanged.connect(lambda: self._on_row_changed(row))
        self.table.setCellWidget(row, self.COL_PACKING, edit_packing)

        # 3 ── Qty widget (value + unit combo)
        qty_val  = float(data.get("quantity_value", 1.0) or 1.0)
        qty_unit = str(data.get("quantity_unit", "kg") or "kg")
        qty_w = QtyWidget(qty_val, qty_unit)
        qty_w.changed.connect(lambda: self._on_qty_changed(row))
        self.table.setCellWidget(row, self.COL_QTY, qty_w)

        # 4 ── Billing Qty
        spin_billing = QDoubleSpinBox()
        spin_billing.setRange(0.01, 999999.99)
        spin_billing.setDecimals(2)
        spin_billing.setValue(float(data.get("billing_quantity") or data.get("quantity_value", 1.0)))
        spin_billing.setButtonSymbols(QDoubleSpinBox.NoButtons)
        spin_billing.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        spin_billing.setStyleSheet(
            "QDoubleSpinBox { border: none; border-bottom: 1px solid #CBD5E1;"
            " padding: 4px 6px; background: transparent; }"
            "QDoubleSpinBox:focus { border-bottom: 2px solid #0A2540; }"
        )
        spin_billing.valueChanged.connect(lambda: self._on_row_changed(row))
        self.table.setCellWidget(row, self.COL_BILLING, spin_billing)

        # 5 ── Bonus
        edit_bonus = QLineEdit(str(data.get("bonus", "") or ""))
        edit_bonus.setPlaceholderText("0")
        edit_bonus.setAlignment(Qt.AlignCenter)
        edit_bonus.setStyleSheet(
            "QLineEdit { border: none; border-bottom: 1px solid #CBD5E1;"
            " padding: 4px 4px; background: transparent; }"
            "QLineEdit:focus { border-bottom: 2px solid #0A2540; }"
        )
        edit_bonus.textChanged.connect(lambda: self._on_row_changed(row))
        self.table.setCellWidget(row, self.COL_BONUS, edit_bonus)

        # 6 ── Unit Rate
        spin_rate = QDoubleSpinBox()
        spin_rate.setRange(0.0, 99999999.0)
        spin_rate.setDecimals(2)
        spin_rate.setValue(float(data.get("unit_rate", 0.0)))
        spin_rate.setButtonSymbols(QDoubleSpinBox.NoButtons)
        spin_rate.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        spin_rate.setStyleSheet(
            "QDoubleSpinBox { border: none; border-bottom: 1px solid #CBD5E1;"
            " padding: 4px 6px; background: transparent; }"
            "QDoubleSpinBox:focus { border-bottom: 2px solid #0A2540; }"
        )
        spin_rate.valueChanged.connect(lambda: self._on_row_changed(row))
        self.table.setCellWidget(row, self.COL_RATE, spin_rate)

        # 7 ── Amount (auto-calculated, read-only)
        amt_item = QTableWidgetItem("0")
        amt_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        amt_item.setFlags(Qt.ItemIsEnabled)
        amt_item.setFont(QFont("Segoe UI", 9, QFont.Bold))
        amt_item.setForeground(QColor("#0A2540"))
        self.table.setItem(row, self.COL_AMOUNT, amt_item)

        # 8 ── Actions (duplicate + delete)
        action_w = QWidget()
        action_lay = QHBoxLayout(action_w)
        action_lay.setContentsMargins(3, 2, 3, 2)
        action_lay.setSpacing(2)

        btn_dup = QPushButton("⧉")
        btn_dup.setToolTip("Duplicate row")
        btn_dup.setFixedSize(24, 24)
        btn_dup.setCursor(Qt.PointingHandCursor)
        btn_dup.setStyleSheet(
            "QPushButton { background: #E2E8F0; border: none; border-radius: 3px; font-size: 11px; }"
            "QPushButton:hover { background: #CBD5E1; }"
        )
        btn_dup.clicked.connect(lambda checked=False, r=row: self.duplicate_row(r))
        action_lay.addWidget(btn_dup)

        btn_del = QPushButton("🗑")
        btn_del.setToolTip("Delete row")
        btn_del.setFixedSize(24, 24)
        btn_del.setCursor(Qt.PointingHandCursor)
        btn_del.setStyleSheet(
            "QPushButton { background: #FEE2E2; border: none; border-radius: 3px; font-size: 11px; }"
            "QPushButton:hover { background: #EF4444; color: white; }"
        )
        btn_del.clicked.connect(lambda checked=False, r=row: self.delete_row(r))
        action_lay.addWidget(btn_del)

        self.table.setCellWidget(row, self.COL_ACTIONS, action_w)

        self._recalculate_row(row)
        self.items_changed.emit()

    # ──────────────────────────────────────────────────────────────────────────
    # Row events
    # ──────────────────────────────────────────────────────────────────────────
    def _on_qty_changed(self, row: int):
        """When physical Qty changes, auto-sync Billing Qty."""
        qty_w = self.table.cellWidget(row, self.COL_QTY)
        spin_billing = self.table.cellWidget(row, self.COL_BILLING)
        if qty_w and spin_billing:
            spin_billing.setValue(qty_w.value())
        self._on_row_changed(row)

    def _on_row_changed(self, row: int):
        self._recalculate_row(row)
        self.items_changed.emit()

    def _recalculate_row(self, row: int):
        if row >= self.table.rowCount():
            return
        spin_billing = self.table.cellWidget(row, self.COL_BILLING)
        spin_rate    = self.table.cellWidget(row, self.COL_RATE)
        amt_item     = self.table.item(row, self.COL_AMOUNT)
        if spin_billing and spin_rate and amt_item:
            qty  = Decimal(str(spin_billing.value()))
            rate = Decimal(str(spin_rate.value()))
            amt  = CalculationService.calculate_line_item(qty, rate)
            amt_item.setText(format_currency(amt, decimals=0))

    # ──────────────────────────────────────────────────────────────────────────
    # Row management
    # ──────────────────────────────────────────────────────────────────────────
    def duplicate_row(self, row: int):
        items = self.get_items_data()
        # Because get_items_data() skips empty rows, we need to count non-empty
        # but row index here refers to the actual table row.
        data = self._read_row_raw(row)
        if data:
            self.add_item_row(data)

    def delete_row(self, row: int):
        self.table.removeRow(row)
        self._renumber_rows()
        self.items_changed.emit()

    def clear_all_rows(self):
        self.table.setRowCount(0)
        self.items_changed.emit()

    def _renumber_rows(self):
        for r in range(self.table.rowCount()):
            item = self.table.item(r, self.COL_SNO)
            if item:
                item.setText(str(r + 1))

    # ──────────────────────────────────────────────────────────────────────────
    # Data interface (backward-compatible)
    # ──────────────────────────────────────────────────────────────────────────
    def _read_row_raw(self, r: int) -> Dict[str, Any]:
        """Read all fields from a single table row (including empty product names)."""
        edit_name    = self.table.cellWidget(r, self.COL_PRODUCT)
        edit_packing = self.table.cellWidget(r, self.COL_PACKING)
        qty_w        = self.table.cellWidget(r, self.COL_QTY)
        spin_billing = self.table.cellWidget(r, self.COL_BILLING)
        edit_bonus   = self.table.cellWidget(r, self.COL_BONUS)
        spin_rate    = self.table.cellWidget(r, self.COL_RATE)

        billing_val = to_decimal(spin_billing.value() if spin_billing else 1.0)
        rate_val    = to_decimal(spin_rate.value()    if spin_rate    else 0.0)
        amt_val     = CalculationService.calculate_line_item(billing_val, rate_val)
        qty_val     = to_decimal(qty_w.value()        if qty_w        else 1.0)
        qty_unit    = qty_w.unit()                     if qty_w        else "kg"

        return {
            "serial_no":       r + 1,
            "product_name":    edit_name.text().strip()    if edit_name    else "",
            "packing":         edit_packing.text().strip() if edit_packing else "",
            "quantity_value":  qty_val,
            "quantity_unit":   qty_unit,
            "billing_quantity": billing_val,
            "bonus":           edit_bonus.text().strip()   if edit_bonus   else "",
            "unit_rate":       rate_val,
            "discount_percent": Decimal("0.00"),
            "tax_percent":     Decimal("0.00"),
            "amount":          amt_val,
        }

    def get_items_data(self) -> List[Dict[str, Any]]:
        """Return list of non-empty rows. Backward-compatible."""
        items = []
        for r in range(self.table.rowCount()):
            data = self._read_row_raw(r)
            if data["product_name"]:   # skip completely empty rows
                items.append(data)
        return items

    def set_items_data(self, items: List[Dict[str, Any]]):
        """Load a list of item dicts into the table. Backward-compatible."""
        self.table.setRowCount(0)
        for item in items:
            self.add_item_row(item)
