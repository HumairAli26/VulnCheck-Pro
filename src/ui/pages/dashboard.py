"""
SecureAudit
Dashboard Page

Author: Humair Ali
"""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QGridLayout, QHBoxLayout, QLabel, QVBoxLayout

from src.config.colors import Colors, colors
from src.config.fonts import fonts
from src.core.audit_engine import ScanSummary
from src.models.audit_result import AuditStatus, Severity
from src.services.database.db_manager import database_manager
from src.ui.pages.base_page import BasePage
from src.ui.widgets.action_button import ActionButton
from src.ui.widgets.info_card import InfoCard
from src.ui.widgets.progress_ring import ProgressRing
from src.ui.widgets.section_header import SectionHeader

class DashboardPage(BasePage):
    """Landing page: overall score plus a card per audited category."""

    request_scan = Signal()
    request_reports = Signal()
    request_history = Signal()

    def __init__(self):
        super().__init__()
        self._cards: dict[str, InfoCard] = {}
        self.setup_ui()
        self.refresh_from_database()

    def setup_ui(self):
        self.main_layout.addWidget(
            SectionHeader("Dashboard", "Monitor your system's security posture")
        )

        top_row = QHBoxLayout()
        top_row.setSpacing(20)

        self.ring = ProgressRing(0, "Security Score")
        top_row.addWidget(self.ring, 0)

        grid = QGridLayout()
        grid.setSpacing(20)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        
        # Initialize all cards
        self._cards["System Health"] = InfoCard("System Health", "No scans yet", colors.SUBTEXT)
        self._cards["Network"] = InfoCard("Firewall & Ports", "Not scanned", colors.SUBTEXT)
        self._cards["Data Protection"] = InfoCard("Disk Encryption", "Not scanned", colors.SUBTEXT)
        self._cards["Patch Management"] = InfoCard("Updates", "Not scanned", colors.SUBTEXT)
        self._cards["Screen Lock"] = InfoCard("Screen Lock", "Not scanned", colors.SUBTEXT)
        self._cards["Running Processes"] = InfoCard("Running Processes", "Not scanned", colors.SUBTEXT)

        # Added positions for all 6 cards (3 rows, 2 columns)
        positions = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)]
        for (title, card), pos in zip(self._cards.items(), positions):
            grid.addWidget(card, *pos)

        top_row.addLayout(grid, 1)
        self.main_layout.addLayout(top_row)

        self.summary_label = QLabel("Run a scan to see results here.")
        self.summary_label.setStyleSheet(
            f'color:{colors.SUBTEXT}; font-family:"{fonts.FAMILY}"; font-size:{fonts.BODY}pt;'
        )
        self.main_layout.addWidget(self.summary_label)

        buttons = QHBoxLayout()
        buttons.setSpacing(15)
        start_scan_btn = ActionButton("Start Scan")
        start_scan_btn.clicked.connect(self.request_scan.emit)
        reports_btn = ActionButton("Generate Report")
        reports_btn.clicked.connect(self.request_reports.emit)
        history_btn = ActionButton("View History")
        history_btn.clicked.connect(self.request_history.emit)

        buttons.addWidget(start_scan_btn)
        buttons.addWidget(reports_btn)
        buttons.addWidget(history_btn)
        buttons.addStretch()

        self.main_layout.addLayout(buttons)
        self.main_layout.addStretch()

    def refresh_from_database(self) -> None:
        latest = database_manager.get_latest_scan()
        if latest is None:
            return
        results = [database_manager.finding_to_audit_result(f) for f in latest.findings]
        summary = ScanSummary(
            started_at=latest.started_at,
            finished_at=latest.finished_at,
            duration_seconds=latest.duration_seconds,
            results=results,
        )
        self.refresh(summary)

    def refresh(self, summary: ScanSummary) -> None:
        self.ring.set_value(summary.security_score)

        by_category = {}
        for result in summary.results:
            by_category.setdefault(result.category, []).append(result)

        worst_overall = self._worst_severity(summary.results)
        self._cards["System Health"].set_value(
            "Healthy" if worst_overall in (Severity.INFO, Severity.LOW) else "Needs Attention",
            Colors.for_severity(worst_overall.value) if worst_overall else colors.SUCCESS,
        )

        # Updated to include all categories
        self._update_category_card("Network", by_category.get("Network", []), "Firewall & Ports")
        self._update_category_card("Data Protection", by_category.get("Data Protection", []), "Disk Encryption")
        self._update_category_card("Patch Management", by_category.get("Patch Management", []), "Updates")
        self._update_category_card("Screen Lock", by_category.get("Screen Lock", []), "Screen Lock")
        self._update_category_card("Running Processes", by_category.get("Running Processes", []), "Processes")

        self.summary_label.setText(
            f"Last scan: {summary.finished_at}  ·  {len(summary.results)} check(s)  ·  "
            f"{summary.failed_count} failed to complete"
        )

    def _update_category_card(self, key: str, results: list, title: str) -> None:
        card = self._cards[key]
        if not results:
            card.set_value("Not scanned", colors.SUBTEXT)
            return
        worst = self._worst_severity(results)
        label = "Passed" if worst in (Severity.INFO, Severity.LOW) else worst.value
        card.title_label.setText(title)
        card.set_value(label, Colors.for_severity(worst.value))

    @staticmethod
    def _worst_severity(results: list) -> Severity:
        if not results:
            return Severity.INFO
        order = [Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM, Severity.LOW, Severity.INFO]
        for level in order:
            if any(r.severity == level for r in results):
                return level
        return Severity.INFO