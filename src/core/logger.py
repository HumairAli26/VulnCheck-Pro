"""
SecureAudit
Application Logger

Author: Humair Ali
"""

from __future__ import annotations

import sys
from pathlib import Path

from loguru import logger

_LOG_DIR = Path(__file__).resolve().parents[2] / "logs"
_LOG_DIR.mkdir(exist_ok=True)

logger.remove()
if sys.stderr is not None:
    logger.add(sys.stderr, level="WARNING")
logger.add(
    _LOG_DIR / "secureaudit.log",
    rotation="5 MB",
    retention="10 days",
    level="INFO",
    enqueue=True,
)

__all__ = ["logger"]
