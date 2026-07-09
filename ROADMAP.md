# Roadmap

SecureAudit is a working, extensible core rather than a finished
"enterprise suite." This is the list of natural next steps, grouped by
theme. None of this is a commitment or a timeline — it's a map of what
would meaningfully extend the project, following the same
provider/audit/remediation pattern already established.

## More audits

- **Password policy** (min length, complexity, expiration) — Linux
  `/etc/login.defs` + PAM, Windows `net accounts`, macOS `pwpolicy`.
- **Administrator / Guest account audit** — flags enabled guest accounts
  and enumerates local admin group membership.
- **Startup programs / persistence audit** beyond the current
  deleted-executable check — enumerate actual autostart entries (Windows
  Run/RunOnce registry keys, Linux `~/.config/autostart` +
  `systemctl --user list-unit-files`, macOS LaunchAgents/LaunchDaemons)
  and flag unusually large counts or suspicious paths.
- **Browser security** — check for outdated browser versions, risky
  extensions, or insecure default settings.
- **Wi-Fi security** — flag WEP/open networks in saved profiles.
- **SSH/RDP configuration depth** — beyond "is the port open": check for
  password auth enabled, root login allowed, weak ciphers.
- **Audit logging status** — is the OS's own security event logging
  enabled and retained.
- **Time synchronization** — NTP drift can break certificate validation
  and enable certain replay attacks.

## Port scanning

- Auth-less probes for MongoDB and Elasticsearch (both have similar
  zero-auth-by-default history to Redis/Memcached but need slightly more
  protocol handshaking).
- Optional network-facing scan mode (currently localhost-only by design)
  with explicit consent/warnings, since scanning hosts you don't own can
  have legal implications.
- UDP port scanning (currently TCP-only; UDP scanning is inherently
  slower/less reliable but some services — DNS, SNMP — are UDP-first).

## Compliance mapping

- Current tagging (`CIS Control 4`, `NIST 800-53 SC-28`, etc.) is
  lightweight and finding-level. A full CIS Controls v8 / NIST CSF / ISO
  27001 crosswalk, with per-control pass/fail rollups and a dedicated
  Compliance page in the UI, is the natural next step (this was in the
  original project spec as its own page).

## Platform coverage

- **Screen Lock** currently only detects GNOME desktops on Linux via
  `gsettings`. KDE (`kwriteconfig5`/kscreenlocker) and XFCE
  (`xfconf-query`) support would close this gap.
- Execution-verification of the Windows and macOS provider code on real
  hardware/CI (currently written correctly against documented behavior
  but only Linux paths have been run and confirmed in practice).

## Operational features

- **Scheduled/background scans** — the Settings page already has a
  disabled checkbox for this; needs a scheduler (e.g. `QTimer` for
  in-app, or OS-level Task Scheduler/cron/launchd integration for
  scans while the app isn't open).
- **HTML report export**, alongside the existing PDF/JSON/CSV.
- **A plugin system** for third-party audits, so this doesn't have to be
  the only place new checks get added.
- **Score trend on the Dashboard** — compare the latest scan's score
  against the previous one and show a delta (data already exists in the
  database; this is a UI-only addition).

## Packaging & distribution

- PyInstaller packaging for one-click Windows/macOS/Linux installers
  (currently run from source via `python app.py`).

## Explicitly considered and deferred

- **Live AI-generated explanations** (calling the Claude API with a
  user-supplied key for dynamic, freeform analysis) was discussed and
  intentionally not built — the current rule-based remediation catalog
  covers this narrow, well-documented domain without the added
  dependency, cost, and non-determinism a live API call would introduce.
  Worth revisiting if the audit catalog grows into more open-ended
  territory where a fixed knowledge base stops scaling.