"""
SecureAudit Engine

Author: Humair Ali
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable, Iterable

from src.core.logger import logger
from src.models.audit_result import AuditResult, AuditStatus, Severity


@dataclass
class ScanSummary:
    """Aggregate outcome of running a full set of audits."""

    started_at: str
    finished_at: str
    duration_seconds: float
    results: list[AuditResult] = field(default_factory=list)

    @property
    def security_score(self) -> int:
        """
        A single 0-100 "security score" for the dashboard, where 100 is a
        clean bill of health. Each finding subtracts its severity weight.
        """
        penalty = sum(r.risk_score for r in self.results)
        return max(0, 100 - penalty)

    @property
    def risk_distribution(self) -> dict[str, int]:
        """Count of findings per severity, used for the dashboard pie chart."""
        counts = {s.value: 0 for s in Severity}
        for result in self.results:
            counts[result.severity.value] += 1
        return counts

    @property
    def failed_count(self) -> int:
        return sum(1 for r in self.results if r.status == AuditStatus.FAILED)


class AuditEngine:
    """
    Runs all registered audits and produces a ScanSummary.

    Audits are simple objects exposing ``.name`` and ``.run() -> AuditResult``.
    The engine itself has no knowledge of *what* an audit checks -- that
    keeps this class stable even as the audit catalog grows.
    """

    def __init__(self) -> None:
        self._audits: list = []

    def register(self, audit) -> None:
        self._audits.append(audit)

    def register_all(self, audits: Iterable) -> None:
        for audit in audits:
            self.register(audit)

    def run(
        self,
        progress_callback: Callable[[int, int, str], None] | None = None,
    ) -> ScanSummary:
        """
        Execute every registered audit in order.

        progress_callback, if provided, is invoked as
        (completed_count, total_count, current_audit_name) after each audit,
        which the Scan page uses to drive a QProgressBar without the engine
        needing to know anything about Qt.
        """
        started = datetime.now()
        results: list[AuditResult] = []
        total = len(self._audits)

        for index, audit in enumerate(self._audits, start=1):
            name = getattr(audit, "name", audit.__class__.__name__)
            try:
                result = audit.run()
                results.append(result)
            except Exception as exc:  # noqa: BLE001 - an audit must never crash the app
                logger.exception(f"Audit '{name}' raised an exception")
                results.append(
                    AuditResult(
                        title=name,
                        category=getattr(audit, "category", "General"),
                        status=AuditStatus.FAILED,
                        severity=Severity.INFO,
                        description=f"The audit could not complete: {exc}",
                        recommendation="Re-run the scan. If this persists, check logs/secureaudit.log.",
                    )
                )
            if progress_callback:
                progress_callback(index, total, name)

        finished = datetime.now()
        return ScanSummary(
            started_at=started.isoformat(timespec="seconds"),
            finished_at=finished.isoformat(timespec="seconds"),
            duration_seconds=round((finished - started).total_seconds(), 3),
            results=results,
        )
