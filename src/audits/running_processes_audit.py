"""
SecureAudit
Running Processes Audit

Author: Humair Ali
"""

from __future__ import annotations

from src.audits.base import BaseAudit
from src.models.audit_result import AuditResult, AuditStatus, Severity
from src.services.network.process_lookup import find_processes_with_deleted_executable, list_processes


class RunningProcessesAudit(BaseAudit):
    """
    Checks for processes whose backing executable file no longer exists on
    disk. This is a well-known technique used by malware that deletes its
    own binary after loading into memory specifically to evade file-based
    antivirus scans -- something a simple port scanner or firewall check
    would never surface.
    """

    name = "Running Processes"
    category = "Endpoint Security"

    def run(self) -> AuditResult:
        try:
            all_processes = list_processes()
            suspicious = find_processes_with_deleted_executable()
        except Exception as exc:  # noqa: BLE001
            return AuditResult(
                title=self.name,
                category=self.category,
                status=AuditStatus.FAILED,
                severity=Severity.INFO,
                description=f"Could not enumerate running processes: {exc}",
                recommendation="Re-run with elevated privileges if this persists.",
            )

        if not suspicious:
            return AuditResult(
                title=self.name,
                category=self.category,
                status=AuditStatus.COMPLETED,
                severity=Severity.INFO,
                description=(
                    f"Scanned {len(all_processes)} running process(es); none are running from "
                    "a deleted executable file."
                ),
                recommendation="No action required.",
                compliance=["MITRE ATT&CK T1070.004"],
            )

        details = {
            f"PID {p.pid}": f"{p.name} (user={p.username}) — {p.exe}" for p in suspicious
        }

        return AuditResult(
            title=self.name,
            category=self.category,
            status=AuditStatus.COMPLETED,
            severity=Severity.HIGH,
            description=(
                f"{len(suspicious)} process(es) are running from an executable file that no "
                "longer exists on disk -- a common technique used to evade file-based "
                "antivirus/EDR scanning after the malicious code is already loaded in memory."
            ),
            recommendation=(
                "Investigate each flagged process immediately. If it's not a legitimate "
                "application you recently updated/uninstalled while it was still running, "
                "treat it as a potential compromise: capture details, terminate it, and run a "
                "full antivirus/EDR scan."
            ),
            details=details,
            cvss=7.8,
            compliance=["MITRE ATT&CK T1070.004", "NIST CSF DE.CM-7"],
        )
