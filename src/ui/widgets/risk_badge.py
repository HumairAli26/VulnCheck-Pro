"""
SecureAudit
Risk / Severity Badge Widget

Author: Humair Ali
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel

from src.config.colors import Colors
from src.config.fonts import fonts


class RiskBadge(QLabel):
    """Small rounded pill showing a severity level in its accent color."""

    def __init__(self, severity: str):
        super().__init__(severity)
        self.setAlignment(Qt.AlignCenter)
        color = Colors.for_severity(severity)
        
        # Updated: Removed background-color to make it transparent
        self.setStyleSheet(
            f"""
            QLabel {{
                background-color: transparent;
                color: {color};
                border: 1px solid {color};
                border-radius: 9px;
                padding: 2px 10px;
                font-family: "{fonts.FAMILY}";
                font-size: {fonts.SMALL}pt;
                font-weight: 600;
            }}
            """
        )