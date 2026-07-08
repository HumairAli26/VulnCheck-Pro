"""
SecureAudit
Process Explorer Page

Author: Humair Ali

A detailed, sortable view of everything running on the machine right now
-- PID, user, CPU/memory usage, executable path, and full command line --
with rows highlighted when they match the same "deleted executable"
indicator the Running Processes audit checks for. Most simple security
tools stop at "here's a score"; this gives the same kind of drill-down
transparency you'd expect from Task Manager or `ps`, without leaving the app.
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
)

from src.config.colors import colors
from src.config.fonts import fonts
from src.services.network.process_lookup import ProcessInfo, list_processes
from src.ui.pages.base_page import BasePage
from src.ui.widgets.action_button import ActionButton
from src.ui.widgets.section_header import SectionHeader

_COLUMNS = ["PID", "Name", "User", "CPU %", "Memory %", "Status", "Executable Path"]


class ProcessesPage(BasePage):
    """Live, detailed table of every running process on this machine."""

    def __init__(self):
        super().__init__()
        self._all_processes: list[ProcessInfo] = []
        self.setup_ui()
        self.refresh()

    def setup_ui(self):
        self.main_layout.addWidget(
            SectionHeader("Processes", "Inspect every running process in detail")
        )

        controls = QHBoxLayout()
        controls.setSpacing(12)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Filter by name, user, or path...")
        self.search_input.setStyleSheet(
            f"""
            QLineEdit {{
                background-color: {colors.CARD};
                color: {colors.TEXT};
                border: 1px solid {colors.BORDER};
                border-radius: 6px;
                padding: 8px;
            }}
            """
        )
        self.search_input.textChanged.connect(self._apply_filter)
        controls.addWidget(self.search_input, 1)

        refresh_btn = ActionButton("Refresh")
        refresh_btn.clicked.connect(self.refresh)
        controls.addWidget(refresh_btn)

        self.main_layout.addLayout(controls)

        self.summary_label = QLabel("")
        self.summary_label.setStyleSheet(
            f'color:{colors.SUBTEXT}; font-family:"{fonts.FAMILY}"; font-size:{fonts.SMALL}pt;'
        )
        self.main_layout.addWidget(self.summary_label)

        self.table = QTableWidget(0, len(_COLUMNS))
        self.table.setHorizontalHeaderLabels(_COLUMNS)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(6, QHeaderView.Stretch)
        self.table.setSortingEnabled(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
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
        self.main_layout.addWidget(self.table, 1)

    def refresh(self) -> None:
        self._all_processes = sorted(list_processes(), key=lambda p: p.cpu_percent, reverse=True)
        self._render(self._all_processes)

    def _apply_filter(self, text: str) -> None:
        text = text.strip().lower()
        if not text:
            self._render(self._all_processes)
            return
        filtered = [
            p
            for p in self._all_processes
            if text in p.name.lower() or text in p.username.lower() or text in p.exe.lower()
        ]
        self._render(filtered)

    def _render(self, processes: list[ProcessInfo]) -> None:
        self.table.setSortingEnabled(False)
        self.table.setRowCount(len(processes))

        for row, proc in enumerate(processes):
            suspicious = "(deleted)" in proc.exe

            values = [
                str(proc.pid),
                proc.name,
                proc.username,
                f"{proc.cpu_percent:.1f}",
                f"{proc.memory_percent:.2f}",
                proc.status,
                proc.exe or proc.cmdline or "—",
            ]
            for col, value in enumerate(values):
                item = QTableWidgetItem(value)
                if col in (0, 3, 4):
                    item.setData(Qt.DisplayRole, float(value) if col != 0 else int(value))
                if suspicious:
                    item.setForeground(QColor(colors.DANGER))
                self.table.setItem(row, col, item)

        self.table.setSortingEnabled(True)
        flagged = sum(1 for p in processes if "(deleted)" in p.exe)
        self.summary_label.setText(
            f"{len(processes)} process(es) shown"
            + (f"  ·  {flagged} flagged (running from a deleted executable)" if flagged else "")
        )
