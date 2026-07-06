"""
SecureAudit
About Page

Author: Humair Ali
"""

from __future__ import annotations

from PySide6.QtWidgets import QLabel

from src.config.colors import colors
from src.config.fonts import fonts
from src.config.settings import settings
from src.ui.pages.base_page import BasePage
from src.ui.widgets.section_header import SectionHeader

_DESCRIPTION = (
    "SecureAudit performs local, defensive security posture assessments: it checks "
    "your firewall, disk encryption, patch status, and exposed network ports, scores "
    "the results, and produces PDF, JSON, and CSV reports you can share or archive."
)


class AboutPage(BasePage):
    def __init__(self):
        super().__init__()
        self.main_layout.addWidget(SectionHeader("About", f"{settings.APP_NAME} v{settings.VERSION}"))

        description = QLabel(_DESCRIPTION)
        description.setWordWrap(True)
        description.setStyleSheet(
            f'color:{colors.TEXT}; font-family:"{fonts.FAMILY}"; font-size:{fonts.BODY}pt;'
        )
        self.main_layout.addWidget(description)

        details = QLabel(
            f"Author: {settings.COMPANY}\n"
            "Stack: Python, PySide6, SQLAlchemy, ReportLab\n"
            "License: MIT"
        )
        details.setStyleSheet(
            f'color:{colors.SUBTEXT}; font-family:"{fonts.FAMILY}"; font-size:{fonts.SMALL}pt;'
        )
        self.main_layout.addWidget(details)
        self.main_layout.addStretch()
