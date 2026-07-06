"""
SecureAudit
Linux Update Provider

Author: Humair Ali
"""

from __future__ import annotations

import shutil
import subprocess

from src.providers.base import UpdateProvider, UpdateStatus


class LinuxUpdateProvider(UpdateProvider):
    """Checks for pending package updates via apt or dnf."""

    def get_status(self) -> UpdateStatus:
        if shutil.which("apt"):
            return self._check_apt()
        if shutil.which("dnf"):
            return self._check_dnf()
        return UpdateStatus(
            up_to_date=True,
            error="No supported package manager (apt/dnf) found.",
        )

    def _check_apt(self) -> UpdateStatus:
        try:
            proc = subprocess.run(
                ["apt", "list", "--upgradable"],
                capture_output=True,
                text=True,
                timeout=15,
            )
            lines = [
                line
                for line in proc.stdout.strip().splitlines()
                if line and not line.startswith("Listing...")
            ]
            return UpdateStatus(
                up_to_date=len(lines) == 0,
                pending_count=len(lines),
                pending_items=lines[:10],
            )
        except (subprocess.SubprocessError, OSError, PermissionError) as exc:
            return UpdateStatus(up_to_date=True, error=str(exc))

    def _check_dnf(self) -> UpdateStatus:
        try:
            proc = subprocess.run(
                ["dnf", "check-update"],
                capture_output=True,
                text=True,
                timeout=20,
            )
            # dnf check-update exits 100 when updates ARE available.
            lines = [l for l in proc.stdout.strip().splitlines() if l.strip()]
            pending = lines if proc.returncode == 100 else []
            return UpdateStatus(
                up_to_date=len(pending) == 0,
                pending_count=len(pending),
                pending_items=pending[:10],
            )
        except (subprocess.SubprocessError, OSError, PermissionError) as exc:
            return UpdateStatus(up_to_date=True, error=str(exc))
