"""
SecureAudit
Linux Screen Lock Provider

Author: Humair Ali
"""

from __future__ import annotations

import shutil
import subprocess

from src.providers.base import ScreenLockProvider, ScreenLockStatus


class LinuxScreenLockProvider(ScreenLockProvider):
    """Reads GNOME's screensaver lock settings via ``gsettings``."""

    def get_status(self) -> ScreenLockStatus:
        if not shutil.which("gsettings"):
            return ScreenLockStatus(
                enabled=False,
                error="gsettings not found -- this check currently only supports GNOME-based desktops.",
            )
        try:
            lock_enabled = subprocess.run(
                ["gsettings", "get", "org.gnome.desktop.screensaver", "lock-enabled"],
                capture_output=True,
                text=True,
                timeout=5,
            ).stdout.strip()

            idle_delay_raw = subprocess.run(
                ["gsettings", "get", "org.gnome.desktop.session", "idle-delay"],
                capture_output=True,
                text=True,
                timeout=5,
            ).stdout.strip()

            enabled = lock_enabled == "true"
            timeout_minutes = None
            if "uint32" in idle_delay_raw:
                seconds = int("".join(ch for ch in idle_delay_raw if ch.isdigit()) or 0)
                timeout_minutes = seconds // 60

            return ScreenLockStatus(
                enabled=enabled,
                timeout_minutes=timeout_minutes,
                details={"lock_enabled": lock_enabled, "idle_delay": idle_delay_raw},
            )
        except (subprocess.SubprocessError, OSError, ValueError) as exc:
            return ScreenLockStatus(enabled=False, error=str(exc))
