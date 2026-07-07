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

from PySide6.QtGui import QColor
from PySide6.QtWidgets import QGraphicsDropShadowEffect

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
        self.setMinimumSize(250, 160)
        self.setObjectName("InfoCard")
        self.setFrameShape(QFrame.NoFrame)
        
        # Applying stylesheet to the Frame and all descendant QLabels
        self.setStyleSheet(
            f"""
            QFrame#InfoCard {{
                background-color: {colors.CARD};
                border: none;
                border-radius: 14px;
            }}
            QFrame#InfoCard:hover {{
                background-color: {colors.CARD_HOVER};
            }}
            QFrame#InfoCard QLabel {{
                background-color: transparent;
            }}
            """
        )

        # Subtle depth effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(24)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 90))
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 22, 20, 22)
        layout.setSpacing(14)

        self.title_label = QLabel(self.title)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet(
            f"""
            color:{colors.SUBTEXT};
            font-size:{fonts.BODY + 1}pt;
            font-weight:700;
            letter-spacing: 0.5px;
            """
        )

        self.value_label = QLabel(self.value)
        self.value_label.setAlignment(Qt.AlignCenter)
        self.value_label.setStyleSheet(
            f"""
            color:{self.color};
            font-size:{fonts.TITLE + 6}pt;
            font-weight:800;
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
            # We only update the dynamic color property here
            self.value_label.setStyleSheet(
                f"color:{color}; font-size:{fonts.TITLE + 6}pt; font-weight:800;"
            )