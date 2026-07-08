"""
SecureAudit
Main Application Window

Author: Humair Ali
"""

from __future__ import annotations

from PySide6.QtWidgets import QHBoxLayout, QMainWindow, QStackedWidget, QStatusBar, QWidget

from src.config.settings import settings
from src.ui.navigation.sidebar import Sidebar
from src.ui.pages.about import AboutPage
from src.ui.pages.dashboard import DashboardPage
from src.ui.pages.history import HistoryPage
from src.ui.pages.processes import ProcessesPage
from src.ui.pages.reports import ReportsPage
from src.ui.pages.scan import ScanPage
from src.ui.pages.settings import SettingsPage

_PAGE_DASHBOARD, _PAGE_SCAN, _PAGE_PROCESSES, _PAGE_REPORTS, _PAGE_HISTORY, _PAGE_SETTINGS, _PAGE_ABOUT = range(7)


class MainWindow(QMainWindow):
    """
    Main application window. Every page in SecureAudit lives inside this
    window, and this class is responsible for wiring the small number of
    cross-page events (a completed scan should refresh the Dashboard and
    History pages; dashboard buttons should navigate the sidebar).
    """

    def __init__(self):
        super().__init__()
        self.setup_window()
        self.create_status_bar()

    def setup_window(self):
        self.setWindowTitle(f"{settings.APP_NAME} — Security Posture Auditor")
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
        self.processes_page = ProcessesPage()
        self.reports_page = ReportsPage()
        self.history_page = HistoryPage()
        self.settings_page = SettingsPage()
        self.about_page = AboutPage()

        self.page_stack = QStackedWidget()
        for page in (
            self.dashboard_page,
            self.scan_page,
            self.processes_page,
            self.reports_page,
            self.history_page,
            self.settings_page,
            self.about_page,
        ):
            self.page_stack.addWidget(page)

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.page_stack, 1)

        self.sidebar.page_changed.connect(self.page_stack.setCurrentIndex)
        self.sidebar.change_page(_PAGE_DASHBOARD)

        self._wire_cross_page_events()

    def _wire_cross_page_events(self) -> None:
        # Dashboard action buttons act as shortcuts into the sidebar.
        self.dashboard_page.request_scan.connect(
            lambda: self.sidebar.change_page(_PAGE_SCAN)
        )
        self.dashboard_page.request_reports.connect(
            lambda: self.sidebar.change_page(_PAGE_REPORTS)
        )
        self.dashboard_page.request_history.connect(
            lambda: self.sidebar.change_page(_PAGE_HISTORY)
        )

        # A completed scan should be reflected everywhere without re-opening the app.
        self.scan_page.scan_completed.connect(self.dashboard_page.refresh)
        self.scan_page.scan_completed.connect(lambda _: self.reports_page.refresh())
        self.scan_page.scan_completed.connect(lambda _: self.history_page.refresh())

    def create_status_bar(self):
        status_bar = QStatusBar()
        status_bar.showMessage("Ready")
        self.setStatusBar(status_bar)
