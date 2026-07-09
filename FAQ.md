# Frequently Asked Questions

### Is this a penetration testing tool?

No. SecureAudit is purely defensive: it reads your own machine's
configuration (firewall, encryption, patch status, listening ports,
screen lock, running processes) and tells you what's wrong and how to fix
it. It does not attempt to exploit anything, guess passwords, or attack
other systems.

### Does it scan my whole network, or just this computer?

Just this computer. The port scan connects only to `127.0.0.1`
(localhost) — it never reaches out to other devices on your network or
the internet. Scanning devices you don't own without permission can be
illegal in many jurisdictions; SecureAudit's scope is intentionally
limited to the machine it's running on.

### Does it send my data anywhere?

No. There's no telemetry, analytics, or network calls other than the
provider checks that legitimately need to talk to local OS services.
Scan history is stored locally in `database/secureaudit.db`; reports are
saved locally to wherever you configure in Settings. Nothing leaves your
machine.

### Why does the full port scan check all 65,535 ports? Isn't that slow?

It's a full TCP connect scan, done concurrently (a 400-worker thread
pool), and it typically finishes in 3–5 seconds on localhost. Scanning
only a fixed watchlist (the original design) misses anything running on
an unexpected port — a full scan catches everything actually listening,
which is the whole point of an audit.

### Why do some checks say "could not determine"?

Usually a privileges issue. BitLocker status on Windows, and some
firewall/encryption reads on Linux/macOS, need administrator/root access
to answer definitively. Rather than guessing (and potentially telling you
"you're fine" when it doesn't actually know), SecureAudit reports honestly
that it couldn't check. Re-run elevated for a definitive answer.

### What's the difference between Quick Scan and Full Scan?

Quick Scan covers System Information, Firewall Status, and Open Ports —
fast, no elevated privileges typically needed. Full Scan adds Disk
Encryption, Automatic Updates, Screen Lock, and Running Processes, which
is the more thorough option and what you'd want before generating a
report you intend to actually act on.

### Does it work equally well on Windows, Linux, and macOS?

Every audit has a real implementation for all three, using each OS's
native tools. That said, this project was built and tested primarily in a
Linux environment — the Linux code paths have been executed and verified
directly; the Windows and macOS provider code is written correctly
against documented OS behavior but hasn't been execution-verified on real
Windows/macOS hardware yet. If you hit something that doesn't work as
described on Windows or macOS, please report it (see `CONTRIBUTING.md`).

### Why does Screen Lock only work on some Linux desktops?

The current implementation reads GNOME's `gsettings`. KDE, XFCE, and other
desktop environments store this setting differently and aren't supported
yet — this is a known gap, tracked in `ROADMAP.md`, not a silent failure.

### Can I delete my scan history?

Yes — it's just a SQLite file at `database/secureaudit.db`. Closing the
app and deleting that file clears all history (the app will recreate an
empty database on next launch). There's no in-app "delete history" button
yet.

### Can I run this without the GUI?

Yes, via `python cli.py scan` and `python cli.py history` — useful for
headless machines or scripting.

### Is the Redis/Memcached "no authentication" check safe to run?

Yes — it sends exactly one standard, read-only liveness command each
service defines itself (`PING` for Redis, `version` for Memcached). It
doesn't write data, doesn't attempt authentication bypass, and doesn't
send anything outside each protocol's own normal usage.

### What license is this under?

MIT — see `LICENSE`. Use it, modify it, and redistribute it freely.

### I found a real security issue in SecureAudit itself. Where do I report it?

See `SECURITY.md` — please don't open a public issue for anything that
could be actively exploited; there's a private reporting path described
there.