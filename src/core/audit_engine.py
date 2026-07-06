"""
SecureAudit Engine

Author: Humair Ali
"""
from typing import List

from src.models.audit_result import AuditResult

class AuditEngine:
    """
    Runs all registered audits.
    """
    def __init__(self):
        self.audits = []

    def register(self, audit):
        self.audits.append(audit)

    def run(self) -> List[AuditResult]:
        results = []
        for audit in self.audits:
            results.append(
                audit.run()
            )
        return results