"""
SecureAudit
Audit Registry

Author: Humair Ali

Adding a new audit to a scan is a one-line change here -- nothing in the
engine, UI, or CLI needs to know it exists.
"""

from __future__ import annotations

from src.audits.base import BaseAudit
from src.audits.disk_encryption_audit import DiskEncryptionAudit
from src.audits.firewall_audit import FirewallAudit
from src.audits.open_ports_audit import OpenPortsAudit
from src.audits.running_processes_audit import RunningProcessesAudit
from src.audits.screen_lock_audit import ScreenLockAudit
from src.audits.system_information import SystemInformationAudit
from src.audits.updates_audit import UpdatesAudit

#: Audits included in a Quick Scan -- fast, no elevated privileges required.
QUICK_SCAN_AUDITS: list[type[BaseAudit]] = [
    SystemInformationAudit,
    FirewallAudit,
    OpenPortsAudit,
]

#: Audits included in a Full Scan -- everything, including checks that may
#: require administrator/root privileges to return a definitive answer.
FULL_SCAN_AUDITS: list[type[BaseAudit]] = [
    SystemInformationAudit,
    FirewallAudit,
    DiskEncryptionAudit,
    UpdatesAudit,
    OpenPortsAudit,
    ScreenLockAudit,
    RunningProcessesAudit,
]


def build_quick_scan() -> list[BaseAudit]:
    return [audit_cls() for audit_cls in QUICK_SCAN_AUDITS]


def build_full_scan() -> list[BaseAudit]:
    return [audit_cls() for audit_cls in FULL_SCAN_AUDITS]
