"""
SecureAudit
macOS Firewall Provider

Author: Humair Ali

NOTE: Requires macOS to run; cannot be executed/verified in this sandbox.
"""

from __future__ import annotations

import subprocess

from src.providers.base import FirewallProvider, FirewallStatus

_SOCKETFILTERFW = "/usr/libexec/ApplicationFirewall/socketfilterfw"


class MacOSFirewallProvider(FirewallProvider):
    """Reads Application Firewall state via ``socketfilterfw``."""

    def get_status(self) -> FirewallStatus:
        try:
            proc = subprocess.run(
                [_SOCKETFILTERFW, "--getglobalstate"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            output = proc.stdout.strip()
            enabled = "enabled" in output.lower()
            return FirewallStatus(enabled=enabled, raw_output=output)
        except (subprocess.SubprocessError, OSError, FileNotFoundError) as exc:
            return FirewallStatus(enabled=False, error=str(exc))
