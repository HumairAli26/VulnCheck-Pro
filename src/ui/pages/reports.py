"""
SecureAudit
Reports Page

Author: Humair Ali
"""

from __future__ import annotations

from PySide6.QtWidgets import QHBoxLayout, QLabel, QListWidget, QListWidgetItem

from src.config.colors import colors
from src.config.fonts import fonts
from src.core.audit_engine import ScanSummary
from src.services.database.db_manager import database_manager
from src.services.report.report_service import generate_report
from src.ui.pages.base_page import BasePage
from src.ui.widgets.action_button import ActionButton
from src.ui.widgets.section_header import SectionHeader


class ReportsPage(BasePage):
    """Generates PDF / JSON / CSV reports from any previously-run scan."""

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.main_layout.addWidget(
            SectionHeader("Reports", "Export a professional report from any past scan")
        )

        self.scan_list = QListWidget()
        self.scan_list.setStyleSheet(
            f"""
            QListWidget {{
                background-color: {colors.CARD};
                border-radius: 10px;
                color: {colors.TEXT};
                padding: 8px;
            }}
            QListWidget::item {{ padding: 8px; }}
            QListWidget::item:selected {{ background-color: {colors.PRIMARY}; border-radius: 6px; }}
            """
        )
        self.main_layout.addWidget(self.scan_list, 1)

        buttons = QHBoxLayout()
        buttons.setSpacing(15)
        for fmt in ("pdf", "json", "csv"):
            btn = ActionButton(f"Export {fmt.upper()}")
            btn.clicked.connect(lambda checked=False, f=fmt: self._export(f))
            buttons.addWidget(btn)
        buttons.addStretch()
        self.main_layout.addLayout(buttons)

        self.status_label = QLabel("")
        self.status_label.setStyleSheet(
            f'color:{colors.SUCCESS}; font-family:"{fonts.FAMILY}"; font-size:{fonts.SMALL}pt;'
        )
        self.main_layout.addWidget(self.status_label)

        self.refresh()

    def refresh(self) -> None:
        self.scan_list.clear()
        for scan in database_manager.list_scans(limit=50):
            item = QListWidgetItem(
                f"Scan #{scan.id}  ·  {scan.finished_at}  ·  Score {scan.security_score}/100  "
                f"·  {scan.scan_type}"
            )
            item.setData(1, scan.id)
            self.scan_list.addItem(item)

    def _export(self, fmt: str) -> None:
        item = self.scan_list.currentItem()
        if item is None:
            self.status_label.setStyleSheet(
                f'color:{colors.DANGER}; font-family:"{fonts.FAMILY}"; font-size:{fonts.SMALL}pt;'
            )
            self.status_label.setText("Select a scan from the list first.")
            return

        scan_id = item.data(1)
        record = database_manager.get_scan(scan_id)
        if record is None:
            return

        results = [database_manager.finding_to_audit_result(f) for f in record.findings]
        summary = ScanSummary(
            started_at=record.started_at,
            finished_at=record.finished_at,
            duration_seconds=record.duration_seconds,
            results=results,
        )
        path = generate_report(summary, fmt)
        self.status_label.setStyleSheet(
            f'color:{colors.SUCCESS}; font-family:"{fonts.FAMILY}"; font-size:{fonts.SMALL}pt;'
        )
        self.status_label.setText(f"Saved to {path}")
