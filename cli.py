"""
SecureAudit
Command-Line Interface

Author: Humair Ali

Usage:
    python cli.py scan --type quick
    python cli.py scan --type full --report pdf
    python cli.py history
"""

from __future__ import annotations

import argparse
import sys

from src.audits.registry import build_full_scan, build_quick_scan
from src.core.audit_engine import AuditEngine
from src.services.database.db_manager import database_manager
from src.services.report.report_service import generate_report


def cmd_scan(args: argparse.Namespace) -> int:
    audits = build_quick_scan() if args.type == "quick" else build_full_scan()
    engine = AuditEngine()
    engine.register_all(audits)

    def on_progress(done: int, total: int, name: str) -> None:
        print(f"[{done}/{total}] {name}")

    for audit in audits:
        audit_name = getattr(audit, "name", audit.__class__.__name__)
        audit.set_progress_callback(
            lambda done, total, n=audit_name: print(f"    {n}: {done:,}/{total:,}", end="\r")
        )

    summary = engine.run(progress_callback=on_progress)
    print()

    print("-" * 60)
    print(f"Security score: {summary.security_score}/100")
    print(f"Findings: {len(summary.results)}  (failed: {summary.failed_count})")
    for result in summary.results:
        print(f"  [{result.severity.value:>13}] {result.title} — {result.category}")

    database_manager.save_scan(summary, scan_type=args.type)

    if args.report:
        path = generate_report(summary, args.report)
        print(f"\nReport saved to: {path}")

    return 0


def cmd_history(args: argparse.Namespace) -> int:
    scans = database_manager.list_scans(limit=args.limit)
    if not scans:
        print("No scans recorded yet.")
        return 0
    for scan in scans:
        print(
            f"#{scan.id}  {scan.finished_at}  type={scan.scan_type}  "
            f"score={scan.security_score}/100  findings={len(scan.findings)}"
        )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="secureaudit", description="SecureAudit CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan_parser = subparsers.add_parser("scan", help="Run a security scan")
    scan_parser.add_argument("--type", choices=["quick", "full"], default="full")
    scan_parser.add_argument(
        "--report", choices=["pdf", "json", "csv"], default=None,
        help="Also generate a report in this format",
    )
    scan_parser.set_defaults(func=cmd_scan)

    history_parser = subparsers.add_parser("history", help="List past scans")
    history_parser.add_argument("--limit", type=int, default=20)
    history_parser.set_defaults(func=cmd_history)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
