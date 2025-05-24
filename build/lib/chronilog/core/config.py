import os
import tomllib  # Python 3.11+ for reading .toml
from chronilog.utils.paths import resolve_log_path
from dotenv import load_dotenv
from pathlib import Path
import logging

# Load .env file if present
load_dotenv()

# Load .toml file (optional, overrides .env)
CONFIG_FILE = Path(".chronilog.toml")
TOML_CONFIG = {}

if CONFIG_FILE.exists():
    try:
        with open(CONFIG_FILE, "rb") as f:
            TOML_CONFIG = tomllib.load(f)
    except Exception as e:
        print(f"[chroniloggr] Warning: Failed to load config from TOML: {e}")

# Internal fallback defaults
DEFAULTS = {
    "log_path": "logs/chronilog.log",
    "log_level": "DEBUG",
    "log_max_mb": 5,
    "log_backup_count": 3,
}


def _get_config(key: str):
    """Load from .env > .toml > fallback."""
    # Env first
    env_value = os.getenv(f"CHRONILOG_{key.upper()}")
    if env_value is not None:
        return env_value

    # Then TOML
    if key in TOML_CONFIG:
        return TOML_CONFIG[key]

    # Fallback
    return DEFAULTS[key]


def get_log_path() -> str:
    raw_path = _get_config("log_path")
    return str(resolve_log_path(raw_path)) if not os.path.isabs(raw_path) else raw_path


def get_log_level() -> int:
    level_str = str(_get_config("log_level")).upper()
    return getattr(logging, level_str, logging.DEBUG)


def get_max_log_size() -> int:
    # Convert MB to bytes
    try:
        return int(_get_config("log_max_mb")) * 1024 * 1024
    except Exception:
        return 5 * 1024 * 1024


def get_backup_count() -> int:
    try:
        return int(_get_config("log_backup_count"))
    except Exception:
        return 3