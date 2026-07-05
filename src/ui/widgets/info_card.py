"""
SecureAudit
Reusable Information Card

Author: Humair Ali
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
)

from src.config.colors import colors
from src.config.fonts import fonts


class InfoCard(QFrame):
    """
    Professional dashboard card.
    """
    def __init__(
        self,
        title: str,
        value: str,
        color: str = colors.PRIMARY,
    ):
        super().__init__()
        self.title = title
        self.value = value
        self.color = color
        self.setup_ui()

    def setup_ui(self):
        self.setMinimumSize(250, 150)
        self.setObjectName("InfoCard")
        self.setStyleSheet(
            f"""
            QFrame#InfoCard {{

                background-color: {colors.CARD};

                border-radius: 12px;

            }}
            """
        )

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        title_label = QLabel(self.title)
        title_label.setStyleSheet(
            f"""
            color:{colors.SUBTEXT};
            font-size:{fonts.BODY}pt;
            """
        )

        value_label = QLabel(self.value)
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setStyleSheet(
            f"""
            color:{self.color};
            font-size:{fonts.TITLE}pt;
            font-weight:bold;
            """
        )

        layout.addWidget(title_label)
        layout.addStretch()
        layout.addWidget(value_label)
        layout.addStretch()
        self.setLayout(layout)