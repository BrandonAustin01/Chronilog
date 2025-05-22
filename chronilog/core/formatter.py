import logging
import json
import os

from datetime import datetime
from rich.logging import RichHandler


USE_JSON = os.getenv("CHRONILOG_JSON", "0") == "1"

class JsonFormatter(logging.Formatter):
    """Custom JSON formatter for logging."""
    def format(self, record: logging.LogRecord) -> str:
        timestamp = datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S')
        return json.dumps({
            "timestamp": timestamp,
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        })
    
class PlainFormatter(logging.Formatter):
    """Plain text formatter for file output (no Rich)."""
    def format(self, record: logging.LogRecord) -> str:
        timestamp = datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S')
        return f"[{timestamp}] [{record.levelname}] [{record.name}] {record.getMessage()}"

def build_console_handler() -> logging.Handler:
    """Returns a rich console handler with beautiful output."""
    return RichHandler(
        rich_tracebacks=True,
        markup=True,
        show_time=True,
        show_level=True,
        show_path=False
    )

def build_file_formatter() -> logging.Formatter:
    """Returns the correct file formatter (JSON or plain)."""
    return JsonFormatter() if USE_JSON else PlainFormatter()