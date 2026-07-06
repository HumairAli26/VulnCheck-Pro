"""
SecureAudit
Report Service

Author: Humair Ali
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from src.config.settings import settings
from src.core.audit_engine import ScanSummary
from src.services.report.csv_report import export_csv
from src.services.report.json_report import export_json
from src.services.report.pdf_report import export_pdf

_EXPORTERS = {
    "pdf": (export_pdf, "pdf"),
    "json": (export_json, "json"),
    "csv": (export_csv, "csv"),
}


def generate_report(
    summary: ScanSummary, fmt: str, output_dir: Path | str | None = None
) -> Path:
    """Generate a report in the requested format ('pdf', 'json', or 'csv')."""
    fmt = fmt.lower()
    if fmt not in _EXPORTERS:
        raise ValueError(f"Unsupported report format: {fmt}")

    exporter, extension = _EXPORTERS[fmt]
    directory = Path(output_dir) if output_dir else Path(settings.EXPORT_FOLDER)
    directory.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"SecureAudit_Report_{timestamp}.{extension}"
    return exporter(summary, directory / filename)
