"""
History Page
"""
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QLabel
from src.config.fonts import fonts
from src.ui.pages.base_page import BasePage

class HistoryPage(BasePage):

    def __init__(self):
        super().__init__()
        title = QLabel("History")
        title.setFont(
            QFont(
                fonts.FAMILY,
                fonts.TITLE,
                QFont.Bold,
            )
        )
        title.setAlignment(Qt.AlignCenter)

        self.main_layout.addStretch()
        self.main_layout.addWidget(title)
        self.main_layout.addStretch()