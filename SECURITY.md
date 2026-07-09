# Security Policy

SecureAudit is a **defensive** security posture auditor. It reads local
system configuration (firewall state, disk encryption, patch status,
listening ports, screen lock settings, running processes) and reports on
it — it does not perform exploitation, credential attacks, or any offensive
action against this or any other machine.

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.4.x   | ✅ |
| < 0.4   | ❌ (upgrade recommended) |

## Reporting a vulnerability

If you find a security issue **in SecureAudit itself** — for example:

- A way to make it execute arbitrary/attacker-controlled commands
- A way for a malicious finding/report to trigger code execution when
  viewed
- Credential or scan-history data being written somewhere insecure or
  transmitted off the machine
- A provider that could be tricked into destructive behavior (it should
  only ever *read* system state, never modify it)

please **do not open a public GitHub issue**. Instead, email the
maintainer directly (see repository contact info) with:

1. A description of the issue and its impact
2. Steps to reproduce
3. The OS/Python/PySide6 versions involved

Please allow a reasonable window to investigate and patch before any
public disclosure.

## What is *not* a security issue (please open a normal issue instead)

- A check reporting an inaccurate result (e.g. firewall audit says
  "enabled" when it's actually off) — this is a correctness bug, report it
  as a regular issue with your OS/version.
- Windows/macOS provider code that doesn't work as documented — several of
  these are written correctly against documented OS behavior but have not
  been execution-verified on real hardware (this is called out explicitly
  in the README/CHANGELOG). Bug reports with real logs are very welcome.
- Missing audits/features — see `ROADMAP.md`.

## Data handling

- All scan history is stored **locally only**, in a SQLite database under
  `database/secureaudit.db`. Nothing is sent to any external server.
- Reports (PDF/JSON/CSV) are written locally to the `reports/` folder (or
  wherever you configure in Settings). You are responsible for how you
  share these — they can contain sensitive information about your system's
  security posture (open ports, process names, usernames).
- There is no telemetry, analytics, or phone-home behavior anywhere in
  this codebase.
- The port scanner only connects to `127.0.0.1` (localhost) — it does not
  scan other hosts or networks.

## Privileges

Several checks (BitLocker status on Windows, some firewall/encryption
checks on Linux/macOS) are more accurate when run with
administrator/root privileges. SecureAudit is designed to **degrade
gracefully** without elevated privileges — it reports "could not
determine" rather than guessing — but it will never request privilege
escalation on its own or install anything without your explicit action.