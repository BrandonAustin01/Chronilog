import os
import pytest
import tempfile
from pathlib import Path
from chronilog.core.config import (
    get_log_path,
    get_log_level,
    get_max_log_size,
    get_backup_count,
    load_config
)

# === Shared helper ===
def write_toml_file(path: Path, contents: str):
    path.write_text(contents, encoding="utf-8")

# === Test Cases ===

def test_env_overrides_toml_and_default(monkeypatch):
    monkeypatch.setenv("CHRONILOG_LOG_PATH", "env.log")
    monkeypatch.setenv("CHRONILOG_LOG_LEVEL", "ERROR")
    monkeypatch.setenv("CHRONILOG_LOG_MAX_MB", "42")

    assert get_log_path().endswith("env.log")
    assert get_log_level() == 40  # logging.ERROR
    assert get_max_log_size() == 42 * 1024 * 1024

def test_toml_overrides_default(tmp_path: Path, monkeypatch):
    toml_path = tmp_path / ".chronilog.toml"
    monkeypatch.chdir(tmp_path)

    write_toml_file(toml_path, """
        [logging]
        log_path = "toml.log"
        log_level = "WARNING"
        log_max_mb = 7
        log_backup_count = 9
        """)

    config = load_config()
    assert config["logging"]["log_path"] == "toml.log"
    assert config["logging"]["log_level"] == "WARNING"
    assert config["logging"]["log_max_mb"] == 7
    assert config["logging"]["log_backup_count"] == 9

def test_fallback_values_apply(monkeypatch):
    monkeypatch.delenv("CHRONILOG_LOG_PATH", raising=False)
    monkeypatch.delenv("CHRONILOG_LOG_LEVEL", raising=False)
    monkeypatch.delenv("CHRONILOG_LOG_MAX_MB", raising=False)
    monkeypatch.delenv("CHRONILOG_LOG_BACKUP_COUNT", raising=False)

    log_path = get_log_path().replace("\\", "/").lower()
    assert log_path.endswith("chronilog.log")  # ✅ match the default
    assert get_log_level() == 10  # DEBUG
    assert get_max_log_size() == 5 * 1024 * 1024
    assert get_backup_count() == 3

