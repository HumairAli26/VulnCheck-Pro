from src.audits.base import BaseAudit
from src.core.audit_engine import AuditEngine
from src.models.audit_result import AuditResult, AuditStatus, Severity


class _AlwaysPassAudit(BaseAudit):
    name = "Always Pass"
    category = "Test"

    def run(self) -> AuditResult:
        return AuditResult(
            title=self.name,
            category=self.category,
            status=AuditStatus.COMPLETED,
            severity=Severity.INFO,
            description="ok",
            recommendation="none",
        )


class _AlwaysCriticalAudit(BaseAudit):
    name = "Always Critical"
    category = "Test"

    def run(self) -> AuditResult:
        return AuditResult(
            title=self.name,
            category=self.category,
            status=AuditStatus.COMPLETED,
            severity=Severity.CRITICAL,
            description="bad",
            recommendation="fix",
        )


class _AlwaysCrashesAudit(BaseAudit):
    name = "Always Crashes"
    category = "Test"

    def run(self) -> AuditResult:
        raise RuntimeError("simulated failure")


def test_engine_runs_all_registered_audits():
    engine = AuditEngine()
    engine.register_all([_AlwaysPassAudit(), _AlwaysCriticalAudit()])
    summary = engine.run()
    assert len(summary.results) == 2


def test_engine_security_score_drops_with_severity():
    engine = AuditEngine()
    engine.register(_AlwaysCriticalAudit())
    summary = engine.run()
    assert summary.security_score == 100 - Severity.CRITICAL.weight


def test_engine_never_crashes_on_a_faulty_audit():
    engine = AuditEngine()
    engine.register(_AlwaysCrashesAudit())
    summary = engine.run()
    assert len(summary.results) == 1
    assert summary.results[0].status == AuditStatus.FAILED


def test_progress_callback_is_invoked_per_audit():
    calls = []
    engine = AuditEngine()
    engine.register_all([_AlwaysPassAudit(), _AlwaysCriticalAudit()])
    engine.run(progress_callback=lambda done, total, name: calls.append((done, total, name)))
    assert calls == [(1, 2, "Always Pass"), (2, 2, "Always Critical")]
