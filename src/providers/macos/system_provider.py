"""
SecureAudit
macOS System Provider

Author: Humair Ali
"""

from __future__ import annotations

import getpass
import platform
import shutil
import socket
import subprocess

from src.providers.base import SystemProvider, SystemSnapshot


class MacOSSystemProvider(SystemProvider):
    """Collects general host information using stdlib + ``sysctl``."""

    def get_snapshot(self) -> SystemSnapshot:
        disk_total, disk_used = self._read_disk_gb()
        return SystemSnapshot(
            hostname=socket.gethostname(),
            username=getpass.getuser(),
            os_name=platform.system(),
            os_version=platform.mac_ver()[0] or platform.version(),
            cpu=self._read_cpu_brand(),
            memory_total_gb=self._read_memory_gb(),
            disk_total_gb=disk_total,
            disk_used_gb=disk_used,
        )

    @staticmethod
    def _read_cpu_brand() -> str:
        try:
            proc = subprocess.run(
                ["sysctl", "-n", "machdep.cpu.brand_string"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            return proc.stdout.strip() or platform.processor()
        except (subprocess.SubprocessError, OSError):
            return platform.processor()

    @staticmethod
    def _read_memory_gb() -> float:
        try:
            proc = subprocess.run(
                ["sysctl", "-n", "hw.memsize"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            bytes_total = int(proc.stdout.strip())
            return round(bytes_total / (1024**3), 2)
        except (subprocess.SubprocessError, OSError, ValueError):
            return 0.0

    @staticmethod
    def _read_disk_gb() -> tuple[float, float]:
        try:
            usage = shutil.disk_usage("/")
            return (
                round(usage.total / (1024**3), 2),
                round(usage.used / (1024**3), 2),
            )
        except OSError:
            return 0.0, 0.0
