"""
SecureAudit
Main Application Window

Author: Humair Ali
"""

from PySide6.QtWidgets import (
    QMainWindow,
    QStatusBar,
    QWidget,
    QHBoxLayout,
    QStackedWidget
)
from src.ui.navigation.sidebar import Sidebar
from src.config.settings import settings

from src.ui.pages.dashboard import DashboardPage
from src.ui.pages.scan import ScanPage
from src.ui.pages.reports import ReportsPage
from src.ui.pages.history import HistoryPage
from src.ui.pages.settings import SettingsPage
from src.ui.pages.about import AboutPage


class MainWindow(QMainWindow):
    """
    Main application window.
    Every page in SecureAudit will live inside this window.
    """

    def __init__(self):
        super().__init__()

        self.setup_window()
        self.create_status_bar()

    def setup_window(self):
        self.setWindowTitle(settings.APP_NAME)
        self.resize(settings.WIDTH, settings.HEIGHT)
        self.setMinimumSize(settings.MIN_WIDTH, settings.MIN_HEIGHT)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.central_widget.setLayout(main_layout)
        self.sidebar = Sidebar()

        self.dashboard_page = DashboardPage()
        self.scan_page = ScanPage()
        self.reports_page = ReportsPage()
        self.history_page = HistoryPage()
        self.settings_page = SettingsPage()
        self.about_page = AboutPage()

        self.page_stack = QStackedWidget()

        self.page_stack.addWidget(self.dashboard_page)
        self.page_stack.addWidget(self.scan_page)
        self.page_stack.addWidget(self.reports_page)
        self.page_stack.addWidget(self.history_page)
        self.page_stack.addWidget(self.settings_page)
        self.page_stack.addWidget(self.about_page)

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.page_stack, 1)

    def create_status_bar(self):
        status_bar = QStatusBar()
        status_bar.showMessage("Ready")
        self.setStatusBar(status_bar)