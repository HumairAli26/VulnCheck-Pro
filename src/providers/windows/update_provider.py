"""
SecureAudit
Windows Update Provider

Author: Humair Ali

NOTE: Uses the Windows Update Agent COM API via PowerShell. Requires
Windows to run; cannot be executed in this sandbox.
"""

from __future__ import annotations

import subprocess

from src.providers.base import UpdateProvider, UpdateStatus

_PS_SCRIPT = (
    "$s = New-Object -ComObject Microsoft.Update.Session; "
    "$searcher = $s.CreateUpdateSearcher(); "
    "$result = $searcher.Search(\"IsInstalled=0 and Type='Software'\"); "
    "$result.Updates | ForEach-Object { $_.Title }"
)


class WindowsUpdateProvider(UpdateProvider):
    """Queries the Windows Update Agent for pending software updates."""

    def get_status(self) -> UpdateStatus:
        try:
            proc = subprocess.run(
                ["powershell", "-NoProfile", "-Command", _PS_SCRIPT],
                capture_output=True,
                text=True,
                timeout=60,
            )
            items = [line.strip() for line in proc.stdout.splitlines() if line.strip()]
            return UpdateStatus(
                up_to_date=len(items) == 0,
                pending_count=len(items),
                pending_items=items[:10],
            )
        except FileNotFoundError:
            return UpdateStatus(
                up_to_date=True,
                error="PowerShell was not found on this system.",
            )
        except (subprocess.SubprocessError, OSError) as exc:
            return UpdateStatus(up_to_date=True, error=str(exc))
