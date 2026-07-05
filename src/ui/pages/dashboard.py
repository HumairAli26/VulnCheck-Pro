"""
Dashboard Page
"""

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget
from src.config.fonts import fonts
from src.ui.pages.base_page import BasePage
from PySide6.QtWidgets import QGridLayout
from src.ui.widgets.info_card import InfoCard

class DashboardPage(BasePage):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        grid = QGridLayout()
        grid.setSpacing(20)
        grid.addWidget(
            InfoCard(
                "System Health",
                "Healthy",
            ),
            0,
            0,
        )
        grid.addWidget(
            InfoCard(
                "Firewall",
                "Enabled",
                "#22C55E",
            ),
            0,
            1,
        )
        grid.addWidget(
            InfoCard(
                "Risk Score",
                "0",
                "#2563EB",
            ),
            0,
            2,
        )

        self.main_layout.addLayout(grid)
        self.main_layout.addStretch()