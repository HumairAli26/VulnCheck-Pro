"""
System Service
"""

from abc import ABC, abstractmethod
from src.core.models.system_info import SystemInfo


class SystemService(ABC):

    @abstractmethod
    def collect(self) -> SystemInfo:
        """
        Collect system information.
        """
        pass