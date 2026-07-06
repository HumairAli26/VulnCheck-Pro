"""
System Information Audit
Author: Humair Ali
"""
import getpass
import platform
import socket

from src.audit.system.base import BaseSystemAudit
from src.models.audit_result import AuditResult

class SystemInformationAudit(BaseSystemAudit):
    def run(self) -> AuditResult:
        details = {
            "Operating System": platform.system(),
            "OS Version": platform.version(),
            "Hostname": socket.gethostname(),
            "Current User": getpass.getuser(),
            "Python Version": platform.python_version(),
        }

        return AuditResult(
            title="System Information",
            status="Completed",
            risk="Informational",
            description="Collected basic system information.",
            recommendation="No action required.",
            details=details,
        )