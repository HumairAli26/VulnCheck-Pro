"""
SecureAudit
Database Manager

Author: Humair Ali
"""

from __future__ import annotations

import json
from pathlib import Path

from sqlalchemy import Column, Float, ForeignKey, Integer, String, Text, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, joinedload, relationship, sessionmaker

from src.core.audit_engine import ScanSummary
from src.models.audit_result import AuditResult, AuditStatus, Severity

_DB_DIR = Path(__file__).resolve().parents[3] / "database"
_DB_DIR.mkdir(exist_ok=True)
_DEFAULT_DB_PATH = _DB_DIR / "secureaudit.db"


class Base(DeclarativeBase):
    pass


class ScanRecord(Base):
    """One row per full/quick scan run."""

    __tablename__ = "scans"

    id = Column(Integer, primary_key=True, autoincrement=True)
    started_at = Column(String, nullable=False)
    finished_at = Column(String, nullable=False)
    duration_seconds = Column(Float, nullable=False)
    security_score = Column(Integer, nullable=False)
    scan_type = Column(String, nullable=False, default="full")

    findings = relationship(
        "FindingRecord", back_populates="scan", cascade="all, delete-orphan"
    )


class FindingRecord(Base):
    """One row per audit result within a scan."""

    __tablename__ = "findings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    scan_id = Column(Integer, ForeignKey("scans.id"), nullable=False)
    title = Column(String, nullable=False)
    category = Column(String, nullable=False)
    status = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    recommendation = Column(Text, nullable=False)
    details_json = Column(Text, nullable=False, default="{}")
    cvss = Column(Float, nullable=False, default=0.0)
    references_json = Column(Text, nullable=False, default="[]")
    compliance_json = Column(Text, nullable=False, default="[]")
    timestamp = Column(String, nullable=False)

    scan = relationship("ScanRecord", back_populates="findings")


class DatabaseManager:
    """Thin façade around a SQLAlchemy session factory for scan history."""

    def __init__(self, db_path: Path | str = _DEFAULT_DB_PATH) -> None:
        self._engine = create_engine(f"sqlite:///{db_path}", echo=False)
        Base.metadata.create_all(self._engine)
        self._session_factory: sessionmaker[Session] = sessionmaker(
            bind=self._engine, expire_on_commit=False
        )

    def save_scan(self, summary: ScanSummary, scan_type: str = "full") -> int:
        """Persist a ScanSummary and return the new scan's id."""
        with self._session_factory() as session:
            scan = ScanRecord(
                started_at=summary.started_at,
                finished_at=summary.finished_at,
                duration_seconds=summary.duration_seconds,
                security_score=summary.security_score,
                scan_type=scan_type,
            )
            for result in summary.results:
                scan.findings.append(
                    FindingRecord(
                        title=result.title,
                        category=result.category,
                        status=result.status.value,
                        severity=result.severity.value,
                        description=result.description,
                        recommendation=result.recommendation,
                        details_json=json.dumps(result.details),
                        cvss=result.cvss,
                        references_json=json.dumps(result.references),
                        compliance_json=json.dumps(result.compliance),
                        timestamp=result.timestamp,
                    )
                )
            session.add(scan)
            session.commit()
            return scan.id

    def list_scans(self, limit: int = 50) -> list[ScanRecord]:
        with self._session_factory() as session:
            return (
                session.query(ScanRecord)
                .options(joinedload(ScanRecord.findings))
                .order_by(ScanRecord.id.desc())
                .limit(limit)
                .all()
            )

    def get_scan(self, scan_id: int) -> ScanRecord | None:
        with self._session_factory() as session:
            return (
                session.query(ScanRecord)
                .options(joinedload(ScanRecord.findings))
                .filter(ScanRecord.id == scan_id)
                .one_or_none()
            )

    def get_latest_scan(self) -> ScanRecord | None:
        with self._session_factory() as session:
            return (
                session.query(ScanRecord)
                .options(joinedload(ScanRecord.findings))
                .order_by(ScanRecord.id.desc())
                .first()
            )

    @staticmethod
    def finding_to_audit_result(finding: FindingRecord) -> AuditResult:
        """Rehydrate a stored FindingRecord back into an AuditResult."""
        return AuditResult(
            title=finding.title,
            category=finding.category,
            status=AuditStatus(finding.status),
            severity=Severity(finding.severity),
            description=finding.description,
            recommendation=finding.recommendation,
            details=json.loads(finding.details_json),
            cvss=finding.cvss,
            references=json.loads(finding.references_json),
            compliance=json.loads(finding.compliance_json),
            timestamp=finding.timestamp,
        )


database_manager = DatabaseManager()
