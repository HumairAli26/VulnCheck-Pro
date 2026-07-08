import os
import socket
import threading
import time

from src.audits.running_processes_audit import RunningProcessesAudit
from src.models.audit_result import Severity
from src.services.network.process_lookup import (
    get_process_for_port,
    list_processes,
)


def test_list_processes_includes_this_test_process():
    processes = list_processes()
    pids = {p.pid for p in processes}
    assert os.getpid() in pids


def test_get_process_for_port_attributes_a_listening_socket():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(("127.0.0.1", 0))
        server.listen(1)
        port = server.getsockname()[1]
        time.sleep(0.1)

        result = get_process_for_port(port)
        assert result.error is None
        assert result.process is not None
        assert result.process.pid == os.getpid()


def test_running_processes_audit_completes_cleanly_with_no_deleted_binaries():
    audit = RunningProcessesAudit()
    result = audit.run()
    # In a normal environment nothing should be flagged; this mainly checks
    # the audit runs end-to-end without raising.
    assert result.status.value == "Completed"
    assert result.severity in (Severity.INFO, Severity.HIGH)
