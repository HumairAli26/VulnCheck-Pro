"""
SecureAudit
Application Sidebar

Author: Humair Ali
"""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout

from src.config.colors import colors
from src.config.fonts import fonts
from src.config.settings import settings
from src.ui.navigation.nav_button import NavigationButton

NAV_ITEMS = [
    "Dashboard",
    "Scan",
    "Processes",
    "Reports",
    "History",
    "Settings",
    "About",
]


class Sidebar(QFrame):
    """Left navigation sidebar."""

    page_changed = Signal(int)

    def __init__(self):
        super().__init__()
        self.buttons: dict[int, NavigationButton] = {}
        self.setup_ui()

    def setup_ui(self):
        self.setFixedWidth(220)
        self.setStyleSheet(f"QFrame {{ background-color: {colors.SIDEBAR}; }}")

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 20)
        layout.setSpacing(4)

        layout.addWidget(self._build_header())
        layout.addSpacing(10)

        for index, page_name in enumerate(NAV_ITEMS):
            button = NavigationButton(page_name)
            button.clicked.connect(lambda checked=False, i=index: self.change_page(i))
            layout.addWidget(button)
            self.buttons[index] = button

        layout.addStretch()
        self.setLayout(layout)

    def _build_header(self) -> QFrame:
        header = QFrame()
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(20, 24, 20, 20)
        header_layout.setSpacing(2)

        name = QLabel(settings.APP_NAME)
        name.setStyleSheet(
            f'color:{colors.TEXT}; font-family:"{fonts.FAMILY}"; '
            f"font-size:{fonts.HEADING}pt; font-weight:700;"
        )
        subtitle = QLabel("Security Posture Auditor")
        subtitle.setStyleSheet(
            f'color:{colors.SUBTEXT}; font-family:"{fonts.FAMILY}"; font-size:{fonts.SMALL}pt;'
        )
        header_layout.addWidget(name)
        header_layout.addWidget(subtitle)
        return header

    def change_page(self, index: int):
        """Emit the selected page index and highlight the active button."""
        for button in self.buttons.values():
            button.setChecked(False)
        self.buttons[index].setChecked(True)
        self.page_changed.emit(index)
