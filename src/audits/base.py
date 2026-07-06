"""
SecureAudit
Base Audit

Author: Humair Ali
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from src.models.audit_result import AuditResult


class BaseAudit(ABC):
    """Every audit check in SecureAudit inherits from this class."""

    #: Human-readable name shown in the UI and reports.
    name: str = "Unnamed Audit"

    #: Grouping used for the dashboard cards and compliance mapping.
    category: str = "General"

    @abstractmethod
    def run(self) -> AuditResult:
        """Execute the check and return a single AuditResult."""
        raise NotImplementedError
