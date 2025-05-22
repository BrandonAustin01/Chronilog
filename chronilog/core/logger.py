import logging
from chronilog.core.formatter import build_console_handler, build_file_formatter
from chronilog.core.handlers import get_file_handler
from chronilog.core.config import get_log_level

_loggers = {}

def ChroniLog(
    name: str,
    level: int = None,
    console_formatter: logging.Formatter = None,
    file_formatter: logging.Formatter = None,
    use_cache: bool = True
) -> logging.Logger:
    """
    Initializes and returns a Chronilog logger instance.

    Args:
        name (str): Name of the logger (usually __name__ or module identifier).
        level (int, optional): Override log level (default: config-based).
        console_formatter (logging.Formatter, optional): Override console format.
        file_formatter (logging.Formatter, optional): Override file format.
        use_cache (bool): If True, return cached logger if already initialized.

    Returns:
        logging.Logger: Configured logger instance.
    """
    if use_cache and name in _loggers:
        return _loggers[name]

    logger = logging.getLogger(name)
    logger.setLevel(level or get_log_level())
    logger.propagate = False

    # Clear any orphaned handlers if not using cache
    if not use_cache:
        logger.handlers.clear()

    if not logger.handlers:
        # Console Handler
        console_handler = build_console_handler()
        if console_formatter:
            console_handler.setFormatter(console_formatter)
        else:
            console_handler.setFormatter(None)  # Rich formats internally
        logger.addHandler(console_handler)

        # File Handler
        file_handler = get_file_handler()
        if file_formatter:
            file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    if use_cache:
        _loggers[name] = logger

    return logger
