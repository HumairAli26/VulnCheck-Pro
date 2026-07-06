"""
SecureAudit
macOS Disk Encryption Provider (FileVault)

Author: Humair Ali

NOTE: Requires macOS to run; cannot be executed/verified in this sandbox.
"""

from __future__ import annotations

import subprocess

from src.providers.base import EncryptionProvider, EncryptionStatus


class MacOSEncryptionProvider(EncryptionProvider):
    """Reads FileVault status via ``fdesetup status``."""

    def get_status(self) -> EncryptionStatus:
        try:
            proc = subprocess.run(
                ["fdesetup", "status"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            output = proc.stdout.strip()
            enabled = "FileVault is On" in output
            return EncryptionStatus(
                encrypted=enabled,
                method="FileVault",
                details={"raw": output},
            )
        except (subprocess.SubprocessError, OSError, FileNotFoundError) as exc:
            return EncryptionStatus(encrypted=False, error=str(exc))
