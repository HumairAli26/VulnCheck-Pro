"""
SecureAudit
Main Application Window

Author: Humair Ali
"""

from PySide6.QtWidgets import (
    QMainWindow,
    QStatusBar,
    QWidget,
    QHBoxLayout
)
from src.ui.pages.dashboard import DashboardPage
from src.ui.navigation.sidebar import Sidebar
from src.config.settings import settings


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
        self.dashboard = DashboardPage()

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.dashboard, 1)

    def create_status_bar(self):
        status_bar = QStatusBar()
        status_bar.showMessage("Ready")
        self.setStatusBar(status_bar)