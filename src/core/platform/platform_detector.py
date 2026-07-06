"""
SecureAudit
Platform Detector

Author: Humair Ali
"""
from enum import Enum
import platform

class Platform(Enum):
    WINDOWS = "Windows"
    LINUX = "Linux"
    MACOS = "Darwin"
    UNKNOWN = "Unknown"

class PlatformDetector:
    """
    Detects the operating system SecureAudit is running on.
    """
    @staticmethod
    def current() -> Platform:
        system = platform.system()
        if system == Platform.WINDOWS.value:
            return Platform.WINDOWS

        if system == Platform.LINUX.value:
            return Platform.LINUX

        if system == Platform.MACOS.value:
            return Platform.MACOS

        return Platform.UNKNOWN