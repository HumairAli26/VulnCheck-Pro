"""
SecureAudit
Port Scanner

Author: Humair Ali

A genuinely full TCP port scan (1-65535), not a fixed watchlist -- plus
two things most "simple" desktop security tools skip entirely:

1. Banner grabbing: a lot of services announce themselves the moment you
   connect (SSH, FTP, SMTP...), which turns "port 22 is open" into
   "OpenSSH 8.9p1 is listening", a much more actionable finding.
2. Auth-less exposure probes: for a small set of services that are
   historically shipped with *no authentication by default* (Redis,
   Memcached), we send one harmless, read-only protocol command and check
   whether it succeeds without credentials. This is the difference between
   "port 6379 is open" (mildly interesting) and "this Redis instance will
   let anyone read/write your data with zero authentication" (urgent).

Every probe here is strictly read-only and sends nothing but a standard
liveness/info command -- nothing that writes data, guesses credentials,
or could be mistaken for exploitation.
"""

from __future__ import annotations

import socket
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Callable

_MAX_PORT = 65535
_DEFAULT_WORKERS = 400
_DEFAULT_CONNECT_TIMEOUT = 0.05
_BANNER_TIMEOUT = 0.3
_PROGRESS_REPORT_EVERY = 2000


def scan_all_ports(
    host: str = "127.0.0.1",
    max_workers: int = _DEFAULT_WORKERS,
    timeout: float = _DEFAULT_CONNECT_TIMEOUT,
    progress_callback: Callable[[int, int], None] | None = None,
) -> list[int]:
    """
    Attempt a TCP connect to every port from 1-65535 and return the ones
    that accepted a connection. Concurrent by design -- a serial scan of
    65535 ports would take minutes; this typically finishes in a few
    seconds on localhost.
    """
    total = _MAX_PORT
    open_ports: list[int] = []
    completed = 0
    lock = threading.Lock()

    def check(port: int) -> int | None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            return port if sock.connect_ex((host, port)) == 0 else None

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for result in executor.map(check, range(1, _MAX_PORT + 1)):
            if result is not None:
                open_ports.append(result)
            with lock:
                completed += 1
                if progress_callback and (
                    completed % _PROGRESS_REPORT_EVERY == 0 or completed == total
                ):
                    progress_callback(completed, total)

    return sorted(open_ports)


def resolve_service_name(port: int) -> str:
    """Best-effort lookup of the well-known service name for a port."""
    try:
        return socket.getservbyport(port, "tcp")
    except OSError:
        return "Unknown"


def grab_banner(host: str, port: int, timeout: float = _BANNER_TIMEOUT) -> str | None:
    """
    Connect and passively read whatever the service sends first, without
    sending anything ourselves. Many text-based protocols (SSH, FTP, SMTP,
    POP3, IMAP) greet unprompted; protocols that don't (most HTTP servers)
    will simply time out here, which is fine -- we fall back to the
    well-known service name instead.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            sock.connect((host, port))
            data = sock.recv(200)
            text = data.decode("utf-8", errors="replace").strip()
            return text[:120] if text else None
    except (OSError, socket.timeout):
        return None


def probe_redis_auth(host: str, port: int, timeout: float = _BANNER_TIMEOUT) -> bool | None:
    """
    Sends a single PING (Redis's own liveness command -- read-only, no
    side effects). Returns True if the connection has NO authentication
    (Redis's historical default), False if it correctly demanded AUTH,
    or None if the service didn't respond like Redis at all.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            sock.connect((host, port))
            sock.sendall(b"PING\r\n")
            response = sock.recv(64)
            if response.startswith(b"+PONG"):
                return True
            if b"NOAUTH" in response:
                return False
            return None
    except (OSError, socket.timeout):
        return None


def probe_memcached_exposed(host: str, port: int, timeout: float = _BANNER_TIMEOUT) -> bool | None:
    """
    Sends Memcached's own 'version' command (read-only, standard liveness
    check). Memcached has no authentication mechanism at all in its
    classic text protocol, so any response here means it's fully exposed.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            sock.connect((host, port))
            sock.sendall(b"version\r\n")
            response = sock.recv(64)
            return response.startswith(b"VERSION")
    except (OSError, socket.timeout):
        return None
