import sys
from pathlib import Path

from loguru import logger

from config import get_settings


def setup_logging() -> None:
    settings = get_settings()
    logger.remove()

    fmt = (
        '{{"timestamp":"{time:YYYY-MM-DDTHH:mm:ss.SSSZ}",'
        '"level":"{level}","message":"{message}"}}'
    )

    logger.add(sys.stderr, level=settings.log_level, format=fmt)
    log_path = Path(settings.log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    logger.add(
        str(log_path),
        level=settings.log_level,
        format=fmt,
        rotation='1 day',
        encoding='utf-8',
    )
