# User Guide

## Overview

SecureAudit checks your machine's security posture across seven areas and
gives you a single 0–100 score, plus specific, guided steps to fix
anything it finds. It does not modify your system — everything it does is
read-only.

## Dashboard

The landing page. Shows:

- **Security Score** (0–100 ring) — 100 minus a penalty for every finding,
  weighted by severity (Informational: 0, Low: 5, Medium: 15, High: 30,
  Critical: 50).
- **System Health** — a rollup of the worst severity found anywhere in the
  last scan.
- **Firewall & Ports**, **Disk Encryption**, **Updates**, **Screen Lock**,
  **Running Processes** — one card each, showing "Passed" or the worst
  severity found in that area.
- **Start Scan / Generate Report / View History** buttons — shortcuts into
  the other pages.

Nothing shows here until you've run at least one scan.

## Scan

Two options:

- **Quick Scan** — System Information, Firewall Status, Open Ports. Fast,
  no elevated privileges needed for a meaningful result.
- **Full Scan** — everything Quick Scan covers, plus Disk Encryption,
  Automatic Updates, Screen Lock, and Running Processes. Takes a few
  seconds longer (the full 65,535-port scan is the majority of that time,
  and it's still typically under 10 seconds).

While a scan runs, the status line updates live — including sub-progress
during the port scan (e.g. "Open Ports: 48,000/65,535"). Each finding
appears as a card once the scan finishes, with a severity badge and, for
anything that isn't purely informational, a **"View Fix Steps"** button.

## View Fix Steps

Click this on any finding to open a dialog with:

- **What could happen if this isn't fixed** — a plain-English explanation
  of the actual risk (not just "this is bad").
- **Numbered steps** — specific to your OS, down to actual menu paths or
  terminal commands.
- **Estimated time** and a restart warning if the fix requires one.
- **Copy Steps** — copies the whole thing (including the threat
  explanation) to your clipboard so you can paste it into a note, ticket,
  or message to whoever needs to actually make the change.

For the Open Ports finding specifically, if multiple risky ports were
found, this dialog breaks each one down individually — its own threat
paragraph and its own fix steps — rather than one generic blob.

## Processes

A live table of everything currently running: PID, user, CPU%, memory%,
status, and full executable path. Use the search box to filter by name,
user, or path. Rows are highlighted in red if the process is running from
a file that no longer exists on disk (the same check the Running
Processes audit performs) — a known technique used by malware to evade
file-based antivirus after it's already loaded into memory. Click
**Refresh** to take a new snapshot at any time.

## Reports

Pick any past scan from the list and export it as:

- **PDF** — a formatted report with an executive summary and a
  color-coded findings table, suitable for sharing.
- **JSON** — full machine-readable data, including every field on every
  finding.
- **CSV** — flat, spreadsheet-friendly format.

Reports save to the folder configured in Settings (default: `reports/` in
the project directory).

## History

Every scan you've ever run, newest first, with its score and type
(Quick/Full). Click a row to see every finding from that scan below the
table — useful for tracking whether something you fixed actually stayed
fixed.

## Settings

- **Export Folder** — where reports get saved. Browse to change it.
- **Notifications** — toggle (currently a preference flag; no OS-level
  notifications are sent yet).
- **Scheduled Scans** — shown but disabled; not implemented yet (see
  `ROADMAP.md`).

Settings are saved to `config/user_settings.json` and persist across app
restarts.

## About

App version, author, tech stack, and license.

## Using the CLI instead

Everything above is also available without the GUI:

```bash
python cli.py scan --type quick
python cli.py scan --type full --report pdf
python cli.py history --limit 10
```

Useful for running SecureAudit on a headless machine or scripting it into
a scheduled job (until built-in scheduling exists).

## A note on privileges

Several checks are more accurate when SecureAudit is run with
administrator/root privileges (see `INSTALL.md` for OS-specific notes).
Without elevation, those specific checks will honestly report "could not
determine" rather than guessing — you'll never get a false "all clear"
because of a permissions issue.