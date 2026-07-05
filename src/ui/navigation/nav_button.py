"""
Navigation Button Widget
"""

from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QPushButton
from src.config.colors import colors
from src.config.fonts import fonts


class NavigationButton(QPushButton):
    def __init__(self, text: str):
        super().__init__(text)
        self.setup_ui()

    def setup_ui(self):
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setMinimumHeight(48)
        self.setCheckable(True)
        self.setStyleSheet(
            f"""
            QPushButton {{
                background-color: transparent;
                color: {colors.TEXT};
                border: none;
                border-radius: 8px;
                padding-left: 18px;
                text-align: left;
                font-family: "{fonts.FAMILY}";
                font-size: {fonts.BODY}pt;
            }}

            QPushButton:hover {{
                background-color: {colors.CARD};
            }}

            QPushButton:checked {{
                background-color: {colors.PRIMARY};
                color: white;
            }}
            """
        )
        