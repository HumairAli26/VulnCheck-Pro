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

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFrame, QVBoxLayout
from src.config.colors import colors
from src.ui.navigation.nav_button import NavigationButton

class Sidebar(QFrame):
    """
    Left navigation sidebar.
    """
    page_changed = Signal(int)
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

        for index, (page_name, icon) in enumerate(NAV_ITEMS):
            button = NavigationButton(f"{icon}  {page_name}")
            button.clicked.connect(
                lambda checked=False, i=index: self.change_page(i)
            )
            layout.addWidget(button)
            self.buttons[index] = button
        layout.addStretch()

        self.setLayout(layout)

    def change_page(self, index: int):
        """
        Emit the selected page index and
        highlight the active button.
        """
        for button in self.buttons.values():
            button.setChecked(False)
        self.buttons[index].setChecked(True)
        self.page_changed.emit(index)