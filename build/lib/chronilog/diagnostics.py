import os
import traceback
import logging
from chronilog.core.logger import get_logger
from chronilog.core.config import (
    get_log_path,
    get_log_level,
    get_max_log_size,
    get_backup_count
)

from pathlib import Path
from logging import Logger

def run_diagnostics(logger_name: str = "diagnostics") -> dict:
    """
    Performs a full logger audit: file path check, write test, config printout.
    Returns a structured result dictionary.
    """
    results = {
        "log_path": get_log_path(),
        "log_level": get_log_level(),
        "log_size_limit": get_max_log_size(),
        "log_backup_count": get_backup_count(),
        "file_writeable": False,
        "logger_attached": False,
        "errors": [],
    }

    try:
        # File write test
        log_path = Path(results["log_path"])
        log_path.parent.mkdir(parents=True, exist_ok=True)
        test_message = "[chronilog] Diagnostic write test"

        with open(log_path, "a", encoding="utf-8") as f:
            f.write(test_message + "\n")

        results["file_writeable"] = True

    except Exception as e:
        results["errors"].append(f"File write failed: {str(e)}")

    try:
        # Check if logger has working handlers
        logger: Logger = get_logger(logger_name)
        logger.debug("[chronilog] Diagnostics logger test message.")
        results["logger_attached"] = len(logger.handlers) > 0

    except Exception as e:
        results["errors"].append(f"Logger test failed: {str(e)}\n{traceback.format_exc()}")

    return results


def print_diagnostics():
    """Prints logger configuration and audit results to the terminal."""
    from rich.console import Console
    from rich.table import Table

    console = Console()
    results = run_diagnostics()

    console.rule("[bold green]🩺 chroniloggr Diagnostics Report")

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Parameter")
    table.add_column("Value", style="cyan")

    table.add_row("Log Path", results["log_path"])
    table.add_row("Log Level", logging.getLevelName(results["log_level"]))
    table.add_row("Max Size", f"{results['log_size_limit'] // (1024 * 1024)} MB")
    table.add_row("Backup Count", str(results["log_backup_count"]))
    table.add_row("File Writeable", "✅ Yes" if results["file_writeable"] else "❌ No")
    table.add_row("Logger Active", "✅ Yes" if results["logger_attached"] else "❌ No")

    console.print(table)

    if results["errors"]:
        console.print("\n[bold red]Errors Detected:")
        for err in results["errors"]:
            console.print(f"  • {err}")
    else:
        console.print("\n[bold green]All systems go.\n")