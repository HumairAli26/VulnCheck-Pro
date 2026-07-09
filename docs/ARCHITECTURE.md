# Architecture

## Layering
Presentation   src/ui/            PySide6 pages, widgets, navigation
↓
Application    src/audits/        BaseAudit subclasses — know what to check
↓
Domain         src/models/        AuditResult, Severity, AuditStatus
src/core/          AuditEngine, ScanSummary, ScanWorker
↓
Infrastructure src/providers/     OS-specific implementations — know how

Dependencies only point downward. `src/ui` depends on `src/audits`, never
the reverse; `src/audits` depends on `src/providers` via an abstract
interface, never a concrete OS-specific class directly.

## The provider pattern, and why it exists

Every audit needs to answer an OS-specific question ("is the firewall on?")
using an OS-specific mechanism (`netsh` vs `ufw` vs `socketfilterfw`). If
`FirewallAudit` contained `if platform == "Windows": ... elif ...`, every
audit would accumulate three code paths and testing would require three
real operating systems just to touch one file.

Instead:

- `src/providers/base.py` defines abstract interfaces
  (`FirewallProvider`, `EncryptionProvider`, `UpdateProvider`,
  `ScreenLockProvider`, `SystemProvider`) plus small `@dataclass` result
  types (`FirewallStatus`, `EncryptionStatus`, ...).
- `src/providers/windows/`, `src/providers/linux/`, `src/providers/macos/`
  each implement every interface using that OS's native tools.
- `src/providers/factory.py` has one function per interface
  (`get_firewall_provider()`, etc.) that inspects
  `PlatformDetector.current()` and returns the right concrete
  implementation.
- Audits only ever call the factory, e.g.:

```python
  provider = get_firewall_provider()
  status = provider.get_status()
```

  This is why `FirewallAudit` is ~40 lines regardless of which of three
  very different OS APIs sits behind it.

**Rule enforced throughout the codebase:** audits never call `subprocess`
directly. All shelling-out lives in providers. This keeps audits
unit-testable with a fake provider and keeps the "this touches the OS"
surface area auditable in one place.

## AuditEngine and BaseAudit

`BaseAudit` (`src/audits/base.py`) is the contract every check implements:

```python
class BaseAudit(ABC):
    name: str
    category: str

    def set_progress_callback(self, callback): ...  # optional, no-op by default
    @abstractmethod
    def run(self) -> AuditResult: ...
```

`AuditEngine` (`src/core/audit_engine.py`) runs a list of audits and
produces a `ScanSummary`. Two properties matter:

1. **Per-audit crash isolation.** If `audit.run()` raises, the engine
   catches it, logs it, and synthesizes a `FAILED` `AuditResult` instead of
   letting one broken check take down the whole scan. This is a hard
   guarantee, covered by `tests/test_audit_engine.py`.
2. **Fine-grained progress.** Some audits (notably the full 65,535-port
   scan) take several seconds and shouldn't leave the UI looking frozen at
   "[5/7] Open Ports" the whole time. `BaseAudit.set_progress_callback()`
   lets an audit report its own internal `(done, total)` progress. The
   engine's own per-audit `progress_callback` and an audit's internal
   fine-grained callback are two independent channels — see
   `src/core/scan_worker.py` for how the UI tells them apart (a
   `(0, 0, text)` tuple from the fine-grained channel is a sentinel meaning
   "update the status text only, don't move the progress bar").

## Data flow of a scan
ScanPage._start_scan()
→ ScanWorker(audits).start()          # QThread, keeps UI responsive
→ AuditEngine.run()
→ for each audit: audit.run() → AuditResult
→ emits finished_scan(ScanSummary)
→ ScanPage._on_finished()
→ database_manager.save_scan(summary)      # persists to SQLite
→ emits scan_completed(summary)
→ MainWindow relays to DashboardPage.refresh(summary)
→ MainWindow relays to ReportsPage.refresh() / HistoryPage.refresh()

Everything downstream of `finished_scan` runs on the main/UI thread; only
`AuditEngine.run()` itself executes on the worker thread.

## Database schema

Two SQLAlchemy models in `src/services/database/db_manager.py`:

- `ScanRecord` — one row per scan (timestamps, duration, `security_score`,
  `scan_type`).
- `FindingRecord` — one row per `AuditResult` within a scan, with a
  many-to-one back to `ScanRecord`. Fields that aren't natively
  SQL-friendly (`details`, `references`, `compliance`) are stored as JSON
  strings and rehydrated via `DatabaseManager.finding_to_audit_result()`.

`DatabaseManager` uses `expire_on_commit=False` and `joinedload` on all
read queries specifically so that `ScanRecord.findings` remains accessible
after the session closes — a common SQLAlchemy footgun that would
otherwise raise `DetachedInstanceError` the moment the UI touches a
record outside its original session.

## Remediation lookup chain

`get_remediation(result: AuditResult) -> RemediationGuide`
(`src/services/remediation/remediation_guide.py`) resolves in this order:

1. **Open Ports special case**: if `result.title == "Open Ports"` and it
   has per-port `details`, build a combined guide — one threat paragraph
   and one set of fix steps *per open port found*, pulling from
   `port_threats.py`'s 22-service catalog.
2. **`(title, platform)` exact match** in `_GUIDES` — the common case for
   Firewall/Disk Encryption/Updates/Screen Lock/Running Processes, since
   the fix genuinely differs by OS.
3. **Title-only match** in `_GENERIC_GUIDES` — for findings whose fix is
   OS-independent.
4. **Fallback**: a single-step guide built from the finding's own
   `description`/`recommendation`, so the dialog is never empty even for
   an audit nobody's written a dedicated guide for yet.

## Threading & Qt specifics

- `ScanWorker(QThread)` is the only place `AuditEngine.run()` is invoked
  from the GUI. Its signals (`progress`, `finished_scan`) cross from the
  worker thread to the main thread via Qt's queued-connection mechanism —
  this is why tests that drive a real scan in the GUI need to
  `app.processEvents()` in a loop rather than checking state immediately
  after `worker.isRunning()` goes `False` (the emitted signal can still be
  queued for delivery at that instant).
- The CLI (`cli.py`) does not use `ScanWorker` at all — it drives
  `AuditEngine` directly and synchronously, since there's no UI thread to
  protect.

## Where to look when extending this

| I want to...                                | Start here |
|----------------------------------------------|------------|
| Add a new OS-aware check                     | `CONTRIBUTING.md` → "Adding a new audit" |
| Change how findings are scored                | `Severity.weight` in `src/models/audit_result.py` |
| Add a new report format                       | `src/services/report/` |
| Add a new remediation guide                   | `src/services/remediation/remediation_guide.py` |
| Add a new Dashboard card                      | `DashboardPage` in `src/ui/pages/dashboard.py` |
| Change what appears in Quick vs Full scan      | `src/audits/registry.py` |