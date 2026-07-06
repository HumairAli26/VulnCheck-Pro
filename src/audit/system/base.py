"""
Base System Audit

Author: Humair Ali
"""
from abc import ABC
from abc import abstractmethod

from src.models.audit_result import AuditResult

class BaseSystemAudit(ABC):
    """
    Base class for every system audit.
    """
    @abstractmethod
    def run(self) -> AuditResult:
        """
        Execute audit.
        """
        pass