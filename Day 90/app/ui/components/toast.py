"""
Toast Notification Widget for InvoicePro
Displays unobtrusive modern animated notification pills.
"""
from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QGraphicsOpacityEffect
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QPoint
from PySide6.QtGui import QFont, QColor
from app.config import COLOR_NAVY_PRIMARY, COLOR_SUCCESS, COLOR_WARNING, COLOR_DANGER


class ToastNotification(QWidget):
    def __init__(self, message: str, toast_type: str = "success", duration_ms: int = 3500, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.SubWindow)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setFixedHeight(46)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(18, 8, 18, 8)
        layout.setSpacing(10)

        # Icon and background colors
        colors_map = {
            "success": ("#10B981", "#ECFDF5", "#065F46", "✔"),
            "warning": ("#F59E0B", "#FFFBEB", "#92400E", "⚠"),
            "danger": ("#EF4444", "#FEF2F2", "#991B1B", "✖"),
            "info": ("#3B82F6", "#EFF6FF", "#1E40AF", "ℹ")
        }
        border_c, bg_c, text_c, icon_sym = colors_map.get(toast_type, colors_map["info"])

        self.setStyleSheet(f"""
            QWidget {{
                background-color: {bg_c};
                border: 1.5px solid {border_c};
                border-radius: 8px;
            }}
        """)

        lbl_icon = QLabel(icon_sym)
        lbl_icon.setFont(QFont("Segoe UI", 12, QFont.Bold))
        lbl_icon.setStyleSheet(f"color: {border_c}; border: none; background: transparent;")
        layout.addWidget(lbl_icon)

        lbl_msg = QLabel(message)
        lbl_msg.setFont(QFont("Segoe UI", 10, QFont.DemiBold))
        lbl_msg.setStyleSheet(f"color: {text_c}; border: none; background: transparent;")
        layout.addWidget(lbl_msg)

        # Opacity animation
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)

        self.anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.anim.setDuration(250)
        self.anim.setStartValue(0.0)
        self.anim.setEndValue(1.0)
        self.anim.start()

        # Auto hide timer
        QTimer.singleShot(duration_ms, self.fade_out)

    def fade_out(self):
        self.anim_out = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.anim_out.setDuration(300)
        self.anim_out.setStartValue(1.0)
        self.anim_out.setEndValue(0.0)
        self.anim_out.finished.connect(self.close)
        self.anim_out.start()

    @staticmethod
    def show_toast(parent_window, message: str, toast_type: str = "success"):
        if not parent_window:
            return
        toast = ToastNotification(message, toast_type, parent=parent_window)
        # Position in top-right or bottom-right of parent window
        parent_rect = parent_window.rect()
        toast.adjustSize()
        x = parent_rect.width() - toast.width() - 25
        y = parent_rect.height() - toast.height() - 35
        toast.move(x, y)
        toast.show()
