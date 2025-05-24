import os
import tomllib  # Python 3.11+
import logging

from copy import deepcopy
from chronilog.utils.paths import resolve_log_path
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()  # Load .env if present

CONFIG_FILE = Path(".chronilog.toml")
TOML_CONFIG = {}

if CONFIG_FILE.exists():
    try:
        with open(CONFIG_FILE, "rb") as f:
            TOML_CONFIG = tomllib.load(f)
    except Exception as e:
        print(f"[chronilog] Warning: Failed to load .chronilog.toml: {e}")

DEFAULTS = {
    "log_path": "chronilog.log",
    "log_level": "DEBUG",
    "log_max_mb": 5,
    "log_backup_count": 3,
    "enable_console": False,
    "emoji_fallback": True,
    "wipe_log_on_startup": False,
    "timestamp_format": "%Y-%m-%d %H:%M:%S",
    "disable_rich_format": False,
    "filter_module_prefix": "",
    "enable_rotation": True,
    "console_output": "stdout",
}

def _get_config(key: str):
    """Resolves config value from .env > .toml > fallback."""
    env_value = os.getenv(f"CHRONILOG_{key.upper()}")
    if env_value is not None:
        return env_value
    if key in TOML_CONFIG.get("logging", {}):
        return TOML_CONFIG["logging"][key]
    return DEFAULTS[key]

# === Config Accessors ===

def load_config(path: Path = None) -> dict:
    """
    Returns the fully resolved config dict:
    - Starts from DEFAULTS
    - Applies .chronilog.toml (if found)
    - Does NOT apply .env (that's only used at the getter level)
    """
    config = deepcopy(DEFAULTS)
    config_path = path or Path(".chronilog.toml")

    if config_path.exists():
        try:
            with open(config_path, "rb") as f:
                toml_data = tomllib.load(f)
                for section, overrides in toml_data.items():
                    if section in config:
                        config[section].update(overrides)
                    else:
                        config[section] = overrides
        except Exception as e:
            print(f"[ChroniLog] ⚠️ Failed to load .chronilog.toml: {e}")

    return config

def get_log_path() -> str:
    raw_path = _get_config("log_path")
    return str(resolve_log_path(raw_path)) if not os.path.isabs(raw_path) else raw_path

def get_log_level() -> int:
    level_str = str(_get_config("log_level")).upper()
    return getattr(logging, level_str, logging.DEBUG)

def get_log_format() -> str:
    """
    Returns log_format config key (e.g., 'default' or 'json').
    """
    value = _get_config("log_format")
    return str(value).lower() if value else "default"

def get_max_log_size() -> int:
    try:
        return int(_get_config("log_max_mb")) * 1024 * 1024
    except Exception:
        return DEFAULTS["log_max_mb"] * 1024 * 1024

def get_backup_count() -> int:
    try:
        return int(_get_config("log_backup_count"))
    except Exception:
        return DEFAULTS["log_backup_count"]

def is_console_enabled() -> bool:
    return str(_get_config("enable_console")).lower() == "true"

def is_emoji_fallback() -> bool:
    return str(_get_config("emoji_fallback")).lower() == "true"

def should_wipe_on_startup() -> bool:
    return str(_get_config("wipe_log_on_startup")).lower() == "true"

def get_timestamp_format() -> str:
    return str(_get_config("timestamp_format"))

def is_rich_disabled() -> bool:
    return str(_get_config("disable_rich_format")).lower() == "true"

def get_filter_prefix() -> str:
    return str(_get_config("filter_module_prefix"))

def is_rotation_enabled() -> bool:
    return str(_get_config("enable_rotation")).lower() == "true"

def get_console_output() -> str:
    return str(_get_config("console_output")).lower()
