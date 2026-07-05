"""
Application Sidebar
"""

from PySide6.QtWidgets import QFrame, QVBoxLayout
from src.config.colors import colors
from src.ui.navigation.nav_button import NavigationButton

class Sidebar(QFrame):
    """
    Left navigation sidebar.
    """
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setFixedWidth(230)
        self.setStyleSheet(
            f"""
            QFrame {{
                background-color: {colors.SIDEBAR};
            }}
            """
        )

        layout = QVBoxLayout()
        layout.setContentsMargins(15, 20, 15, 20)
        layout.setSpacing(10)
        self.dashboard_button = NavigationButton("🏠 Dashboard")
        self.scan_button = NavigationButton("🔍 Full Scan")
        self.report_button = NavigationButton("📄 Reports")
        self.history_button = NavigationButton("🕒 History")
        self.settings_button = NavigationButton("⚙ Settings")
        self.about_button = NavigationButton(" ℹ  About")
        layout.addWidget(self.dashboard_button)
        layout.addWidget(self.scan_button)
        layout.addWidget(self.report_button)
        layout.addWidget(self.history_button)
        layout.addWidget(self.settings_button)
        layout.addWidget(self.about_button)
        layout.addStretch()
        self.setLayout(layout)