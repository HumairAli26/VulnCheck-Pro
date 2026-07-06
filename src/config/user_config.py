"""
SecureAudit
User Configuration (persisted preferences)

Author: Humair Ali
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from src.config.settings import settings

_CONFIG_DIR = Path(__file__).resolve().parents[2] / "config"
_CONFIG_PATH = _CONFIG_DIR / "user_settings.json"


@dataclass
class UserConfig:
    theme: str = "dark"
    export_folder: str = settings.EXPORT_FOLDER
    scheduled_scans_enabled: bool = False
    notifications_enabled: bool = True


def load_config() -> UserConfig:
    if not _CONFIG_PATH.exists():
        return UserConfig()
    try:
        data = json.loads(_CONFIG_PATH.read_text(encoding="utf-8"))
        return UserConfig(**{**asdict(UserConfig()), **data})
    except (json.JSONDecodeError, TypeError, OSError):
        return UserConfig()


def save_config(config: UserConfig) -> None:
    _CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    _CONFIG_PATH.write_text(json.dumps(asdict(config), indent=2), encoding="utf-8")
