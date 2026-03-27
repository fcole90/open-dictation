import os

from loguru import logger

# Allow DEBUG logging to be enabled via environment variable
log_level = os.environ.get("LOG_LEVEL", "INFO").upper()

logger.add(
    "logs/open_dictation.log",
    rotation="10 MB",
    retention="10 days",
    level=log_level,
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
)
