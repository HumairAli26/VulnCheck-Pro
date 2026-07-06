"""
SecureAudit
Windows Firewall Provider

Author: Humair Ali

NOTE: This module shells out to ``netsh``, which only exists on Windows.
It cannot be executed or verified on non-Windows machines (including the
sandbox this was authored in) -- test on a real Windows host before
relying on it.
"""

from __future__ import annotations

import subprocess

from src.providers.base import FirewallProvider, FirewallStatus


class WindowsFirewallProvider(FirewallProvider):
    """Reads firewall profile state via ``netsh advfirewall``."""

    def get_status(self) -> FirewallStatus:
        try:
            proc = subprocess.run(
                ["netsh", "advfirewall", "show", "allprofiles"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            output = proc.stdout
            profiles: dict[str, str] = {}
            current_profile = None
            for line in output.splitlines():
                stripped = line.strip()
                if stripped.endswith("Profile Settings:"):
                    current_profile = stripped.replace("Profile Settings:", "").strip()
                elif stripped.startswith("State") and current_profile:
                    state = stripped.split()[-1]
                    profiles[current_profile] = state

            enabled = bool(profiles) and all(
                state.upper() == "ON" for state in profiles.values()
            )
            return FirewallStatus(
                enabled=enabled,
                profile_details=profiles,
                raw_output=output,
            )
        except (subprocess.SubprocessError, OSError, FileNotFoundError) as exc:
            return FirewallStatus(enabled=False, error=str(exc))
