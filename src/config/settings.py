from dataclasses import dataclass

@dataclass(frozen=True)
class AppSettings:
    APP_NAME: str = "SecureAudit"
    VERSION: str = "0.1.0"
    COMPANY: str = "Humair Ali"
    ORGANIZATION: str = "SecureAudit"

    WIDTH: int = 1600
    HEIGHT: int = 900

    MIN_WIDTH: int = 1200
    MIN_HEIGHT: int = 700

settings = AppSettings()