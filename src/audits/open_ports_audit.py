"""
SecureAudit
Open Ports Audit (Full Range Scan)

Author: Humair Ali
"""

from __future__ import annotations

from src.audits.base import BaseAudit
from src.models.audit_result import AuditResult, AuditStatus, Severity
from src.services.network.port_scanner import (
    grab_banner,
    probe_memcached_exposed,
    probe_redis_auth,
    resolve_service_name,
    scan_all_ports,
)
from src.services.network.process_lookup import get_process_for_port
from src.services.remediation.port_threats import PORT_THREATS

_HOST = "127.0.0.1"

# More open ports than this on a general-purpose workstation is unusual
# enough to call out even if none of them individually match the catalog.
_UNUSUAL_OPEN_PORT_COUNT = 15

# Only probe a bounded number of open ports for banners/auth so a machine
# with an unusually large number of open ports can't turn a ~3s port scan
# into a multi-minute one.
_MAX_PROBED_PORTS = 60


class OpenPortsAudit(BaseAudit):
    """
    Scans the entire TCP port range (1-65535) on localhost -- not a fixed
    watchlist -- then goes further than a simple port scanner would:
    cross-references every open port against a curated threat catalog,
    grabs service banners where available, and actively probes Redis /
    Memcached (both historically shipped with zero authentication by
    default) to tell "port is open" apart from "this is unauthenticated
    and readable by anyone right now".
    """

    name = "Open Ports"
    category = "Network"

    def run(self) -> AuditResult:
        open_ports = scan_all_ports(
            host=_HOST,
            progress_callback=lambda done, total: self._report_progress(done, total),
        )

        if not open_ports:
            return AuditResult(
                title=self.name,
                category=self.category,
                status=AuditStatus.COMPLETED,
                severity=Severity.INFO,
                description="A full scan of all 65,535 TCP ports found nothing listening on localhost.",
                recommendation="No action required.",
                compliance=["CIS Control 4"],
            )

        known_risky: list[int] = []
        unauthenticated: list[int] = []
        details: dict[str, str] = {}

        for index, port in enumerate(open_ports):
            entry = resolve_service_name(port)

            if port in PORT_THREATS:
                known_risky.append(port)
                entry = PORT_THREATS[port].service

            if index < _MAX_PROBED_PORTS:
                if port == 6379 and probe_redis_auth(_HOST, port) is True:
                    unauthenticated.append(port)
                    entry += " -- NO AUTHENTICATION REQUIRED (anyone can read/write)"
                elif port == 11211 and probe_memcached_exposed(_HOST, port):
                    unauthenticated.append(port)
                    entry += " -- fully exposed (Memcached has no authentication mechanism)"
                elif port not in PORT_THREATS:
                    banner = grab_banner(_HOST, port)
                    if banner:
                        entry = f"{entry} — {banner}"

                owner = get_process_for_port(port)
                if owner.process:
                    entry += (
                        f"  [PID {owner.process.pid}: {owner.process.name}"
                        f", user={owner.process.username}]"
                    )

            details[str(port)] = entry

        severity, cvss = self._score(known_risky, unauthenticated, open_ports)
        description = self._describe(known_risky, unauthenticated, open_ports)
        recommendation = self._recommend(known_risky, unauthenticated)

        return AuditResult(
            title=self.name,
            category=self.category,
            status=AuditStatus.COMPLETED,
            severity=severity,
            description=description,
            recommendation=recommendation,
            details=details,
            cvss=cvss,
            compliance=["CIS Control 4", "MITRE ATT&CK T1046"],
        )

    @staticmethod
    def _score(
        known_risky: list[int], unauthenticated: list[int], open_ports: list[int]
    ) -> tuple[Severity, float]:
        if unauthenticated:
            return Severity.CRITICAL, 9.4
        if known_risky:
            return Severity.HIGH, 7.2
        if len(open_ports) > _UNUSUAL_OPEN_PORT_COUNT:
            return Severity.MEDIUM, 5.0
        return Severity.LOW, 2.0

    @staticmethod
    def _describe(
        known_risky: list[int], unauthenticated: list[int], open_ports: list[int]
    ) -> str:
        parts = [f"A full scan of all 65,535 TCP ports found {len(open_ports)} open."]
        if unauthenticated:
            parts.append(
                f"{len(unauthenticated)} service(s) responded with NO authentication required: "
                + ", ".join(str(p) for p in unauthenticated) + "."
            )
        if known_risky:
            parts.append(
                f"{len(known_risky)} match known-risky service(s): "
                + ", ".join(str(p) for p in known_risky) + "."
            )
        return " ".join(parts)

    @staticmethod
    def _recommend(known_risky: list[int], unauthenticated: list[int]) -> str:
        if unauthenticated:
            return (
                "Open 'View Fix Steps' on this finding immediately -- at least one exposed "
                "service will accept connections from anyone with no password."
            )
        if known_risky:
            return "Review each flagged port's fix steps and close or restrict anything not explicitly needed."
        return "Review the open ports listed; close anything you don't recognize or need."
