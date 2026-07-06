"""
SecureAudit
Audit Result Model

Author: Humair Ali
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class Severity(str, Enum):
    """Severity levels for an audit finding, ordered low -> high."""

    INFO = "Informational"
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

    @property
    def weight(self) -> int:
        """Contribution of this severity to the aggregate risk score."""
        return {
            Severity.INFO: 0,
            Severity.LOW: 5,
            Severity.MEDIUM: 15,
            Severity.HIGH: 30,
            Severity.CRITICAL: 50,
        }[self]


class AuditStatus(str, Enum):
    """Outcome status of running an individual audit."""

    COMPLETED = "Completed"
    FAILED = "Failed"
    SKIPPED = "Skipped"
    UNSUPPORTED = "Unsupported"


@dataclass
class AuditResult:
    """
    Represents the result of one audit check.

    Kept intentionally flat and JSON-serializable so it can be persisted
    to SQLite and rendered directly into PDF / HTML / CSV reports without
    an intermediate transformation step.
    """

    title: str
    category: str
    status: AuditStatus
    severity: Severity
    description: str
    recommendation: str
    details: dict[str, str] = field(default_factory=dict)
    cvss: float = 0.0
    references: list[str] = field(default_factory=list)
    compliance: list[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat(timespec="seconds"))

    # --- Backwards-compatible alias -------------------------------------
    # Earlier prototype code (test_engine.py) referred to this field as
    # ``risk``. Keeping the property avoids breaking that script while the
    # rest of the app standardizes on ``severity``.
    @property
    def risk(self) -> str:
        return self.severity.value

    @property
    def risk_score(self) -> int:
        """Numeric contribution of this single finding to overall risk."""
        return self.severity.weight

    def to_dict(self) -> dict:
        """Flat, JSON-safe representation used by reports and the database."""
        return {
            "title": self.title,
            "category": self.category,
            "status": self.status.value,
            "severity": self.severity.value,
            "description": self.description,
            "recommendation": self.recommendation,
            "details": self.details,
            "cvss": self.cvss,
            "references": self.references,
            "compliance": self.compliance,
            "timestamp": self.timestamp,
            "risk_score": self.risk_score,
        }
