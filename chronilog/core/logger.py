import logging

# === Custom SUCCESS Log Level ===
SUCCESS_LEVEL = 25
logging.addLevelName(SUCCESS_LEVEL, "SUCCESS")

def success(self, message, *args, **kwargs):
    if self.isEnabledFor(SUCCESS_LEVEL):
        self._log(SUCCESS_LEVEL, message, args, **kwargs)

logging.Logger.success = success
# ================================

from chronilog.core.formatter import build_console_handler, build_file_formatter
from chronilog.core.handlers import get_file_handler
from chronilog.core.config import get_log_level

_loggers = {}

def ChroniLog(
    name: str,
    level: int = None,
    console_formatter: logging.Formatter = None,
    file_formatter: logging.Formatter = None,
    use_cache: bool = True,
    enable_console: bool = False
) -> logging.Logger:
    """
    Initializes and returns a Chronilog logger instance.
    """
    if use_cache and name in _loggers:
        return _loggers[name]

    logger = logging.getLogger(name)
    logger.setLevel(level or get_log_level())
    logger.propagate = False

    # ✅ Always reset handlers (safe and reliable)
    logger.handlers.clear()

    # 🟩 File Handler
    file_handler = get_file_handler()
    file_handler.setFormatter(file_formatter or build_file_formatter())
    logger.addHandler(file_handler)

    # 🟨 Optional Console Handler
    if enable_console:
        console_handler = build_console_handler()
        console_handler.setFormatter(console_formatter or None)
        logger.addHandler(console_handler)

    if use_cache:
        _loggers[name] = logger

    return logger