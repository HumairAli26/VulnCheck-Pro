"""
SecureAudit
Open Ports Audit

Author: Humair Ali
"""

from __future__ import annotations

import socket

from src.audits.base import BaseAudit
from src.models.audit_result import AuditResult, AuditStatus, Severity

# Common ports that are risky to expose on a general-purpose workstation
# if left open unintentionally.
_WATCHED_PORTS = {
    21: "FTP",
    23: "Telnet",
    135: "RPC",
    139: "NetBIOS",
    445: "SMB",
    3389: "RDP",
    5900: "VNC",
}


class OpenPortsAudit(BaseAudit):
    """Scans localhost for commonly-risky listening ports."""

    name = "Open Ports"
    category = "Network"

    def run(self) -> AuditResult:
        open_ports: dict[str, str] = {}
        for port, service in _WATCHED_PORTS.items():
            if self._is_open(port):
                open_ports[str(port)] = service

        if not open_ports:
            return AuditResult(
                title=self.name,
                category=self.category,
                status=AuditStatus.COMPLETED,
                severity=Severity.INFO,
                description="No commonly-risky ports were found open on localhost.",
                recommendation="No action required.",
                compliance=["CIS Control 4"],
            )

        severity = Severity.HIGH if len(open_ports) > 1 else Severity.MEDIUM
        return AuditResult(
            title=self.name,
            category=self.category,
            status=AuditStatus.COMPLETED,
            severity=severity,
            description=f"{len(open_ports)} commonly-risky port(s) are open: "
            + ", ".join(f"{p} ({s})" for p, s in open_ports.items()),
            recommendation="Close unused services or restrict access to these ports via the firewall.",
            details=open_ports,
            cvss=6.1,
            compliance=["CIS Control 4", "MITRE ATT&CK T1046"],
        )

    @staticmethod
    def _is_open(port: int, host: str = "127.0.0.1", timeout: float = 0.3) -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            return sock.connect_ex((host, port)) == 0
