"""
Audit Result Model

Author: Humair Ali
"""
from dataclasses import dataclass, field

@dataclass
class AuditResult:
    """
    Represents the result of one audit.
    """
    title: str
    status: str
    risk: str
    description: str
    recommendation: str
    details: dict[str, str] = field(default_factory=dict)