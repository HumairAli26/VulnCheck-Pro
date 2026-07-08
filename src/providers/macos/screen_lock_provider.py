"""
SecureAudit
macOS Screen Lock Provider

Author: Humair Ali

NOTE: Requires macOS to run; cannot be executed/verified in this sandbox.
"""

from __future__ import annotations

import subprocess

from src.providers.base import ScreenLockProvider, ScreenLockStatus


class MacOSScreenLockProvider(ScreenLockProvider):
    """Reads the 'require password after sleep/screensaver' setting via ``defaults``."""

    def get_status(self) -> ScreenLockStatus:
        try:
            ask_for_password = subprocess.run(
                ["defaults", "read", "com.apple.screensaver", "askForPassword"],
                capture_output=True,
                text=True,
                timeout=5,
            ).stdout.strip()

            delay_raw = subprocess.run(
                ["defaults", "read", "com.apple.screensaver", "askForPasswordDelay"],
                capture_output=True,
                text=True,
                timeout=5,
            ).stdout.strip()

            enabled = ask_for_password == "1"
            timeout_minutes = None
            if delay_raw.replace(".", "", 1).isdigit():
                timeout_minutes = int(float(delay_raw)) // 60

            return ScreenLockStatus(
                enabled=enabled,
                timeout_minutes=timeout_minutes,
                details={"askForPassword": ask_for_password, "askForPasswordDelay": delay_raw},
            )
        except (subprocess.SubprocessError, OSError) as exc:
            return ScreenLockStatus(enabled=False, error=str(exc))
