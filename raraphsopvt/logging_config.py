import logging
from logging.handlers import RotatingFileHandler
from .config import settings
from pathlib import Path

LOG_FILE = Path(__file__).resolve().parent.parent / "app.log"


def get_logger(name: str = "raraphsopvt") -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(settings.log_level.upper())

    text_handler = logging.StreamHandler()
    text_handler.setLevel(settings.log_level.upper())
    text_handler.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] %(name)s - %(message)s")
    )

    file_handler = RotatingFileHandler(LOG_FILE, maxBytes=1_048_576, backupCount=3, encoding="utf-8")
    file_handler.setLevel(settings.log_level.upper())
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] %(name)s - %(message)s")
    )

    logger.addHandler(text_handler)
    logger.addHandler(file_handler)
    return logger


logger = get_logger()
