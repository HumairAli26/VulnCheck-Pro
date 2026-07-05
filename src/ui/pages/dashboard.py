"""
Dashboard Page
"""

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget
from src.config.fonts import fonts
from src.ui.pages.base_page import BasePage

class DashboardPage(BasePage):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        layout = self.main_layout

        title = QLabel("Dashboard")
        title.setFont(QFont(fonts.FAMILY, fonts.TITLE, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Welcome to SecureAudit")
        subtitle.setAlignment(Qt.AlignCenter)

        self.main_layout.addStretch()
        self.main_layout.addWidget(title)
        self.main_layout.addWidget(subtitle)
        self.main_layout.addStretch()