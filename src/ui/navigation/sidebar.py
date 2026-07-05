"""
Application Sidebar
"""

NAV_ITEMS = [
    ("Dashboard", "🏠"),
    ("Full Scan", "🔍"),
    ("Reports", "📄"),
    ("History", "🕒"),
    ("Settings", "⚙"),
    (" About", "  ℹ"),
]

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
        self.buttons = {}

        for page_name, icon in NAV_ITEMS:
            button = NavigationButton(
                f"{icon}  {page_name}"
            )
            layout.addWidget(button)
            self.buttons[page_name] = button
        layout.addStretch()

        self.setLayout(layout)