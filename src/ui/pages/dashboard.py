"""
Dashboard Page
"""

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from src.config.fonts import fonts
from src.ui.pages.base_page import BasePage
from src.ui.widgets.info_card import InfoCard
from src.ui.widgets.section_header import SectionHeader
from src.ui.widgets.action_button import ActionButton
from src.config.colors import Colors

from PySide6.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
)

class DashboardPage(BasePage):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.main_layout.addWidget(
            SectionHeader(
                "Dashboard",
                "Monitor your system security posture"
            )
        )

        grid = QGridLayout()
        grid.setSpacing(20)
        grid.addWidget(
            InfoCard("System Health", "Healthy"),
            0,
            0,
        )
        grid.addWidget(
            InfoCard(
                "Firewall",
                "Enabled",
                Colors.SUCCESS,
            ),
            0,
            1,
        )
        grid.addWidget(
            InfoCard(
                "Updates",
                "2 Pending",
                Colors.WARNING,
            ),
            0,
            2,
        )
        grid.addWidget(
            InfoCard(
                "Risk Score",
                "12",
                Colors.DANGER,
            ),
            0,
            3,
        )

        self.main_layout.addLayout(grid)

        buttons = QHBoxLayout()
        buttons.setSpacing(15)
        buttons.addWidget(
            ActionButton("Start Scan")
        )
        buttons.addWidget(
            ActionButton("Generate Report")
        )
        buttons.addWidget(
            ActionButton("View History")
        )
        buttons.addStretch()

        self.main_layout.addLayout(buttons)
        self.main_layout.addStretch()