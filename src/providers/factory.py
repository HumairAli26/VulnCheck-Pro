"""
SecureAudit
Provider Factory

Author: Humair Ali
"""

from __future__ import annotations

from src.core.platform.platform_detector import Platform, PlatformDetector
from src.providers.base import (
    EncryptionProvider,
    FirewallProvider,
    ScreenLockProvider,
    SystemProvider,
    UpdateProvider,
)


class UnsupportedPlatformError(RuntimeError):
    """Raised when no provider implementation exists for the current OS."""


def _current_platform() -> Platform:
    return PlatformDetector.current()


def get_firewall_provider() -> FirewallProvider:
    platform = _current_platform()
    if platform is Platform.WINDOWS:
        from src.providers.windows.firewall_provider import WindowsFirewallProvider

        return WindowsFirewallProvider()
    if platform is Platform.LINUX:
        from src.providers.linux.firewall_provider import LinuxFirewallProvider

        return LinuxFirewallProvider()
    if platform is Platform.MACOS:
        from src.providers.macos.firewall_provider import MacOSFirewallProvider

        return MacOSFirewallProvider()
    raise UnsupportedPlatformError(f"No firewall provider for {platform}")


def get_encryption_provider() -> EncryptionProvider:
    platform = _current_platform()
    if platform is Platform.WINDOWS:
        from src.providers.windows.encryption_provider import WindowsEncryptionProvider

        return WindowsEncryptionProvider()
    if platform is Platform.LINUX:
        from src.providers.linux.encryption_provider import LinuxEncryptionProvider

        return LinuxEncryptionProvider()
    if platform is Platform.MACOS:
        from src.providers.macos.encryption_provider import MacOSEncryptionProvider

        return MacOSEncryptionProvider()
    raise UnsupportedPlatformError(f"No encryption provider for {platform}")


def get_update_provider() -> UpdateProvider:
    platform = _current_platform()
    if platform is Platform.WINDOWS:
        from src.providers.windows.update_provider import WindowsUpdateProvider

        return WindowsUpdateProvider()
    if platform is Platform.LINUX:
        from src.providers.linux.update_provider import LinuxUpdateProvider

        return LinuxUpdateProvider()
    if platform is Platform.MACOS:
        from src.providers.macos.update_provider import MacOSUpdateProvider

        return MacOSUpdateProvider()
    raise UnsupportedPlatformError(f"No update provider for {platform}")


def get_screen_lock_provider() -> ScreenLockProvider:
    platform = _current_platform()
    if platform is Platform.WINDOWS:
        from src.providers.windows.screen_lock_provider import WindowsScreenLockProvider

        return WindowsScreenLockProvider()
    if platform is Platform.LINUX:
        from src.providers.linux.screen_lock_provider import LinuxScreenLockProvider

        return LinuxScreenLockProvider()
    if platform is Platform.MACOS:
        from src.providers.macos.screen_lock_provider import MacOSScreenLockProvider

        return MacOSScreenLockProvider()
    raise UnsupportedPlatformError(f"No screen lock provider for {platform}")


def get_system_provider() -> SystemProvider:
    platform = _current_platform()
    if platform is Platform.WINDOWS:
        from src.providers.windows.system_provider import WindowsSystemProvider

        return WindowsSystemProvider()
    if platform is Platform.LINUX:
        from src.providers.linux.system_provider import LinuxSystemProvider

        return LinuxSystemProvider()
    if platform is Platform.MACOS:
        from src.providers.macos.system_provider import MacOSSystemProvider

        return MacOSSystemProvider()
    raise UnsupportedPlatformError(f"No system provider for {platform}")
