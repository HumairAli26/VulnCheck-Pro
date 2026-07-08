"""
SecureAudit
Screen Lock Audit

Author: Humair Ali
"""

from __future__ import annotations

from src.audits.base import BaseAudit
from src.models.audit_result import AuditResult, AuditStatus, Severity
from src.providers.factory import get_screen_lock_provider

_MAX_RECOMMENDED_TIMEOUT_MINUTES = 10


class ScreenLockAudit(BaseAudit):
    """Checks whether the screen locks automatically and requires a password to resume."""

    name = "Screen Lock"
    category = "Endpoint Security"

    def run(self) -> AuditResult:
        provider = get_screen_lock_provider()
        status = provider.get_status()

        if status.error:
            return AuditResult(
                title=self.name,
                category=self.category,
                status=AuditStatus.FAILED,
                severity=Severity.INFO,
                description=f"Could not determine screen lock status: {status.error}",
                recommendation="Check your screen lock / screensaver settings manually.",
            )

        if not status.enabled:
            return AuditResult(
                title=self.name,
                category=self.category,
                status=AuditStatus.COMPLETED,
                severity=Severity.MEDIUM,
                description=(
                    "The screen does not automatically lock with a password when idle."
                ),
                recommendation=(
                    "Enable an automatic screen lock with a short timeout (5-10 minutes) so "
                    "the device isn't left accessible if unattended."
                ),
                details=status.details,
                cvss=4.6,
                compliance=["CIS Control 4", "NIST CSF PR.AC-7"],
            )

        if status.timeout_minutes and status.timeout_minutes > _MAX_RECOMMENDED_TIMEOUT_MINUTES:
            return AuditResult(
                title=self.name,
                category=self.category,
                status=AuditStatus.COMPLETED,
                severity=Severity.LOW,
                description=(
                    f"The screen locks after {status.timeout_minutes} minutes of inactivity, "
                    f"longer than the recommended {_MAX_RECOMMENDED_TIMEOUT_MINUTES}."
                ),
                recommendation=f"Reduce the lock timeout to {_MAX_RECOMMENDED_TIMEOUT_MINUTES} minutes or less.",
                details=status.details,
                compliance=["CIS Control 4"],
            )

        return AuditResult(
            title=self.name,
            category=self.category,
            status=AuditStatus.COMPLETED,
            severity=Severity.INFO,
            description="The screen locks automatically with a password within a reasonable timeout.",
            recommendation="No action required.",
            details=status.details,
            compliance=["CIS Control 4", "NIST CSF PR.AC-7"],
        )
