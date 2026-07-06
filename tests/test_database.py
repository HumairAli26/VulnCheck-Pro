from src.core.audit_engine import ScanSummary
from src.models.audit_result import AuditResult, AuditStatus, Severity
from src.services.database.db_manager import DatabaseManager


def _sample_summary() -> ScanSummary:
    result = AuditResult(
        title="Disk Encryption",
        category="Data Protection",
        status=AuditStatus.COMPLETED,
        severity=Severity.CRITICAL,
        description="Not encrypted",
        recommendation="Enable encryption",
    )
    return ScanSummary(
        started_at="2026-01-01T00:00:00",
        finished_at="2026-01-01T00:00:05",
        duration_seconds=5.0,
        results=[result],
    )


def test_save_and_retrieve_scan(tmp_path):
    db = DatabaseManager(db_path=tmp_path / "test.db")
    scan_id = db.save_scan(_sample_summary(), scan_type="full")

    record = db.get_scan(scan_id)
    assert record is not None
    assert len(record.findings) == 1
    assert record.findings[0].title == "Disk Encryption"


def test_list_scans_orders_newest_first(tmp_path):
    db = DatabaseManager(db_path=tmp_path / "test.db")
    first_id = db.save_scan(_sample_summary())
    second_id = db.save_scan(_sample_summary())

    scans = db.list_scans()
    assert scans[0].id == second_id
    assert scans[1].id == first_id


def test_finding_round_trips_to_audit_result(tmp_path):
    db = DatabaseManager(db_path=tmp_path / "test.db")
    db.save_scan(_sample_summary())
    latest = db.get_latest_scan()
    result = db.finding_to_audit_result(latest.findings[0])
    assert result.severity == Severity.CRITICAL
    assert result.status == AuditStatus.COMPLETED
