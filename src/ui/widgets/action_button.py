"""
Dashboard Action Button
"""
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QPushButton

from src.config.colors import colors
from src.config.fonts import fonts

class ActionButton(QPushButton):

    def __init__(self, text: str):
        super().__init__(text)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setMinimumHeight(42)
        self.setStyleSheet(
            f"""
            QPushButton {{
                background:{colors.PRIMARY};
                color:white;
                border:none;
                border-radius:8px;
                font-family:"{fonts.FAMILY}";
                font-size:{fonts.BODY}pt;
                font-weight:bold;
            }}

            QPushButton:hover {{
                background:#1D4ED8;
            }}
            """
        )