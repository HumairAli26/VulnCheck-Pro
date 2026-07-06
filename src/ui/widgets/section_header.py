"""
Section Header Widget
"""
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget
from PySide6.QtGui import QFont

from src.config.colors import colors
from src.config.fonts import fonts

class SectionHeader(QWidget):

    def __init__(self, title: str, subtitle: str):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 20)

        title_label = QLabel(title)
        title_label.setFont(
            QFont(
                fonts.FAMILY,
                fonts.TITLE,
                QFont.Bold,
            )
        )

        subtitle_label = QLabel(subtitle)
        subtitle_label.setStyleSheet(
            f"""
            color:{colors.SUBTEXT};
            font-size:{fonts.BODY}pt;
            """
        )

        layout.addWidget(title_label)
        layout.addWidget(subtitle_label)