import json

from src.core.audit_engine import ScanSummary
from src.models.audit_result import AuditResult, AuditStatus, Severity
from src.services.report.csv_report import export_csv
from src.services.report.json_report import export_json
from src.services.report.pdf_report import export_pdf


def _sample_summary() -> ScanSummary:
    result = AuditResult(
        title="Firewall Status",
        category="Network",
        status=AuditStatus.COMPLETED,
        severity=Severity.HIGH,
        description="Firewall disabled",
        recommendation="Enable it",
        cvss=7.5,
        compliance=["CIS Control 4"],
    )
    return ScanSummary(
        started_at="2026-01-01T00:00:00",
        finished_at="2026-01-01T00:00:05",
        duration_seconds=5.0,
        results=[result],
    )


def test_export_json_round_trips(tmp_path):
    path = export_json(_sample_summary(), tmp_path / "report.json")
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["security_score"] == 100 - Severity.HIGH.weight
    assert data["findings"][0]["title"] == "Firewall Status"


def test_export_csv_contains_header_and_row(tmp_path):
    path = export_csv(_sample_summary(), tmp_path / "report.csv")
    content = path.read_text(encoding="utf-8")
    assert "title" in content.splitlines()[0]
    assert "Firewall Status" in content


def test_export_pdf_produces_a_file(tmp_path):
    path = export_pdf(_sample_summary(), tmp_path / "report.pdf")
    assert path.exists()
    assert path.stat().st_size > 0
