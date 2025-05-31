import sys
import logging
import json
import hashlib
from rich.console import Console
from rich.logging import RichHandler
from logging import StreamHandler, Formatter
from chronilog.core.config import (
    is_emoji_fallback,
    is_rich_disabled,
    get_console_output,
    get_timestamp_format,
    get_log_format
)

class JsonFormatter(logging.Formatter):
    """
    Emits logs as structured JSON with full metadata.
    Compatible with emoji fallback and timestamp formatting.
    """
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": self.formatTime(record, get_timestamp_format()),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "funcName": record.funcName,
            "line": record.lineno,
            "pathname": record.pathname,
            "process": record.process,
            "thread": record.thread,
            "logger_id": hashlib.md5(record.name.encode()).hexdigest()[:8]
        }

        return json.dumps(log_data, ensure_ascii=is_emoji_fallback())


def build_console_handler(output: str = None) -> StreamHandler:
    """
    Returns a console handler based on config:
    - Uses RichHandler by default
    - Falls back to plain StreamHandler if rich formatting is disabled
    - Emoji-safe if emoji_fallback is enabled
    - Console output stream: stdout or stderr
    """
    # Determine desired output stream
    stream = sys.stdout if (output or get_console_output()) == "stdout" else sys.stderr

    # ✅ Plain fallback mode if rich is disabled
    if is_rich_disabled():
        fmt = "[%(asctime)s] [%(levelname)s] %(message)s" if is_emoji_fallback() \
              else "%(asctime)s - %(levelname)s - %(message)s"
        return StreamHandler(stream=stream, formatter=Formatter(fmt, get_timestamp_format()))

    # ✅ RichHandler with redirected console output
    return RichHandler(
        show_time=True,
        show_level=True,
        show_path=False,
        markup=not is_emoji_fallback(),
        rich_tracebacks=True,
        console=Console(file=stream)
    )

def build_file_formatter() -> logging.Formatter:
    """
    Returns a file formatter based on config.
    Supports plain, emoji, or JSON formatting.
    """
    fmt_type = get_log_format()
    time_fmt = get_timestamp_format()

    if fmt_type == "json":
        return JsonFormatter()

    if is_emoji_fallback():
        fmt = "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
    else:
        fmt = "🕒 %(asctime)s | 🔹 %(levelname)s | 🧩 %(name)s | ✏️ %(message)s"

    return logging.Formatter(fmt=fmt, datefmt=time_fmt)
