"""
SecureAudit
Remediation Guide

Author: Humair Ali

Turns a single-sentence ``AuditResult.recommendation`` into an actionable,
numbered walkthrough plus a plain-English "what happens if I ignore this"
explanation -- tailored to the OS that's actually running, since "enable
your firewall" means a completely different set of clicks/commands on
Windows vs. Linux vs. macOS.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from src.core.platform.platform_detector import Platform, PlatformDetector
from src.models.audit_result import AuditResult
from src.services.remediation.port_threats import PORT_THREATS


@dataclass
class RemediationGuide:
    """A step-by-step fix for one finding, plus context on the risk it poses."""

    threat: str = ""
    steps: list[str] = field(default_factory=list)
    estimated_time: str = "5-10 minutes"
    requires_restart: bool = False
    references: list[str] = field(default_factory=list)


# Keyed by (finding title, platform). Steps are written as if speaking
# directly to the user, one concrete action per line.
_GUIDES: dict[tuple[str, Platform], RemediationGuide] = {
    ("Firewall Status", Platform.WINDOWS): RemediationGuide(
        threat=(
            "With no firewall, every network service running on this machine is directly "
            "reachable by anything else on the same network (or the internet, if you're not "
            "behind a router doing NAT) -- there's nothing filtering unsolicited inbound connections."
        ),
        steps=[
            "Open Start and search for 'Windows Security', then open it.",
            "Select 'Firewall & network protection'.",
            "Click each network profile listed (Domain, Private, Public).",
            "Toggle 'Microsoft Defender Firewall' to On for each profile.",
            "Re-run this scan to confirm the firewall now shows as enabled.",
        ],
        estimated_time="2-5 minutes",
        references=["https://support.microsoft.com/windows/turn-microsoft-defender-firewall-on-or-off"],
    ),
    ("Firewall Status", Platform.LINUX): RemediationGuide(
        threat=(
            "With no firewall, every network service running on this machine is directly "
            "reachable by anything else on the same network -- there's nothing filtering "
            "unsolicited inbound connections."
        ),
        steps=[
            "Open a terminal.",
            "Install ufw if it isn't already present: sudo apt install ufw",
            "Enable it: sudo ufw enable",
            "Confirm it's active: sudo ufw status verbose",
            "Re-run this scan to confirm the firewall now shows as enabled.",
        ],
        estimated_time="2-5 minutes",
        references=["https://help.ubuntu.com/community/UFW"],
    ),
    ("Firewall Status", Platform.MACOS): RemediationGuide(
        threat=(
            "With no firewall, every network service running on this machine is directly "
            "reachable by anything else on the same network -- there's nothing filtering "
            "unsolicited inbound connections."
        ),
        steps=[
            "Open System Settings.",
            "Go to Network -> Firewall.",
            "Turn the firewall On.",
            "Re-run this scan to confirm the firewall now shows as enabled.",
        ],
        estimated_time="1-3 minutes",
        references=["https://support.apple.com/guide/mac-help/mh34041/mac"],
    ),
    ("Disk Encryption", Platform.WINDOWS): RemediationGuide(
        threat=(
            "If this laptop/PC is ever lost or stolen, an unencrypted drive can simply be "
            "removed and read on another machine -- every file, saved password, and document "
            "is fully accessible with no login required."
        ),
        steps=[
            "Open Start and search for 'Manage BitLocker', then open it.",
            "Select your system drive (usually C:) and click 'Turn on BitLocker'.",
            "Choose how to back up your recovery key (Microsoft account, file, or print) "
            "and store it somewhere safe -- you will need it if you ever lose access.",
            "Choose 'Encrypt entire drive' for the most complete protection.",
            "Restart when prompted, then let encryption finish in the background.",
            "Re-run this scan afterward to confirm BitLocker shows as On.",
        ],
        estimated_time="20-60 minutes (mostly in the background)",
        requires_restart=True,
        references=["https://support.microsoft.com/windows/turn-on-device-encryption"],
    ),
    ("Disk Encryption", Platform.LINUX): RemediationGuide(
        threat=(
            "If this laptop/PC is ever lost or stolen, an unencrypted drive can simply be "
            "removed and read on another machine -- every file, saved password, and document "
            "is fully accessible with no login required."
        ),
        steps=[
            "Full-disk encryption on Linux (LUKS) is normally set up during OS installation.",
            "Back up your important data first -- converting an existing unencrypted "
            "install to LUKS in place is risky and distribution-specific.",
            "The most reliable path is to reinstall the OS and choose 'Encrypt the new "
            "installation' (or equivalent) at the disk-partitioning step.",
            "After reinstalling, re-run this scan to confirm LUKS is detected.",
        ],
        estimated_time="Requires a reinstall; plan for an hour or more",
        references=["https://wiki.archlinux.org/title/Dm-crypt"],
    ),
    ("Disk Encryption", Platform.MACOS): RemediationGuide(
        threat=(
            "If this Mac is ever lost or stolen, an unencrypted drive can simply be removed "
            "and read on another machine -- every file, saved password, and document is fully "
            "accessible with no login required."
        ),
        steps=[
            "Open System Settings.",
            "Go to Privacy & Security -> FileVault.",
            "Click 'Turn On...'.",
            "Choose how to store your recovery key (iCloud or a local recovery key) and "
            "save it somewhere safe.",
            "Let encryption finish in the background (you can keep using the Mac).",
            "Re-run this scan afterward to confirm FileVault shows as On.",
        ],
        estimated_time="20-60 minutes (mostly in the background)",
        references=["https://support.apple.com/guide/mac-help/mh11785/mac"],
    ),
    ("Automatic Updates", Platform.WINDOWS): RemediationGuide(
        threat=(
            "Pending security updates mean publicly-known vulnerabilities in this OS remain "
            "unpatched -- attackers actively scan for exactly this window, since exploit code "
            "for patched CVEs is often published within days of the patch itself."
        ),
        steps=[
            "Open Start and search for 'Windows Update settings'.",
            "Click 'Check for updates'.",
            "Install everything listed, especially anything marked 'Security update'.",
            "Restart if prompted.",
            "Re-run this scan afterward to confirm no updates remain pending.",
        ],
        estimated_time="10-30 minutes",
        requires_restart=True,
        references=["https://support.microsoft.com/windows/update-windows"],
    ),
    ("Automatic Updates", Platform.LINUX): RemediationGuide(
        threat=(
            "Pending security updates mean publicly-known vulnerabilities in installed "
            "packages remain unpatched -- attackers actively scan for exactly this window."
        ),
        steps=[
            "Open a terminal.",
            "Refresh package lists: sudo apt update",
            "Install pending updates: sudo apt upgrade -y",
            "Restart if the kernel or a core library was updated.",
            "Re-run this scan afterward to confirm no updates remain pending.",
        ],
        estimated_time="5-20 minutes",
        references=["https://ubuntu.com/server/docs/software-updates"],
    ),
    ("Automatic Updates", Platform.MACOS): RemediationGuide(
        threat=(
            "Pending security updates mean publicly-known vulnerabilities in this OS remain "
            "unpatched -- attackers actively scan for exactly this window."
        ),
        steps=[
            "Open System Settings.",
            "Go to General -> Software Update.",
            "Install anything listed.",
            "Restart if prompted.",
            "Re-run this scan afterward to confirm no updates remain pending.",
        ],
        estimated_time="10-30 minutes",
        requires_restart=True,
        references=["https://support.apple.com/HT201541"],
    ),
    ("Screen Lock", Platform.WINDOWS): RemediationGuide(
        threat=(
            "Without an automatic screen lock, anyone who walks up to this unattended device "
            "gets full access to whatever you're logged into -- email, files, saved sessions, "
            "banking, everything -- with no password required."
        ),
        steps=[
            "Open Start and search for 'Screen saver settings', then open it.",
            "Choose any screen saver and set 'Wait' to 5-10 minutes.",
            "Check 'On resume, display logon screen'.",
            "Click OK, then re-run this scan to confirm.",
        ],
        estimated_time="1-2 minutes",
        references=["https://support.microsoft.com/windows/lock-your-windows-pc"],
    ),
    ("Screen Lock", Platform.LINUX): RemediationGuide(
        threat=(
            "Without an automatic screen lock, anyone who walks up to this unattended device "
            "gets full access to whatever you're logged into -- with no password required."
        ),
        steps=[
            "Open a terminal (GNOME-based desktops).",
            "Enable locking: gsettings set org.gnome.desktop.screensaver lock-enabled true",
            "Set a short idle timeout (5 minutes = 300 seconds): "
            "gsettings set org.gnome.desktop.session idle-delay 300",
            "Re-run this scan to confirm.",
        ],
        estimated_time="1-2 minutes",
        references=["https://help.gnome.org/users/gnome-help/stable/privacy-screen-lock.html.en"],
    ),
    ("Screen Lock", Platform.MACOS): RemediationGuide(
        threat=(
            "Without an automatic screen lock, anyone who walks up to this unattended device "
            "gets full access to whatever you're logged into -- with no password required."
        ),
        steps=[
            "Open System Settings.",
            "Go to Lock Screen.",
            "Set 'Require password after screen saver begins or display is turned off' to "
            "'Immediately' or a short delay.",
            "Re-run this scan to confirm.",
        ],
        estimated_time="1-2 minutes",
        references=["https://support.apple.com/guide/mac-help/mchlp2452/mac"],
    ),
    ("Running Processes", Platform.WINDOWS): RemediationGuide(
        threat=(
            "A process running from a file that no longer exists on disk is a well-known "
            "indicator of compromise -- malware often deletes its own dropped binary right "
            "after execution specifically so file-scanning antivirus can't find it, while the "
            "malicious code keeps running in memory."
        ),
        steps=[
            "Open Task Manager (Ctrl+Shift+Esc) and find the flagged PID under the Details tab.",
            "Right-click it and choose 'Open file location' -- if Windows says the file no "
            "longer exists, that confirms the deleted-executable state.",
            "If you don't recognize this process or didn't just update/remove the app it "
            "belongs to, end the task immediately.",
            "Run a full scan with Windows Defender (or your installed antivirus/EDR) afterward.",
            "Re-run this scan to confirm it's no longer flagged.",
        ],
        estimated_time="10-20 minutes",
        references=["https://attack.mitre.org/techniques/T1070/004/"],
    ),
    ("Running Processes", Platform.LINUX): RemediationGuide(
        threat=(
            "A process running from a file that no longer exists on disk is a well-known "
            "indicator of compromise -- malware often deletes its own dropped binary right "
            "after execution specifically so file-scanning antivirus can't find it, while the "
            "malicious code keeps running in memory."
        ),
        steps=[
            "Inspect the process: ls -la /proc/<PID>/exe (it will show '(deleted)' in the target).",
            "Check what it's doing: sudo cat /proc/<PID>/cmdline and sudo lsof -p <PID>",
            "If you don't recognize it or didn't just upgrade/remove the package it belongs to, "
            "kill it: sudo kill -9 <PID>",
            "Run a malware scan (e.g. sudo apt install chkrootkit rkhunter && sudo rkhunter --check) afterward.",
            "Re-run this scan to confirm it's no longer flagged.",
        ],
        estimated_time="10-20 minutes",
        references=["https://attack.mitre.org/techniques/T1070/004/"],
    ),
    ("Running Processes", Platform.MACOS): RemediationGuide(
        threat=(
            "A process running from a file that no longer exists on disk is a well-known "
            "indicator of compromise -- malware often deletes its own dropped binary right "
            "after execution specifically so file-scanning antivirus can't find it, while the "
            "malicious code keeps running in memory."
        ),
        steps=[
            "Open Activity Monitor and find the flagged PID.",
            "Double-click it and select 'Sample' or check its file path -- if the file is gone, "
            "that confirms the deleted-executable state.",
            "If you don't recognize it, force-quit it from Activity Monitor.",
            "Run a scan with your installed antivirus/EDR (e.g. Malwarebytes for Mac) afterward.",
            "Re-run this scan to confirm it's no longer flagged.",
        ],
        estimated_time="10-20 minutes",
        references=["https://attack.mitre.org/techniques/T1070/004/"],
    ),
}

_DEFAULT_ESTIMATE = "10-20 minutes"


def _build_open_ports_guide(result: AuditResult, platform: Platform) -> RemediationGuide:
    """
    Open Ports is unlike the other audits: each open port is its own
    distinct threat with its own fix, so this builds a combined guide
    covering every port actually found in ``result.details``.
    """
    threats: list[str] = []
    steps: list[str] = []

    for port_str, service in result.details.items():
        try:
            port = int(port_str)
        except ValueError:
            continue

        info = PORT_THREATS.get(port)
        if info is None:
            threats.append(f"Port {port} ({service}): commonly-abused service -- review why it's open.")
            steps.append(f"Port {port} ({service}): identify and stop the process, or restrict it at the firewall.")
            continue

        threats.append(f"Port {port} ({info.service}): {info.threat}")
        for step in info.steps_for(platform):
            steps.append(f"[Port {port} / {info.service}] {step}")

    if not threats:
        threats.append(
            "Unrecognized open port(s) were found; review each to confirm it's intentional."
        )

    return RemediationGuide(
        threat="\n\n".join(threats),
        steps=steps or ["Review the open port(s) listed and close anything not explicitly needed."],
        estimated_time=f"{max(5, 5 * len(result.details))}-{max(10, 10 * len(result.details))} minutes",
        references=["https://attack.mitre.org/techniques/T1046/"],
    )


# Fallback used when there's no OS-specific guide and the finding isn't Open Ports.
_GENERIC_GUIDES: dict[str, RemediationGuide] = {}


def get_remediation(result: AuditResult) -> RemediationGuide:
    """
    Return the best available guide for a finding.

    Falls back, in order, to: the Open Ports per-port builder, an
    OS-specific guide, a generic guide keyed only by title, and finally a
    single generic step built from the finding's own recommendation text
    so the dialog is never empty.
    """
    platform = PlatformDetector.current()

    if result.title == "Open Ports" and result.details:
        return _build_open_ports_guide(result, platform)

    guide = _GUIDES.get((result.title, platform))
    if guide:
        return guide

    guide = _GENERIC_GUIDES.get(result.title)
    if guide:
        return guide

    return RemediationGuide(
        threat=result.description,
        steps=[result.recommendation],
        estimated_time=_DEFAULT_ESTIMATE,
        references=list(result.references),
    )
