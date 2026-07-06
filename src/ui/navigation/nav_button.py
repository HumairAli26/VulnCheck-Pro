"""
SecureAudit
Navigation Button Widget

Author: Humair Ali
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QPushButton

from src.config.colors import colors
from src.config.fonts import fonts


class NavigationButton(QPushButton):
    """A sidebar entry. Deliberately icon-free -- text only, professional tone."""

    def __init__(self, text: str):
        super().__init__(text)
        self.setup_ui()

    def setup_ui(self):
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setMinimumHeight(44)
        self.setCheckable(True)
        self.setStyleSheet(
            f"""
            QPushButton {{
                background-color: transparent;
                color: {colors.SUBTEXT};
                border: none;
                border-left: 3px solid transparent;
                border-radius: 0px;
                padding-left: 18px;
                text-align: left;
                font-family: "{fonts.FAMILY}";
                font-size: {fonts.BODY}pt;
            }}

            QPushButton:hover {{
                background-color: {colors.CARD_HOVER};
                color: {colors.TEXT};
            }}

            QPushButton:checked {{
                background-color: {colors.CARD};
                border-left: 3px solid {colors.PRIMARY};
                color: {colors.TEXT};
                font-weight: 600;
            }}
            """
        )
