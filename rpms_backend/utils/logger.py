"""
RPMS Logging Utility
Logs activity, exceptions, and audit events to console and file
"""

import logging
import os
from rpms_backend import config

def setup_logger():
    logger = logging.getLogger("RPMS")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        # File handler
        log_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), config.LOG_FILE)
        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(name)s: %(message)s")
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        # Console handler
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter("%(levelname)s: %(message)s")
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    return logger

logger = setup_logger()
