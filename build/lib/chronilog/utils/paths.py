import os
from pathlib import Path
import platform

def get_default_log_dir(app_name: str = "chronilog") -> Path:
    """
    Returns a safe default log directory path based on the OS.

    Windows: C:/Users/<User>/AppData/Local/<app_name>/logs
    macOS:   ~/Library/Logs/<app_name>/
    Linux:   ~/.local/share/<app_name>/logs/
    """
    system = platform.system()

    if system == "Windows":
        base = os.getenv("LOCALAPPDATA", Path.home() / "AppData" / "Local")
        log_dir = Path(base) / app_name / "logs"
    elif system == "Darwin":
        log_dir = Path.home() / "Library" / "Logs" / app_name
    else:  # Linux or other UNIX-like
        log_dir = Path.home() / ".local" / "share" / app_name / "logs"

    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir

def resolve_log_path(filename: str = "chronilog.log", app_name: str = "chronilog") -> str:
    """
    Combines default directory with filename to build the full path.
    """
    return str(get_default_log_dir(app_name) / filename)