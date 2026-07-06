"""
SecureAudit
Disk Encryption Audit

Author: Humair Ali
"""

from __future__ import annotations

from src.audits.base import BaseAudit
from src.models.audit_result import AuditResult, AuditStatus, Severity
from src.providers.factory import get_encryption_provider


class DiskEncryptionAudit(BaseAudit):
    """Checks whether the system drive is encrypted at rest."""

    name = "Disk Encryption"
    category = "Data Protection"

    def run(self) -> AuditResult:
        provider = get_encryption_provider()
        status = provider.get_status()

        if status.error:
            return AuditResult(
                title=self.name,
                category=self.category,
                status=AuditStatus.FAILED,
                severity=Severity.INFO,
                description=f"Could not determine disk encryption status: {status.error}",
                recommendation="Re-run SecureAudit with administrator/root privileges.",
            )

        if status.encrypted:
            return AuditResult(
                title=self.name,
                category=self.category,
                status=AuditStatus.COMPLETED,
                severity=Severity.INFO,
                description=f"The system drive is encrypted using {status.method}.",
                recommendation="No action required.",
                details=status.details,
                compliance=["CIS Control 3", "NIST 800-53 SC-28"],
            )

        return AuditResult(
            title=self.name,
            category=self.category,
            status=AuditStatus.COMPLETED,
            severity=Severity.CRITICAL,
            description="The system drive does not appear to be encrypted.",
            recommendation=(
                "Enable full-disk encryption (BitLocker on Windows, FileVault on "
                "macOS, or LUKS on Linux) to protect data if the device is lost or stolen."
            ),
            details=status.details,
            cvss=8.1,
            references=["https://www.cisa.gov/topics/cyber-threats-and-advisories"],
            compliance=["CIS Control 3", "NIST 800-53 SC-28"],
        )
