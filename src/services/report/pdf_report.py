"""
SecureAudit
PDF Report Exporter

Author: Humair Ali
"""

from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors as rl_colors
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from src.config.settings import settings
from src.core.audit_engine import ScanSummary
from src.models.audit_result import Severity

_SEVERITY_COLOR = {
    Severity.INFO.value: rl_colors.HexColor("#3B82F6"),
    Severity.LOW.value: rl_colors.HexColor("#22C55E"),
    Severity.MEDIUM.value: rl_colors.HexColor("#F59E0B"),
    Severity.HIGH.value: rl_colors.HexColor("#EF4444"),
    Severity.CRITICAL.value: rl_colors.HexColor("#991B1B"),
}


def export_pdf(summary: ScanSummary, output_path: Path | str) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(str(path), pagesize=LETTER, title=f"{settings.APP_NAME} Report")
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "SecureAuditTitle", parent=styles["Title"], textColor=rl_colors.HexColor("#111827")
    )
    heading_style = ParagraphStyle(
        "SecureAuditHeading", parent=styles["Heading2"], textColor=rl_colors.HexColor("#1F2937")
    )
    body_style = styles["BodyText"]

    story = [
        Paragraph(f"{settings.APP_NAME} Security Assessment Report", title_style),
        Spacer(1, 6),
        Paragraph(
            f"Scan window: {summary.started_at} &rarr; {summary.finished_at} "
            f"({summary.duration_seconds}s)",
            body_style,
        ),
        Spacer(1, 12),
        Paragraph("Executive Summary", heading_style),
        Paragraph(
            f"Overall security score: <b>{summary.security_score}/100</b>. "
            f"{len(summary.results)} check(s) were performed; "
            f"{summary.failed_count} could not be completed.",
            body_style,
        ),
        Spacer(1, 12),
        Paragraph("Findings", heading_style),
    ]

    table_data = [["Title", "Category", "Severity", "CVSS", "Recommendation"]]
    row_colors = [rl_colors.white]
    for result in summary.results:
        table_data.append(
            [
                Paragraph(result.title, body_style),
                Paragraph(result.category, body_style),
                Paragraph(result.severity.value, body_style),
                str(result.cvss or "-"),
                Paragraph(result.recommendation, body_style),
            ]
        )
        row_colors.append(_SEVERITY_COLOR.get(result.severity.value, rl_colors.white))

    table = Table(table_data, colWidths=[1.3 * inch, 1.1 * inch, 0.9 * inch, 0.6 * inch, 2.4 * inch])
    style_commands = [
        ("BACKGROUND", (0, 0), (-1, 0), rl_colors.HexColor("#111827")),
        ("TEXTCOLOR", (0, 0), (-1, 0), rl_colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, rl_colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]
    for row_index, color in enumerate(row_colors[1:], start=1):
        style_commands.append(("BACKGROUND", (2, row_index), (2, row_index), color))
    table.setStyle(TableStyle(style_commands))

    story.append(table)
    doc.build(story)
    return path
