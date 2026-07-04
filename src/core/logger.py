from loguru import logger

logger.add(
    "logs/secureaudit.log",
    rotation="5 MB",
    retention="10 days",
    level="INFO"
)