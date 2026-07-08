"""
SecureAudit
Base Audit

Author: Humair Ali
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Callable

from src.models.audit_result import AuditResult


class BaseAudit(ABC):
    """Every audit check in SecureAudit inherits from this class."""

    #: Human-readable name shown in the UI and reports.
    name: str = "Unnamed Audit"

    #: Grouping used for the dashboard cards and compliance mapping.
    category: str = "General"

    def __init__(self) -> None:
        self._progress_callback: Callable[[int, int], None] | None = None

    def set_progress_callback(self, callback: Callable[[int, int], None]) -> None:
        """
        Optional hook for long-running audits (e.g. a full 65535-port scan)
        to report fine-grained (done, total) progress mid-check. No-op for
        audits that don't need it -- the engine and UI both work fine
        whether or not a given audit calls this.
        """
        self._progress_callback = callback

    def _report_progress(self, done: int, total: int) -> None:
        if self._progress_callback:
            self._progress_callback(done, total)

    @abstractmethod
    def run(self) -> AuditResult:
        """Execute the check and return a single AuditResult."""
        raise NotImplementedError
