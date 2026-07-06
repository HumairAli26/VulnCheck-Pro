"""
SecureAudit
Application Settings

Author: Humair Ali
"""

from dataclasses import dataclass
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class AppSettings:
    APP_NAME: str = "SecureAudit"
    VERSION: str = "0.2.0"
    COMPANY: str = "Humair Ali"
    ORGANIZATION: str = "SecureAudit"

    WIDTH: int = 1440
    HEIGHT: int = 860

    MIN_WIDTH: int = 1180
    MIN_HEIGHT: int = 680

    EXPORT_FOLDER: str = str(_ROOT / "reports")
    DATABASE_PATH: str = str(_ROOT / "database" / "secureaudit.db")
    LOG_FOLDER: str = str(_ROOT / "logs")


settings = AppSettings()
