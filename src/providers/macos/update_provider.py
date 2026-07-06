"""
SecureAudit
macOS Update Provider

Author: Humair Ali

NOTE: Requires macOS to run; cannot be executed/verified in this sandbox.
"""

from __future__ import annotations

import subprocess

from src.providers.base import UpdateProvider, UpdateStatus


class MacOSUpdateProvider(UpdateProvider):
    """Checks for pending macOS software updates via ``softwareupdate -l``."""

    def get_status(self) -> UpdateStatus:
        try:
            proc = subprocess.run(
                ["softwareupdate", "-l"],
                capture_output=True,
                text=True,
                timeout=60,
            )
            output = proc.stdout
            items = [
                line.strip()
                for line in output.splitlines()
                if line.strip().startswith("*")
            ]
            no_updates = "No new software available" in output
            return UpdateStatus(
                up_to_date=no_updates or len(items) == 0,
                pending_count=len(items),
                pending_items=items[:10],
            )
        except (subprocess.SubprocessError, OSError, FileNotFoundError) as exc:
            return UpdateStatus(up_to_date=True, error=str(exc))
