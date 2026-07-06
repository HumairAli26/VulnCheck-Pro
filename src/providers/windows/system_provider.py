"""
SecureAudit
Windows System Provider

Author: Humair Ali
"""

from __future__ import annotations

import getpass
import platform
import shutil
import socket

from src.providers.base import SystemProvider, SystemSnapshot


class WindowsSystemProvider(SystemProvider):
    """Collects general host information using stdlib only (no admin rights needed)."""

    def get_snapshot(self) -> SystemSnapshot:
        disk_total, disk_used = self._read_disk_gb()
        return SystemSnapshot(
            hostname=socket.gethostname(),
            username=getpass.getuser(),
            os_name=platform.system(),
            os_version=platform.version(),
            cpu=platform.processor(),
            memory_total_gb=self._read_memory_gb(),
            disk_total_gb=disk_total,
            disk_used_gb=disk_used,
        )

    @staticmethod
    def _read_memory_gb() -> float:
        try:
            import ctypes

            class MEMORYSTATUSEX(ctypes.Structure):
                _fields_ = [
                    ("dwLength", ctypes.c_ulong),
                    ("dwMemoryLoad", ctypes.c_ulong),
                    ("ullTotalPhys", ctypes.c_ulonglong),
                    ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong),
                    ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong),
                    ("ullAvailVirtual", ctypes.c_ulonglong),
                    ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
                ]

            stat = MEMORYSTATUSEX()
            stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))  # type: ignore[attr-defined]
            return round(stat.ullTotalPhys / (1024**3), 2)
        except Exception:
            return 0.0

    @staticmethod
    def _read_disk_gb() -> tuple[float, float]:
        try:
            usage = shutil.disk_usage("C:\\")
            return (
                round(usage.total / (1024**3), 2),
                round(usage.used / (1024**3), 2),
            )
        except OSError:
            return 0.0, 0.0
