"""
SecureAudit
Linux Firewall Provider

Author: Humair Ali
"""

from __future__ import annotations

import shutil
import subprocess

from src.providers.base import FirewallProvider, FirewallStatus


class LinuxFirewallProvider(FirewallProvider):
    """
    Checks UFW first (most common on Debian/Ubuntu desktops), and falls
    back to inspecting iptables rules directly if UFW isn't installed.
    """

    def get_status(self) -> FirewallStatus:
        if shutil.which("ufw"):
            return self._check_ufw()
        if shutil.which("iptables"):
            return self._check_iptables()
        return FirewallStatus(
            enabled=False,
            error="Neither ufw nor iptables was found on this system.",
        )

    def _check_ufw(self) -> FirewallStatus:
        try:
            proc = subprocess.run(
                ["ufw", "status", "verbose"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            output = proc.stdout.strip()
            enabled = "Status: active" in output
            return FirewallStatus(
                enabled=enabled,
                profile_details={"backend": "ufw"},
                raw_output=output,
            )
        except (subprocess.SubprocessError, OSError, PermissionError) as exc:
            return FirewallStatus(enabled=False, error=str(exc))

    def _check_iptables(self) -> FirewallStatus:
        try:
            proc = subprocess.run(
                ["iptables", "-L", "-n"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            output = proc.stdout.strip()
            # A default-open chain policy with no rules is effectively "no firewall".
            has_rules = len(output.splitlines()) > 3
            enabled = has_rules
            return FirewallStatus(
                enabled=enabled,
                profile_details={"backend": "iptables"},
                raw_output=output,
            )
        except (subprocess.SubprocessError, OSError, PermissionError) as exc:
            return FirewallStatus(enabled=False, error=str(exc))
