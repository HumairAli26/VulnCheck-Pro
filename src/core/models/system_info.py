"""
System Information Model
"""
from dataclasses import dataclass

@dataclass
class SystemInfo:
    hostname: str
    username: str
    operating_system: str
    operating_system_version: str
    cpu: str
    memory_gb: float
    disk_total_gb: float
    disk_used_gb: float
    python_version: str