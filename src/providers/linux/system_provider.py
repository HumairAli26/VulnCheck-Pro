"""
SecureAudit
Linux System Provider

Author: Humair Ali
"""

from __future__ import annotations

import getpass
import platform
import shutil
import socket
import subprocess

from src.providers.base import SystemProvider, SystemSnapshot


class LinuxSystemProvider(SystemProvider):
    """Collects general host information using stdlib + /proc where possible."""

    def get_snapshot(self) -> SystemSnapshot:
        memory_gb = self._read_memory_gb()
        disk_total, disk_used = self._read_disk_gb()

        return SystemSnapshot(
            hostname=socket.gethostname(),
            username=getpass.getuser(),
            os_name=platform.system(),
            os_version=platform.version(),
            cpu=platform.processor() or platform.machine(),
            memory_total_gb=memory_gb,
            disk_total_gb=disk_total,
            disk_used_gb=disk_used,
            uptime=self._read_uptime(),
        )

    @staticmethod
    def _read_memory_gb() -> float:
        try:
            with open("/proc/meminfo") as f:
                for line in f:
                    if line.startswith("MemTotal:"):
                        kb = int(line.split()[1])
                        return round(kb / (1024 * 1024), 2)
        except OSError:
            pass
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

    @staticmethod
    def _read_uptime() -> str:
        try:
            proc = subprocess.run(
                ["uptime", "-p"], capture_output=True, text=True, timeout=5
            )
            return proc.stdout.strip() or "Unknown"
        except (subprocess.SubprocessError, OSError):
            return "Unknown"
