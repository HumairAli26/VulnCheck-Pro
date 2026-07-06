"""
SecureAudit
Firewall Audit

Author: Humair Ali
"""

from __future__ import annotations

from src.audits.base import BaseAudit
from src.models.audit_result import AuditResult, AuditStatus, Severity
from src.providers.factory import get_firewall_provider


class FirewallAudit(BaseAudit):
    """Checks whether the host firewall is active."""

    name = "Firewall Status"
    category = "Network"

    def run(self) -> AuditResult:
        provider = get_firewall_provider()
        status = provider.get_status()

        if status.error:
            recommendation = (
                "Install ufw or iptables to enable firewall auditing on this system."
                if "was not found" in status.error or "was found" in status.error
                else "Re-run SecureAudit with administrator/root privileges."
            )
            return AuditResult(
                title=self.name,
                category=self.category,
                status=AuditStatus.FAILED,
                severity=Severity.INFO,
                description=f"Could not determine firewall status: {status.error}",
                recommendation=recommendation,
            )

        if status.enabled:
            return AuditResult(
                title=self.name,
                category=self.category,
                status=AuditStatus.COMPLETED,
                severity=Severity.INFO,
                description="The host firewall is enabled and active.",
                recommendation="No action required. Periodically review firewall rules.",
                details=status.profile_details,
                compliance=["CIS Control 4", "NIST CSF PR.AC-5"],
            )

        return AuditResult(
            title=self.name,
            category=self.category,
            status=AuditStatus.COMPLETED,
            severity=Severity.HIGH,
            description="The host firewall is disabled or partially disabled.",
            recommendation="Enable the firewall on all active network profiles immediately.",
            details=status.profile_details,
            cvss=7.5,
            references=["https://www.cisecurity.org/controls/network-infrastructure-management"],
            compliance=["CIS Control 4", "NIST CSF PR.AC-5"],
        )
