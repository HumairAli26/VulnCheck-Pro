"""
SecureAudit
JSON Report Exporter

Author: Humair Ali
"""

from __future__ import annotations

import json
from pathlib import Path

from src.core.audit_engine import ScanSummary


def export_json(summary: ScanSummary, output_path: Path | str) -> Path:
    payload = {
        "started_at": summary.started_at,
        "finished_at": summary.finished_at,
        "duration_seconds": summary.duration_seconds,
        "security_score": summary.security_score,
        "risk_distribution": summary.risk_distribution,
        "findings": [result.to_dict() for result in summary.results],
    }
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path
