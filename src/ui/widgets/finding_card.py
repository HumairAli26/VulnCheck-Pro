"""
SecureAudit
Finding Card Widget

Author: Humair Ali
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout

from src.config.colors import Colors, colors
from src.config.fonts import fonts
from src.models.audit_result import AuditResult, Severity
from src.ui.dialogs.remediation_dialog import RemediationDialog
from src.ui.widgets.risk_badge import RiskBadge


class FindingCard(QFrame):
    """One row summarizing a single audit finding, used in Scan/Reports/History."""

    def __init__(self, result: AuditResult):
        super().__init__()
        self._result = result
        self.setObjectName("FindingCard")
        accent = Colors.for_severity(result.severity.value)
        
        # CHANGED: background-color set to transparent, added border
        self.setStyleSheet(
            f"""
            QFrame#FindingCard {{
                background-color: transparent;
                border: 2px solid {colors.CARD};
                border-left: 4px solid {accent};
                border-radius: 8px;
            }}
            """
        )

        outer = QHBoxLayout(self)
        outer.setContentsMargins(16, 12, 16, 12)
        outer.setSpacing(14)

        text_col = QVBoxLayout()
        text_col.setSpacing(4)

        # CHANGED: Added background-color: transparent to labels
        title = QLabel(f"{result.title}  ·  {result.category}")
        title.setStyleSheet(
            f'color:{colors.TEXT}; font-family:"{fonts.FAMILY}"; '
            f"font-size:{fonts.BODY}pt; font-weight:600; background-color: transparent;"
        )

        description = QLabel(result.description)
        description.setWordWrap(True)
        description.setStyleSheet(
            f'color:{colors.SUBTEXT}; font-family:"{fonts.FAMILY}"; font-size:{fonts.SMALL}pt; background-color: transparent;'
        )

        recommendation = QLabel(f"Recommendation: {result.recommendation}")
        recommendation.setWordWrap(True)
        recommendation.setStyleSheet(
            f'color:{colors.INFO}; font-family:"{fonts.FAMILY}"; font-size:{fonts.SMALL}pt; background-color: transparent;'
        )

        text_col.addWidget(title)
        text_col.addWidget(description)
        text_col.addWidget(recommendation)

        outer.addLayout(text_col, 1)

        side_col = QVBoxLayout()
        side_col.setSpacing(8)
        side_col.addWidget(RiskBadge(result.severity.value))

        if result.severity != Severity.INFO:
            fix_btn = QPushButton("View Fix Steps")
            fix_btn.setCursor(QCursor(Qt.PointingHandCursor))
            fix_btn.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: transparent;
                    color: {accent};
                    border: 1px solid {accent};
                    border-radius: 6px;
                    padding: 4px 10px;
                    font-size: {fonts.SMALL}pt;
                    font-weight: 600;
                }}
                QPushButton:hover {{
                    background-color: {accent}44;
                }}
                """
            )
            fix_btn.clicked.connect(self._show_remediation)
            side_col.addWidget(fix_btn)

        outer.addLayout(side_col, 0)

    def _show_remediation(self) -> None:
        dialog = RemediationDialog(self._result, parent=self.window())
        dialog.exec()