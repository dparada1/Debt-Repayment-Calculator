from .constants import LOG_DIR, LOG_FILE, LOG_LEVEL, LOG_FORMAT
from pathlib import Path
import logging


def setup_logger(name: str = __name__) -> logging.Logger:
    """Configures and returns a logger with file handler."""
    
    # Ensure log directory exists
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)

    # Prevent adding duplicate handlers
    if not logger.handlers:
        file_handler = logging.FileHandler(LOG_FILE)
        formatter = logging.Formatter(LOG_FORMAT)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    logger.debug(f"Logger '{name}' initialized.")
    return logger


# Initialize the logger
my_log = setup_logger()
my_log.info("Logger ready.")
