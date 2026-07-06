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

        self.title_label = QLabel(self.title)
        self.title_label.setStyleSheet(
            f"""
            color:{colors.SUBTEXT};
            font-size:{fonts.BODY}pt;
            """
        )

        self.value_label = QLabel(self.value)
        self.value_label.setAlignment(Qt.AlignCenter)
        self.value_label.setStyleSheet(
            f"""
            color:{self.color};
            font-size:{fonts.TITLE}pt;
            font-weight:bold;
            """
        )

        layout.addWidget(self.title_label)
        layout.addStretch()
        layout.addWidget(self.value_label)
        layout.addStretch()
        self.setLayout(layout)

    def set_value(self, value: str, color: str | None = None) -> None:
        self.value = value
        self.value_label.setText(value)
        if color:
            self.color = color
            self.value_label.setStyleSheet(
                f"color:{color}; font-size:{fonts.TITLE}pt; font-weight:bold;"
            )