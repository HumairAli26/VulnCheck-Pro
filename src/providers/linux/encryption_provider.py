"""
SecureAudit
Linux Disk Encryption Provider

Author: Humair Ali
"""

from __future__ import annotations

import shutil
import subprocess

from src.providers.base import EncryptionProvider, EncryptionStatus


class LinuxEncryptionProvider(EncryptionProvider):
    """Detects LUKS-encrypted block devices via ``lsblk``."""

    def get_status(self) -> EncryptionStatus:
        if not shutil.which("lsblk"):
            return EncryptionStatus(
                encrypted=False,
                error="lsblk is not available on this system.",
            )
        try:
            proc = subprocess.run(
                ["lsblk", "-o", "NAME,TYPE,FSTYPE,MOUNTPOINT"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            output = proc.stdout
            has_luks = "crypto_LUKS" in output or "crypt" in output
            return EncryptionStatus(
                encrypted=has_luks,
                method="LUKS" if has_luks else "None detected",
                details={"backend": "lsblk"},
            )
        except (subprocess.SubprocessError, OSError, PermissionError) as exc:
            return EncryptionStatus(encrypted=False, error=str(exc))
