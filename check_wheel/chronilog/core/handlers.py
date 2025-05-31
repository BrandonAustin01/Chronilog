import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path
from chronilog.core.formatter import build_console_handler, build_file_formatter
from chronilog.core.config import get_log_path, get_max_log_size, get_backup_count



def get_console_handler() -> logging.Handler:
    """
    Returns a Rich console logging handler.
    RichHandler manages its own formatting — no need to attach a formatter.
    """
    handler = build_console_handler()
    handler.setLevel(logging.DEBUG)  # Capture everything; logger will filter
    return handler

def get_file_handler() -> logging.Handler:
    """
    Returns a rotating file handler with safe log directory setup.
    Log format is determined by build_file_formatter().
    """
    log_path = Path(get_log_path())
    log_dir = log_path.parent
    log_dir.mkdir(parents=True, exist_ok=True)

    handler = RotatingFileHandler(
        filename=log_path,
        mode="a",
        maxBytes=get_max_log_size(),
        backupCount=get_backup_count(),
        encoding="utf-8"
    )

    handler.setFormatter(build_file_formatter())
    handler.setLevel(logging.DEBUG)
    return handler