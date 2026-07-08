"""
SecureAudit
Progress Ring Widget

Author: Humair Ali
"""

from __future__ import annotations

from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QColor, QFont, QPainter, QPen
from PySide6.QtWidgets import QWidget

from src.config.colors import colors
from src.config.fonts import fonts


class ProgressRing(QWidget):
    """
    A circular gauge (0-100) used for the security/compliance score.
    Implemented with QPainter rather than QtCharts to avoid an extra
    dependency for what is fundamentally a single arc.
    """

    def __init__(self, value: int = 0, label: str = "Security Score", parent=None):
        super().__init__(parent)
        self._value = max(0, min(100, value))
        self._label = label
        self.setMinimumSize(180, 180)

    def set_value(self, value: int) -> None:
        self._value = max(0, min(100, value))
        self.update()

    def _color_for_value(self) -> QColor:
        if self._value >= 80:
            return QColor(colors.SUCCESS)
        if self._value >= 50:
            return QColor(colors.WARNING)
        return QColor(colors.DANGER)

    def paintEvent(self, event) -> None:  # noqa: N802 - Qt override
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        side = min(self.width(), self.height()) - 20
        rect = QRectF(
            (self.width() - side) / 2, (self.height() - side) / 2, side, side
        )

        track_pen = QPen(QColor(colors.CARD), 14, Qt.SolidLine, Qt.RoundCap)
        painter.setPen(track_pen)
        painter.drawArc(rect, 0, 360 * 16)

        value_pen = QPen(self._color_for_value(), 14, Qt.SolidLine, Qt.RoundCap)
        painter.setPen(value_pen)
        span = int(360 * 16 * (self._value / 100))
        painter.drawArc(rect, 90 * 16, -span)

        painter.setPen(QColor(colors.TEXT))
        painter.setFont(QFont(fonts.FAMILY, fonts.TITLE, QFont.Bold))
        painter.drawText(rect, Qt.AlignCenter, str(self._value))

        label_rect = QRectF(rect.x(), rect.bottom() + 15, rect.width(), 30)
        painter.setPen(QColor(colors.SUBTEXT))
        painter.setFont(QFont(fonts.FAMILY, fonts.SMALL))
        painter.drawText(label_rect, Qt.AlignCenter, self._label)
