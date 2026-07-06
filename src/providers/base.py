"""
SecureAudit
Provider Interfaces

Author: Humair Ali

Every audit talks to the operating system exclusively through these
interfaces. This is what keeps `src/audits` free of any `if platform ==`
branching: audits ask the factory for "the firewall provider" and get back
whichever concrete implementation matches the current OS.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class FirewallStatus:
    enabled: bool
    profile_details: dict[str, str] = field(default_factory=dict)
    raw_output: str = ""
    error: str | None = None


@dataclass
class EncryptionStatus:
    encrypted: bool
    method: str = "Unknown"
    details: dict[str, str] = field(default_factory=dict)
    error: str | None = None


@dataclass
class UpdateStatus:
    up_to_date: bool
    pending_count: int = 0
    pending_items: list[str] = field(default_factory=list)
    error: str | None = None


@dataclass
class SystemSnapshot:
    hostname: str
    username: str
    os_name: str
    os_version: str
    cpu: str
    memory_total_gb: float
    disk_total_gb: float
    disk_used_gb: float
    uptime: str = "Unknown"


class FirewallProvider(ABC):
    """Reports whether the host firewall is active."""

    @abstractmethod
    def get_status(self) -> FirewallStatus: ...


class EncryptionProvider(ABC):
    """Reports whether the primary disk/volume is encrypted at rest."""

    @abstractmethod
    def get_status(self) -> EncryptionStatus: ...


class UpdateProvider(ABC):
    """Reports whether the OS has pending security updates."""

    @abstractmethod
    def get_status(self) -> UpdateStatus: ...


class SystemProvider(ABC):
    """Collects general host information."""

    @abstractmethod
    def get_snapshot(self) -> SystemSnapshot: ...
