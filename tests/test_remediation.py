from src.models.audit_result import AuditResult, AuditStatus, Severity
from src.services.remediation.remediation_guide import get_remediation


def _finding(title: str, category: str = "Network") -> AuditResult:
    return AuditResult(
        title=title,
        category=category,
        status=AuditStatus.COMPLETED,
        severity=Severity.HIGH,
        description="desc",
        recommendation="Do the thing.",
    )


def test_known_finding_returns_multiple_concrete_steps():
    guide = get_remediation(_finding("Firewall Status"))
    assert len(guide.steps) >= 2


def test_generic_finding_falls_back_to_title_lookup():
    guide = get_remediation(_finding("Open Ports"))
    assert len(guide.steps) >= 2


def test_unknown_finding_falls_back_to_its_own_recommendation():
    result = _finding("Some Brand New Check Nobody Wrote a Guide For")
    guide = get_remediation(result)
    assert guide.steps == [result.recommendation]
