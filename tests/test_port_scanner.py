import socket
import threading
import time

import pytest

from src.audits.open_ports_audit import OpenPortsAudit
from src.models.audit_result import Severity
from src.services.network.port_scanner import (
    grab_banner,
    probe_redis_auth,
    resolve_service_name,
    scan_all_ports,
)


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _start_echo_server(port: int, response: bytes) -> None:
    def serve():
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("127.0.0.1", port))
        server.listen(1)
        server.settimeout(2)
        try:
            conn, _ = server.accept()
        except socket.timeout:
            server.close()
            return
        try:
            conn.sendall(response)
        except OSError:
            pass
        finally:
            conn.close()
            server.close()

    threading.Thread(target=serve, daemon=True).start()
    time.sleep(0.2)


def test_scan_all_ports_finds_a_listening_socket():
    port = _free_port()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", port))
    server.listen(1)
    try:
        open_ports = scan_all_ports(host="127.0.0.1")
        assert port in open_ports
    finally:
        server.close()


def test_scan_all_ports_reports_progress():
    calls = []
    scan_all_ports(host="127.0.0.1", progress_callback=lambda done, total: calls.append((done, total)))
    assert calls
    assert calls[-1] == (65535, 65535)


def test_resolve_service_name_recognizes_http():
    assert resolve_service_name(80) in ("http", "www", "www-http")


def test_grab_banner_reads_unsolicited_greeting():
    port = _free_port()
    _start_echo_server(port, b"220 fake-ftp-server ready\r\n")
    banner = grab_banner("127.0.0.1", port)
    assert banner is not None
    assert "fake-ftp-server" in banner


def test_probe_redis_auth_detects_unauthenticated_instance():
    port = _free_port()
    _start_echo_server(port, b"+PONG\r\n")
    assert probe_redis_auth("127.0.0.1", port) is True


def test_probe_redis_auth_detects_auth_required():
    port = _free_port()
    _start_echo_server(port, b"-NOAUTH Authentication required.\r\n")
    assert probe_redis_auth("127.0.0.1", port) is False


def test_open_ports_audit_flags_unauthenticated_redis_as_critical():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind(("127.0.0.1", 6379))
    except OSError:
        pytest.skip("Port 6379 already in use in this environment.")
    server.listen(5)

    def serve():
        while True:
            try:
                conn, _ = server.accept()
            except OSError:
                return
            try:
                conn.recv(64)
                conn.sendall(b"+PONG\r\n")
            except OSError:
                pass
            finally:
                conn.close()

    thread = threading.Thread(target=serve, daemon=True)
    thread.start()
    time.sleep(0.2)

    try:
        audit = OpenPortsAudit()
        result = audit.run()
        assert result.severity == Severity.CRITICAL
        assert "NO AUTHENTICATION" in result.details["6379"]
    finally:
        server.close()
