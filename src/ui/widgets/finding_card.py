"""
SecureAudit
Finding Card Widget

Author: Humair Ali
"""

from __future__ import annotations

from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout

from src.config.colors import Colors, colors
from src.config.fonts import fonts
from src.models.audit_result import AuditResult
from src.ui.widgets.risk_badge import RiskBadge


class FindingCard(QFrame):
    """One row summarizing a single audit finding, used in Scan/Reports/History."""

    def __init__(self, result: AuditResult):
        super().__init__()
        self._result = result
        self.setObjectName("FindingCard")
        accent = Colors.for_severity(result.severity.value)
        self.setStyleSheet(
            f"""
            QFrame#FindingCard {{
                background-color: {colors.CARD};
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

        title = QLabel(f"{result.title}  ·  {result.category}")
        title.setStyleSheet(
            f'color:{colors.TEXT}; font-family:"{fonts.FAMILY}"; '
            f"font-size:{fonts.BODY}pt; font-weight:600;"
        )

        description = QLabel(result.description)
        description.setWordWrap(True)
        description.setStyleSheet(
            f'color:{colors.SUBTEXT}; font-family:"{fonts.FAMILY}"; font-size:{fonts.SMALL}pt;'
        )

        recommendation = QLabel(f"Recommendation: {result.recommendation}")
        recommendation.setWordWrap(True)
        recommendation.setStyleSheet(
            f'color:{colors.INFO}; font-family:"{fonts.FAMILY}"; font-size:{fonts.SMALL}pt;'
        )

        text_col.addWidget(title)
        text_col.addWidget(description)
        text_col.addWidget(recommendation)

        outer.addLayout(text_col, 1)
        
        # Initialize and configure the badge
        badge = RiskBadge(result.severity.value)
        
        # Enforce a fixed width to ensure uniform alignment for all badges
        # Adjust '120' if your labels are wider/narrower than expected
        badge.setFixedWidth(120) 
        
        outer.addWidget(badge, 0)