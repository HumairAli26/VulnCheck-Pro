"""
SecureAudit
History Page

Author: Humair Ali
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QHeaderView,
    QScrollArea,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from src.config.colors import colors
from src.services.database.db_manager import database_manager
from src.ui.pages.base_page import BasePage
from src.ui.widgets.finding_card import FindingCard
from src.ui.widgets.section_header import SectionHeader


class HistoryPage(BasePage):
    """Table of past scans; selecting a row shows its findings below."""

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.main_layout.addWidget(
            SectionHeader("History", "Review previous scans and their findings")
        )

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Scan ID", "Finished At", "Type", "Score"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setStyleSheet(
            f"""
            QTableWidget {{
                background-color: {colors.CARD};
                color: {colors.TEXT};
                border-radius: 10px;
                gridline-color: {colors.BORDER};
            }}
            QHeaderView::section {{
                background-color: {colors.SIDEBAR};
                color: {colors.SUBTEXT};
                border: none;
                padding: 6px;
            }}
            """
        )
        self.table.itemSelectionChanged.connect(self._on_selection_changed)
        self.main_layout.addWidget(self.table)

        self.details_container = QWidget()
        self.details_layout = QVBoxLayout(self.details_container)
        self.details_layout.setSpacing(10)
        self.details_layout.addStretch()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.details_container)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        self.main_layout.addWidget(scroll, 1)

        self.refresh()

    def refresh(self) -> None:
        scans = database_manager.list_scans(limit=100)
        self.table.setRowCount(len(scans))
        for row, scan in enumerate(scans):
            self.table.setItem(row, 0, QTableWidgetItem(str(scan.id)))
            self.table.setItem(row, 1, QTableWidgetItem(scan.finished_at))
            self.table.setItem(row, 2, QTableWidgetItem(scan.scan_type))
            self.table.setItem(row, 3, QTableWidgetItem(f"{scan.security_score}/100"))

    def _on_selection_changed(self) -> None:
        rows = self.table.selectionModel().selectedRows()
        if not rows:
            return
        scan_id = int(self.table.item(rows[0].row(), 0).text())
        record = database_manager.get_scan(scan_id)
        if record is None:
            return

        self._clear_details()
        for finding in record.findings:
            result = database_manager.finding_to_audit_result(finding)
            self.details_layout.insertWidget(
                self.details_layout.count() - 1, FindingCard(result)
            )

    def _clear_details(self) -> None:
        while self.details_layout.count() > 1:
            item = self.details_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
