"""
SecureAudit
Reusable Information Card

Author: Humair Ali
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QFrame,
    QGraphicsDropShadowEffect,
    QLabel,
    QVBoxLayout,
)

from src.config.colors import colors
from src.config.fonts import fonts


class InfoCard(QFrame):
    """Professional dashboard card with a centered, bold heading and outlined border."""

    def __init__(
        self,
        title: str,
        value: str,
        color: str = colors.PRIMARY,
    ):
        super().__init__()
        self.title = title
        self.value = value
        self.color = color
        self.setup_ui()

    def setup_ui(self):
        self.setMinimumSize(250, 160)
        self.setObjectName("InfoCard")
        self.setFrameShape(QFrame.NoFrame)
        
        self.setStyleSheet(
            f"""
            QFrame#InfoCard {{
                background-color: transparent;
                border: 2px solid {colors.CARD}; 
                border-radius: 14px;
            }}
            QFrame#InfoCard:hover {{
                background-color: rgba(255, 255, 255, 5);
                border-color: {colors.PRIMARY};
            }}
            """
        )

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(24)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 90))
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 22, 20, 22)
        layout.setSpacing(14)

        self.title_label = QLabel(self.title)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet(
            f"color:{colors.SUBTEXT}; font-size:{fonts.HEADING + 1}pt; font-weight:700; background-color: transparent;"
        )

        # --- NEW: Added horizontal line separator ---
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet(f"background-color: {colors.CARD}; border: none; height: 1px;")
        
        self.value_label = QLabel(self.value)
        self.value_label.setAlignment(Qt.AlignCenter)
        self.value_label.setWordWrap(True)
        self.value_label.setStyleSheet(
            f"color:{self.color}; font-size:{fonts.TITLE + 6}pt; font-weight:800; background-color: transparent;"
        )

        layout.addWidget(self.title_label)
        layout.addWidget(line)  # Insert the separator
        layout.addStretch()
        layout.addWidget(self.value_label)
        layout.addStretch()
        self.setLayout(layout)

    def set_value(self, value: str, color: str | None = None) -> None:
        """Update the displayed value (and optionally its accent color)."""
        self.value = value
        self.value_label.setText(value)
        if color:
            self.color = color
            self.value_label.setStyleSheet(
                f"color:{color}; font-size:{fonts.TITLE + 6}pt; font-weight:800; background-color: transparent;"
            )