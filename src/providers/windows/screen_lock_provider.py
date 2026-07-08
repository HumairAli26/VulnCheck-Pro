"""
SecureAudit
Windows Screen Lock Provider

Author: Humair Ali

NOTE: Requires Windows to run; cannot be executed/verified in this sandbox.
"""

from __future__ import annotations

from src.providers.base import ScreenLockProvider, ScreenLockStatus


class WindowsScreenLockProvider(ScreenLockProvider):
    """Reads screen-saver/lock policy from the registry."""

    def get_status(self) -> ScreenLockStatus:
        try:
            import winreg  # type: ignore[import-not-found]

            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Control Panel\Desktop")
            try:
                screensaver_active, _ = winreg.QueryValueEx(key, "ScreenSaveActive")
            except FileNotFoundError:
                screensaver_active = "0"
            try:
                screensaver_secure, _ = winreg.QueryValueEx(key, "ScreenSaverIsSecure")
            except FileNotFoundError:
                screensaver_secure = "0"
            try:
                timeout_raw, _ = winreg.QueryValueEx(key, "ScreenSaveTimeOut")
            except FileNotFoundError:
                timeout_raw = "0"
            winreg.CloseKey(key)

            enabled = screensaver_active == "1" and screensaver_secure == "1"
            timeout_minutes = int(timeout_raw) // 60 if str(timeout_raw).isdigit() else None

            return ScreenLockStatus(
                enabled=enabled,
                timeout_minutes=timeout_minutes,
                details={
                    "ScreenSaveActive": str(screensaver_active),
                    "ScreenSaverIsSecure": str(screensaver_secure),
                },
            )
        except ImportError:
            return ScreenLockStatus(enabled=False, error="winreg is only available on Windows.")
        except OSError as exc:
            return ScreenLockStatus(enabled=False, error=str(exc))
