"""
SecureAudit
Scan Worker (QThread)

Author: Humair Ali
"""

from __future__ import annotations

from PySide6.QtCore import QThread, Signal

from src.audits.base import BaseAudit
from src.core.audit_engine import AuditEngine, ScanSummary


class ScanWorker(QThread):
    """
    Runs a list of audits on a background thread so the GUI never freezes
    mid-scan, and reports progress back to the Scan page.
    """

    progress = Signal(int, int, str)
    finished_scan = Signal(object)  # emits ScanSummary

    def __init__(self, audits: list[BaseAudit], parent=None):
        super().__init__(parent)
        self._audits = audits

    def run(self) -> None:  # noqa: N802 - Qt override
        engine = AuditEngine()
        engine.register_all(self._audits)
        summary: ScanSummary = engine.run(
            progress_callback=lambda done, total, name: self.progress.emit(done, total, name)
        )
        self.finished_scan.emit(summary)
