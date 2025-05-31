import logging
import pytest
from unittest.mock import patch
from chronilog.integrations import sentry as sentry_module
from chronilog.integrations.sentry import init_sentry

# Skip the whole module if sentry_sdk is missing
pytest.importorskip("sentry_sdk", reason="sentry_sdk is not installed")

@pytest.fixture(autouse=True)
def clear_env(monkeypatch):
    monkeypatch.delenv("SENTRY_DSN", raising=False)
    monkeypatch.delenv("CHRONILOG_SENTRY_DSN", raising=False)
    monkeypatch.setattr("chronilog.core.config._get_config", lambda key: {
        "enable_sentry": False,
        "sentry_dsn": "",
        "sentry_level": "ERROR",
        "sentry_traces_sample_rate": 0.0
    }.get(key, None))


def test_sentry_disabled_by_default(caplog):
    caplog.set_level(logging.DEBUG)
    init_sentry()
    assert "Sentry is disabled" in caplog.text


def test_sentry_invalid_dsn_logs_warning(monkeypatch, caplog):
    caplog.set_level(logging.WARNING, logger="chronilog.integrations.sentry")

    # ✅ Patch the correct target — the copy inside sentry.py
    monkeypatch.setattr("chronilog.integrations.sentry._get_config", lambda key: {
        "enable_sentry": "true",  # must be string "true" to match logic
        "sentry_dsn": "invalid",
        "sentry_level": "ERROR",
        "sentry_traces_sample_rate": 0.0,
    }.get(key))

    with patch("chronilog.integrations.sentry.sentry_sdk.init", side_effect=ValueError("Fake failure")):
        init_sentry()

    print("Captured Logs:", caplog.text)
    assert "Failed to initialize Sentry" in caplog.text




