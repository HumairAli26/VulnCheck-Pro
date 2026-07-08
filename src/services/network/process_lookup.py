"""
SecureAudit
Process Lookup

Author: Humair Ali

A plain TCP connect scan can tell you a port is open. It can't tell you
*which program opened it*. This module closes that gap using psutil to
correlate listening sockets back to a PID, process name, executable path,
and the user it's running as -- and separately flags a specific, classic
malware/persistence indicator: a running process whose executable file no
longer exists on disk (common when malware deletes itself after loading
into memory, or a compromised binary was quarantined/removed).
"""

from __future__ import annotations

from dataclasses import dataclass, field

import psutil


@dataclass
class ProcessInfo:
    pid: int
    name: str
    username: str = "Unknown"
    exe: str = ""
    cmdline: str = ""
    cpu_percent: float = 0.0
    memory_percent: float = 0.0
    status: str = "unknown"


@dataclass
class ListeningProcess:
    port: int
    process: ProcessInfo | None
    error: str | None = None


def get_process_for_port(port: int) -> ListeningProcess:
    """Find the process (if any) bound to a listening TCP port."""
    try:
        for conn in psutil.net_connections(kind="inet"):
            if (
                conn.status == psutil.CONN_LISTEN
                and conn.laddr
                and conn.laddr.port == port
                and conn.pid
            ):
                return ListeningProcess(port=port, process=_describe(conn.pid))
        return ListeningProcess(port=port, process=None)
    except psutil.AccessDenied:
        return ListeningProcess(
            port=port,
            process=None,
            error="Process attribution requires administrator/root privileges on this OS.",
        )
    except Exception as exc:  # noqa: BLE001 - never let introspection crash a scan
        return ListeningProcess(port=port, process=None, error=str(exc))


def list_processes() -> list[ProcessInfo]:
    """Snapshot of every currently running process, for the Process Explorer page."""
    processes: list[ProcessInfo] = []
    for proc in psutil.process_iter(
        ["pid", "name", "username", "exe", "cmdline", "cpu_percent", "memory_percent", "status"]
    ):
        try:
            info = proc.info
            processes.append(
                ProcessInfo(
                    pid=info.get("pid", -1),
                    name=info.get("name") or "Unknown",
                    username=info.get("username") or "Unknown",
                    exe=info.get("exe") or "",
                    cmdline=" ".join(info.get("cmdline") or []),
                    cpu_percent=info.get("cpu_percent") or 0.0,
                    memory_percent=round(info.get("memory_percent") or 0.0, 2),
                    status=info.get("status") or "unknown",
                )
            )
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return processes


def find_processes_with_deleted_executable() -> list[ProcessInfo]:
    """
    Flags processes whose backing executable file no longer exists on disk --
    a classic sign of malware that deletes itself post-load to dodge
    file-based antivirus/EDR scans, or of a binary removed out from under a
    still-running process.
    """
    suspicious: list[ProcessInfo] = []
    for proc in psutil.process_iter(["pid", "name", "username", "exe", "status"]):
        try:
            exe = proc.info.get("exe")
            if exe and "(deleted)" in exe:
                suspicious.append(
                    ProcessInfo(
                        pid=proc.info.get("pid", -1),
                        name=proc.info.get("name") or "Unknown",
                        username=proc.info.get("username") or "Unknown",
                        exe=exe,
                        status=proc.info.get("status") or "unknown",
                    )
                )
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return suspicious


def _describe(pid: int) -> ProcessInfo | None:
    try:
        proc = psutil.Process(pid)
        with proc.oneshot():
            return ProcessInfo(
                pid=pid,
                name=proc.name(),
                username=_safe(proc.username, "Unknown"),
                exe=_safe(proc.exe, ""),
                cmdline=" ".join(_safe(proc.cmdline, [])),
                cpu_percent=proc.cpu_percent(interval=None),
                memory_percent=round(proc.memory_percent(), 2),
                status=_safe(proc.status, "unknown"),
            )
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        return None


def _safe(getter, default):
    try:
        return getter()
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        return default
