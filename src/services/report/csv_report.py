"""
SecureAudit
CSV Report Exporter

Author: Humair Ali
"""

from __future__ import annotations

import csv
from pathlib import Path

from src.core.audit_engine import ScanSummary

_FIELDS = [
    "title",
    "category",
    "status",
    "severity",
    "risk_score",
    "cvss",
    "description",
    "recommendation",
    "compliance",
    "timestamp",
]


def export_csv(summary: ScanSummary, output_path: Path | str) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=_FIELDS)
        writer.writeheader()
        for result in summary.results:
            row = result.to_dict()
            row["compliance"] = "; ".join(row["compliance"])
            writer.writerow({field: row.get(field, "") for field in _FIELDS})

    return path
