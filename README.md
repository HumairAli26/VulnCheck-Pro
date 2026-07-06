# SecureAudit

A cross-platform desktop application that audits a device's **defensive** security posture — firewall, disk encryption, patch status, and exposed network ports — and turns the results into a scored dashboard and shareable PDF/JSON/CSV reports.

SecureAudit does **not** perform penetration testing or exploit anything. It answers a narrower, more common question: *"Is this machine configured the way a security-conscious admin would want it to be?"*

## Features

- **Clean architecture.** UI, audit logic, OS-specific providers, persistence, and reporting are separate layers with no circular dependencies. Adding a new check is a one-line registration, not a rewrite.
- **Cross-platform provider layer.** Every audit talks to an abstract interface (`FirewallProvider`, `EncryptionProvider`, `UpdateProvider`, `SystemProvider`); Windows, Linux, and macOS each implement it using the tools native to that OS (`netsh`/`manage-bde`, `ufw`/`lsblk`/`apt`, `socketfilterfw`/`fdesetup`/`softwareupdate`).
- **Real audits, not mocked data:**
  - System Information
  - Firewall Status
  - Disk Encryption (BitLocker / FileVault / LUKS)
  - Automatic Updates
  - Open Ports (common risky services: FTP, Telnet, SMB, RDP, VNC, RPC)
- **Scoring.** Every finding has a severity (Informational → Critical) that maps to a point penalty; the aggregate becomes a single 0–100 security score.
- **Persistent history.** Every scan and finding is stored in SQLite via SQLAlchemy, so trends are visible over time.
- **Reporting.** One-click PDF (ReportLab), JSON, and CSV export from any past scan.
- **Responsive UI.** Scans run on a background `QThread` with live progress, so the interface never freezes.
- **CLI.** Everything the GUI can do is also available headlessly for scripting or CI: `python cli.py scan --type full --report pdf`.
- **Fault-tolerant by design.** A crashing or permission-denied audit never takes down a scan — it's caught, logged, and reported as a "Failed" finding instead.

## Architecture

```
Presentation (src/ui)          — PySide6 pages, widgets, navigation
        ↓
Application (src/audits)       — BaseAudit subclasses; know *what* to check
        ↓
Domain (src/models, src/core)  — AuditResult, Severity, AuditEngine, ScanSummary
        ↓
Infrastructure (src/providers) — OS-specific implementations; know *how* to check
```

Audits never call `subprocess` directly — they ask `src/providers/factory.py` for the right provider, and it returns whichever concrete implementation matches `PlatformDetector.current()`. This is what lets `FirewallAudit` be a five-line class regardless of which of three very different OS APIs is behind it.

## Project structure

```
SecureAudit/
├── app.py                     # GUI entry point
├── cli.py                     # Headless CLI entry point
├── src/
│   ├── config/                 # colors, fonts, settings, theme, user_config
│   ├── core/                   # audit_engine, scan_worker, logger, platform detection
│   ├── models/                 # AuditResult / Severity / AuditStatus
│   ├── providers/               # base interfaces + windows/linux/macos implementations
│   ├── audits/                  # one file per check + the registry
│   ├── services/
│   │   ├── database/            # SQLAlchemy models + DatabaseManager
│   │   └── report/               # PDF / JSON / CSV exporters
│   └── ui/
│       ├── main_window.py
│       ├── navigation/           # sidebar, nav buttons
│       ├── pages/                 # dashboard, scan, reports, history, settings, about
│       └── widgets/                # info_card, progress_ring, finding_card, risk_badge...
├── tests/                       # pytest suite (engine, models, db, reports, providers)
├── database/                    # secureaudit.db (created at runtime)
├── reports/                      # generated PDF/JSON/CSV (created at runtime)
└── logs/                         # secureaudit.log (created at runtime)
```

## Getting started

```bash
pip install -r requirements.txt

# Launch the desktop app
python app.py

# Or use the CLI
python cli.py scan --type quick
python cli.py scan --type full --report pdf
python cli.py history
```

Some checks (BitLocker on Windows, encryption/firewall state on macOS/Linux) return more accurate results when run with administrator/root privileges; SecureAudit degrades gracefully and reports "could not determine" rather than guessing when it lacks permission.

## Running the tests

```bash
pip install -r requirements.txt pytest
pytest
```

The suite covers the audit engine's exception-safety guarantee, the severity → score math, database round-tripping, and report generation (PDF/JSON/CSV). It does not require a display and runs the same on Linux, macOS, or Windows CI.

## Compliance mapping

Findings that represent a real gap are tagged with the relevant control(s) where applicable, e.g. `CIS Control 3` (disk encryption), `CIS Control 4` (firewall/network), `CIS Control 7` (patch management), and `NIST 800-53 SC-28`. This is intentionally lightweight rather than a full CIS-CAT/OpenSCAP-style benchmark — see **Roadmap** below.

## Roadmap

This is a working, extensible core rather than a finished "enterprise suite." Natural next additions, following the same provider pattern:

- More audits: password policy, screen lock, administrator/guest accounts, startup programs, running services, USB device control, browser security, Wi-Fi security, SSH/RDP configuration
- Full CIS Controls v8 / NIST CSF / ISO 27001 mapping per finding
- Scheduled/background scans
- HTML report export
- A plugin system for third-party audits
- Packaging via PyInstaller for one-click Windows/macOS/Linux installers

## License

MIT — see `LICENSE`.
