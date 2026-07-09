# Installation

## Requirements

- **Python 3.11+**
- Windows 10/11, a modern Linux distribution, or macOS 12+
- Some checks (BitLocker on Windows, certain firewall/encryption reads on
  Linux/macOS) are more accurate run with administrator/root privileges,
  though the app works without them.

## 1. Get the code

```bash
git clone <your-repo-url>
cd SecureAudit
```

## 2. Install dependencies

```bash
pip install -r requirements.txt
```

This installs:

| Package     | Purpose |
|-------------|---------|
| PySide6     | Desktop GUI (Qt for Python) |
| SQLAlchemy  | Scan history persistence (SQLite) |
| reportlab   | PDF report generation |
| loguru      | Application logging |
| psutil      | Process/connection introspection |
| pytest      | Test suite (optional at runtime, needed to run tests) |

If you only want to run the CLI (no GUI), you can skip `PySide6` — but
`cli.py` currently imports from modules that don't require it, so the
full `requirements.txt` install is the simplest path.

## 3. Run it

**Desktop app:**

```bash
python app.py
```

The window opens maximized. First launch has no scan history — go to the
**Scan** page and run a Quick or Full scan.

**CLI (no GUI required):**

```bash
python cli.py scan --type full --report pdf
python cli.py history
```

## Platform-specific notes

### Windows
- Run from an elevated (Administrator) Command Prompt/PowerShell for
  accurate BitLocker and some firewall results. Without elevation, those
  checks report "could not determine" rather than a wrong answer.
- If PySide6 fails to launch with a "could not find or load the Qt
  platform plugin" error, reinstall PySide6:
  `pip install --force-reinstall PySide6`.

### Linux
- Screen Lock detection currently requires a GNOME-based desktop
  (`gsettings`). Other desktop environments will report "could not
  determine" for that one check — this is a known, documented limitation
  (see `ROADMAP.md`), not a bug.
- `ufw` is preferred for the firewall check, falling back to `iptables` if
  `ufw` isn't installed.
- Run with `sudo` for the most accurate disk encryption / update checks;
  it works without, with reduced accuracy on those specific checks.

### macOS
- Some checks (FileVault status, Application Firewall state) may prompt
  for your password or require running from a Terminal with appropriate
  permissions granted (System Settings → Privacy & Security → check for a
  Terminal/Python permission prompt on first run).

## Development install

```bash
pip install -r requirements.txt
pip install pytest black ruff mypy
pytest
```

All 32+ tests should pass on a clean checkout without any special
privileges (tests that need a live listening socket create their own
temporary one; nothing touches real system configuration).

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| `ModuleNotFoundError: No module named 'src'` | Run commands from the project root (the folder containing `app.py`), not from inside `src/`. |
| GUI opens but scan buttons do nothing | Check `logs/secureaudit.log` for the actual exception — audits fail gracefully and log details rather than crashing. |
| Port scan takes much longer than a few seconds | Uncommon, but possible on a heavily loaded machine or restrictive firewall adding latency per connection attempt; this is expected to be rare. |
| `pip install` fails on PySide6 | Ensure you're on Python 3.11+ and have a recent `pip` (`pip install --upgrade pip` first). |