# Contributing to SecureAudit

Thanks for considering a contribution. This is a defensive security posture
auditor — contributions that help people find and fix misconfigurations on
their own machines are welcome. Contributions aimed at exploitation,
credential harvesting, or offensive tooling are not in scope for this
project.

## Getting set up

```bash
git clone <your-fork-url>
cd SecureAudit
pip install -r requirements.txt
pip install pytest black ruff mypy   # dev tools
pytest
```

All tests should pass on a clean checkout before you start. If they don't,
open an issue rather than working around it.

## Project layout

See `docs/ARCHITECTURE.md` for the full explanation. The short version:

src/providers/   -- OS-specific "how" (Windows/Linux/macOS implementations)
src/audits/      -- cross-platform "what" (one file per check)
src/models/      -- AuditResult, Severity, AuditStatus
src/core/        -- AuditEngine, ScanWorker, logging, platform detection
src/services/    -- database, report generation, remediation knowledge base
src/ui/          -- PySide6 pages, widgets, navigation

## Adding a new audit

This is the most common type of contribution, so here's the exact recipe:

1. **If it needs OS-specific data collection**, add a `XStatus` dataclass and
   `XProvider` abstract class to `src/providers/base.py`, then implement it
   in `src/providers/windows/`, `src/providers/linux/`, and
   `src/providers/macos/`. Register it in `src/providers/factory.py`.
2. **Add the audit itself** in `src/audits/your_check_audit.py`, subclassing
   `BaseAudit`. It should call the provider (via the factory), never
   `subprocess` directly.
3. **Register it** in `src/audits/registry.py` under `QUICK_SCAN_AUDITS`
   and/or `FULL_SCAN_AUDITS`.
4. **Add a remediation guide** in
   `src/services/remediation/remediation_guide.py` — a `threat` explanation
   and per-platform `steps`, keyed by `(your_audit.name, Platform.X)`.
5. **Write tests.** At minimum: the audit runs without raising, and (if
   platform-testable in CI) returns a sane result. See
   `tests/test_audit_engine.py` for the pattern of testing against a fake
   `BaseAudit` subclass if you can't exercise the real OS behavior in CI.
6. If the new audit's category should show its own Dashboard card, see
   `DashboardPage._update_category_card` / `_update_single_result_card` in
   `src/ui/pages/dashboard.py`.

## Code style

- **Formatting**: `black` (line length 88, configured in `pyproject.toml`).
- **Linting**: `ruff` (same line length).
- **Type checking**: `mypy` is configured as an optional dev dependency;
  type hints are expected on new code but the codebase isn't 100% strict yet.
- Every new module should have a module-level docstring in the existing
  style: `SecureAudit` / short title / `Author: <you>`.
- No hardcoded colors/fonts/strings where `src/config` already has the
  right constant — add one if it doesn't.

## Testing expectations

- Run `pytest` before opening a PR. All existing tests must still pass.
- Anything that shells out to the OS (a new provider) should be written so
  it **fails gracefully** (returns an `error` field) rather than raising —
  this is a strict requirement, since a broken audit must never take down
  a whole scan. `AuditEngine.run()` also catches exceptions defensively as
  a second line of defense, but providers/audits shouldn't rely on that.
- If you can't execute-test a Windows/macOS-only code path (e.g. you're on
  Linux), say so explicitly in your PR description rather than claiming
  it's verified. The existing codebase is honest about this in several
  places — keep that going.

## Pull requests

- Keep PRs focused on one audit/feature/fix at a time.
- Update `CHANGELOG.md` under an `[Unreleased]` heading.
- If your change affects installation or usage, update `INSTALL.md` /
  `USER_GUIDE.md` accordingly.

## Reporting bugs vs. reporting vulnerabilities

Regular bugs (a check giving a wrong result, a UI glitch, a crash): open a
normal GitHub issue.

If you've found something that could let SecureAudit itself be used
maliciously (e.g. a way to make it execute arbitrary commands), see
`SECURITY.md` instead — please don't open a public issue for that.