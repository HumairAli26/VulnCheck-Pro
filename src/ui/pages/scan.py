"""
SecureAudit
Scan Page

Author: Humair Ali
"""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from src.audits.registry import build_full_scan, build_quick_scan
from src.config.colors import colors
from src.config.fonts import fonts
from src.core.audit_engine import ScanSummary
from src.core.scan_worker import ScanWorker
from src.services.database.db_manager import database_manager
from src.ui.pages.base_page import BasePage
from src.ui.widgets.action_button import ActionButton
from src.ui.widgets.finding_card import FindingCard
from src.ui.widgets.section_header import SectionHeader


class ScanPage(BasePage):
    """Lets the user trigger a Quick or Full scan and watch results stream in."""

    scan_completed = Signal(object)  # emits ScanSummary

    def __init__(self):
        super().__init__()
        self._worker: ScanWorker | None = None
        self.setup_ui()

    def setup_ui(self):
        self.main_layout.addWidget(
            SectionHeader("Scan", "Run an on-demand security posture assessment")
        )

        buttons = QHBoxLayout()
        buttons.setSpacing(15)
        self.quick_btn = ActionButton("Quick Scan")
        self.quick_btn.clicked.connect(lambda: self._start_scan("quick"))
        self.full_btn = ActionButton("Full Scan")
        self.full_btn.clicked.connect(lambda: self._start_scan("full"))
        buttons.addWidget(self.quick_btn)
        buttons.addWidget(self.full_btn)
        buttons.addStretch()
        self.main_layout.addLayout(buttons)

        self.status_label = QLabel("Idle")
        self.status_label.setStyleSheet(
            f'color:{colors.SUBTEXT}; font-family:"{fonts.FAMILY}"; font-size:{fonts.SMALL}pt;'
        )
        self.main_layout.addWidget(self.status_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(8)
        self.progress_bar.setStyleSheet(
            f"""
            QProgressBar {{ background-color: {colors.CARD}; border-radius: 4px; }}
            QProgressBar::chunk {{ background-color: {colors.PRIMARY}; border-radius: 4px; }}
            """
        )
        self.main_layout.addWidget(self.progress_bar)

        self.results_container = QWidget()
        self.results_layout = QVBoxLayout(self.results_container)
        self.results_layout.setSpacing(10)
        self.results_layout.addStretch()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.results_container)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        self.main_layout.addWidget(scroll, 1)

    def _start_scan(self, scan_type: str) -> None:
        if self._worker is not None and self._worker.isRunning():
            return

        self.quick_btn.setEnabled(False)
        self.full_btn.setEnabled(False)
        self._clear_results()
        self.progress_bar.setValue(0)
        self.status_label.setText(f"Running {scan_type} scan...")

        audits = build_quick_scan() if scan_type == "quick" else build_full_scan()
        self._worker = ScanWorker(audits)
        self._worker.progress.connect(self._on_progress)
        self._worker.finished_scan.connect(lambda s: self._on_finished(s, scan_type))
        self._worker.start()

    def _on_progress(self, done: int, total: int, name: str) -> None:
        if total == 0:
            # Sub-task update (e.g. mid-port-scan) -- text only, bar stays put.
            self.status_label.setText(name)
            return
        percent = int((done / total) * 100)
        self.progress_bar.setValue(percent)
        self.status_label.setText(f"[{done}/{total}] {name}")

    def _on_finished(self, summary: ScanSummary, scan_type: str) -> None:
        self.quick_btn.setEnabled(True)
        self.full_btn.setEnabled(True)
        self.status_label.setText(
            f"Scan complete · Security score {summary.security_score}/100 "
            f"· {summary.duration_seconds}s"
        )

        for result in summary.results:
            self.results_layout.insertWidget(
                self.results_layout.count() - 1, FindingCard(result)
            )

        database_manager.save_scan(summary, scan_type=scan_type)
        self.scan_completed.emit(summary)

    def _clear_results(self) -> None:
        while self.results_layout.count() > 1:
            item = self.results_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
