"""
SecureAudit
System Information Audit

Author: Humair Ali
"""

from __future__ import annotations

from src.audits.base import BaseAudit
from src.models.audit_result import AuditResult, AuditStatus, Severity
from src.providers.factory import get_system_provider


class SystemInformationAudit(BaseAudit):
    """Collects general host information. Always informational, never a finding."""

    name = "System Information"
    category = "System"

    def run(self) -> AuditResult:
        provider = get_system_provider()
        snapshot = provider.get_snapshot()

        details = {
            "Hostname": snapshot.hostname,
            "Current User": snapshot.username,
            "Operating System": snapshot.os_name,
            "OS Version": snapshot.os_version,
            "CPU": snapshot.cpu or "Unknown",
            "Memory (GB)": str(snapshot.memory_total_gb),
            "Disk Used / Total (GB)": f"{snapshot.disk_used_gb} / {snapshot.disk_total_gb}",
        }

        return AuditResult(
            title=self.name,
            category=self.category,
            status=AuditStatus.COMPLETED,
            severity=Severity.INFO,
            description="Collected basic system information for this scan's context.",
            recommendation="No action required.",
            details=details,
        )
