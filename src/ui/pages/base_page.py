"""
Base Page

Every page inside SecureAudit inherits from this class.
"""
from PySide6.QtWidgets import QVBoxLayout, QWidget

class BasePage(QWidget):
    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(
            30,
            30,
            30,
            30,
        )
        self.main_layout.setSpacing(20)
        self.setLayout(self.main_layout)