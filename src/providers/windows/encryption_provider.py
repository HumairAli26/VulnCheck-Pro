"""
SecureAudit
Windows Disk Encryption Provider (BitLocker)

Author: Humair Ali

NOTE: Requires an elevated (Administrator) prompt to query ``manage-bde``
reliably. Not executable/verifiable outside Windows.
"""

from __future__ import annotations

import subprocess

from src.providers.base import EncryptionProvider, EncryptionStatus


class WindowsEncryptionProvider(EncryptionProvider):
    """Reads BitLocker status for the system drive via ``manage-bde``."""

    def get_status(self) -> EncryptionStatus:
        try:
            proc = subprocess.run(
                ["manage-bde", "-status", "C:"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            output = proc.stdout
            protection_on = "Protection On" in output
            percent_line = next(
                (l for l in output.splitlines() if "Percentage Encrypted" in l),
                "",
            )
            return EncryptionStatus(
                encrypted=protection_on,
                method="BitLocker",
                details={"percentage_encrypted": percent_line.strip()},
            )
        except FileNotFoundError:
            return EncryptionStatus(
                encrypted=False,
                error="manage-bde not found (BitLocker may be unavailable on this edition of Windows).",
            )
        except (subprocess.SubprocessError, OSError) as exc:
            return EncryptionStatus(
                encrypted=False,
                error=f"{exc}. This check usually requires an Administrator prompt.",
            )
