from src.models.audit_result import AuditResult, AuditStatus, Severity


def test_severity_weights_increase_with_risk():
    assert Severity.INFO.weight < Severity.LOW.weight
    assert Severity.LOW.weight < Severity.MEDIUM.weight
    assert Severity.MEDIUM.weight < Severity.HIGH.weight
    assert Severity.HIGH.weight < Severity.CRITICAL.weight


def test_audit_result_risk_alias_matches_severity():
    result = AuditResult(
        title="Test",
        category="General",
        status=AuditStatus.COMPLETED,
        severity=Severity.HIGH,
        description="desc",
        recommendation="fix it",
    )
    assert result.risk == "High"
    assert result.risk_score == Severity.HIGH.weight


def test_audit_result_to_dict_is_json_safe():
    result = AuditResult(
        title="Test",
        category="General",
        status=AuditStatus.COMPLETED,
        severity=Severity.LOW,
        description="desc",
        recommendation="fix it",
        references=["https://example.com"],
        compliance=["CIS Control 1"],
    )
    payload = result.to_dict()
    assert payload["severity"] == "Low"
    assert payload["status"] == "Completed"
    assert payload["references"] == ["https://example.com"]
    assert payload["compliance"] == ["CIS Control 1"]
