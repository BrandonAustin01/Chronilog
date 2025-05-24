import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from chronilog.core.formatter import build_console_handler, build_file_formatter
from chronilog.core.config import (
    get_log_path,
    get_max_log_size,
    get_backup_count,
    is_rotation_enabled,
    get_console_output
)

def get_console_handler() -> logging.Handler:
    """
    Returns a Rich-based console handler. Output stream is stdout or stderr.
    """
    handler = build_console_handler(output=get_console_output())
    handler.setLevel(logging.DEBUG)
    return handler

def get_file_handler() -> logging.Handler:
    """
    Returns a file or rotating file handler depending on config.
    """
    log_path = Path(get_log_path())
    log_path.parent.mkdir(parents=True, exist_ok=True)

    if is_rotation_enabled():
        handler = RotatingFileHandler(
            filename=log_path,
            mode="a",
            maxBytes=get_max_log_size(),
            backupCount=get_backup_count(),
            encoding="utf-8"
        )
    else:
        handler = logging.FileHandler(filename=log_path, encoding="utf-8", mode="a")

    handler.setFormatter(build_file_formatter())
    handler.setLevel(logging.DEBUG)
    return handler
