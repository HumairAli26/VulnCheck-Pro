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
        for audit in self._audits:
            audit.set_progress_callback(self._make_subtask_relay(audit))

    def _make_subtask_relay(self, audit: BaseAudit):
        name = getattr(audit, "name", audit.__class__.__name__)

        def relay(done: int, total: int) -> None:
            # (0, 0, text) is a sentinel the Scan page reads as "update the
            # status text only -- this isn't the per-audit progress bar."
            self.progress.emit(0, 0, f"{name}: {done:,}/{total:,}")

        return relay

    def run(self) -> None:  # noqa: N802 - Qt override
        engine = AuditEngine()
        engine.register_all(self._audits)
        summary: ScanSummary = engine.run(
            progress_callback=lambda done, total, name: self.progress.emit(done, total, name)
        )
        self.finished_scan.emit(summary)
