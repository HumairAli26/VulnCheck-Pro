# Changelog

All notable changes to SecureAudit are documented here.
Format loosely follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

> Note: `pyproject.toml` currently reports `0.2.0`. The entries below cover
> everything built since that version was set — bump it to `0.4.0` (or
> later) to match this changelog before your next release/commit.

## [0.4.0] – Process-Level Auditing

### Added
- **Full-range port scan (1–65,535)** replacing the previous fixed 22-port watchlist, using a concurrent thread pool (~3–5s on localhost).
- **Banner grabbing** for open ports that announce themselves unprompted (SSH/FTP/SMTP-style greetings).
- **Auth-less exposure probing** for Redis and Memcached — sends a single read-only liveness command (`PING`, `version`) to detect services running with zero authentication, a real and historically common misconfiguration.
- **Process attribution**: open ports are now cross-referenced against `psutil` to show the actual PID, process name, and owning user, not just "port is open."
- **New audit: Running Processes** (`Endpoint Security` category) — flags processes running from a deleted executable file, a known malware evasion technique (MITRE ATT&CK T1070.004).
- **New page: Process Explorer** — a live, sortable, filterable table of every running process (PID, user, CPU%, memory%, status, executable path), with suspicious rows highlighted.
- Fine-grained progress reporting: `BaseAudit.set_progress_callback()` lets long-running audits (like the port scan) stream sub-progress into the UI/CLI without changing the engine's per-audit contract.

### Fixed
- A silent bug where several `threat=(...)` tuples in the port threat catalog had a trailing comma, turning the string into a 1-element tuple.

## [0.3.0] – Guided Remediation & GUI Polish

### Added
- **Remediation knowledge base** (`src/services/remediation/`): OS-aware, numbered fix steps for every finding, plus an explicit "what could happen if this isn't fixed" threat explanation.
- **Per-port threat catalog** (22 services: FTP, SSH, Telnet, SMTP, DNS, rpcbind, RPC, NetBIOS, IMAP, SMB, MSSQL, Oracle, NFS, MySQL, RDP, PostgreSQL, VNC, Redis, HTTP-Alt, Elasticsearch, Memcached, MongoDB) with real, cited threats and OS-specific closing commands.
- **Remediation dialog** ("View Fix Steps" button on every non-informational finding) with a threat panel, numbered steps, estimated time, restart warning, and a Copy Steps button.
- **New audit: Screen Lock** (`Endpoint Security` category) — checks GNOME (`gsettings`), Windows registry, and macOS (`defaults`) auto-lock settings.
- Window now opens maximized.
- Fixed a global-stylesheet bug where every `QLabel` inherited an opaque background from the app-wide `QWidget` rule, showing a mismatched rectangle behind text on colored cards.
- `InfoCard` redesigned: centered/bold headings, drop-shadow depth instead of a visible border line, hover state.
- Dashboard grid stretches to fill the maximized window; page margins increased; dark-themed scrollbars.

## [0.2.0] – Full Rebuild

### Added
- Clean-architecture rewrite: `providers` (OS-specific implementations) → `audits` (what to check) → `models`/`core` (domain) → `ui` (presentation).
- Real audits: System Information, Firewall Status, Disk Encryption, Automatic Updates, Open Ports (original 7-port watchlist).
- `AuditEngine` with severity-weighted scoring (0–100) and per-audit crash isolation.
- SQLite persistence via SQLAlchemy (`ScanRecord`, `FindingRecord`).
- PDF/JSON/CSV report generation.
- Full PySide6 GUI: Dashboard, Scan (background `QThread`), Reports, History, Settings, About.
- CLI (`cli.py`) for headless scans and history.
- 15 initial pytest tests.
- Fixed a UTF-16-encoded `requirements.txt`, an empty `LICENSE`, and removed dead prototype code.

## [0.1.0] – Initial Scaffold

- Original project skeleton: folder structure, `AuditResult` model, `PlatformDetector`, dashboard UI shell with placeholder data, one working audit (System Information), no audit registered with the engine.