"""
SecureAudit
Automatic Updates Audit

Author: Humair Ali
"""

from __future__ import annotations

from src.audits.base import BaseAudit
from src.models.audit_result import AuditResult, AuditStatus, Severity
from src.providers.factory import get_update_provider


class UpdatesAudit(BaseAudit):
    """Checks for pending OS security updates."""

    name = "Automatic Updates"
    category = "Patch Management"

    def run(self) -> AuditResult:
        provider = get_update_provider()
        status = provider.get_status()

        if status.error:
            return AuditResult(
                title=self.name,
                category=self.category,
                status=AuditStatus.FAILED,
                severity=Severity.INFO,
                description=f"Could not determine update status: {status.error}",
                recommendation="Check for updates manually via your OS update utility.",
            )

        if status.up_to_date:
            return AuditResult(
                title=self.name,
                category=self.category,
                status=AuditStatus.COMPLETED,
                severity=Severity.INFO,
                description="No pending security updates were found.",
                recommendation="No action required. Keep automatic updates enabled.",
                compliance=["CIS Control 7", "NIST CSF PR.MA-1"],
            )

        severity = Severity.HIGH if status.pending_count > 5 else Severity.MEDIUM
        return AuditResult(
            title=self.name,
            category=self.category,
            status=AuditStatus.COMPLETED,
            severity=severity,
            description=f"{status.pending_count} pending update(s) were found.",
            recommendation="Install pending updates as soon as possible, prioritizing security patches.",
            details={"pending_items": ", ".join(status.pending_items) or "See update utility"},
            cvss=6.5 if severity == Severity.HIGH else 4.5,
            compliance=["CIS Control 7", "NIST CSF PR.MA-1"],
        )
