import json
import logging
from io import StringIO
from chronilog.core.formatter import JsonFormatter, build_file_formatter, build_console_handler
from chronilog.core.config import _get_config

def test_json_formatter_outputs_valid_json():
    stream = StringIO()
    handler = logging.StreamHandler(stream)
    handler.setFormatter(JsonFormatter())
    
    logger = logging.getLogger("test.json")
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.propagate = False

    logger.info("Test JSON log")
    handler.flush()
    
    log_output = stream.getvalue().strip()
    log_data = json.loads(log_output)

    assert isinstance(log_data, dict)
    assert log_data["message"] == "Test JSON log"
    assert log_data["level"] == "INFO"
    assert "timestamp" in log_data
    assert "line" in log_data
    assert "logger_id" in log_data

def test_emoji_fallback_sets_ascii_json(monkeypatch):
    monkeypatch.setitem(_get_config.__globals__['TOML_CONFIG'], "logging", {"emoji_fallback": True})
    formatter = JsonFormatter()
    record = logging.LogRecord(
        name="test.logger", level=logging.INFO, pathname=__file__, lineno=1,
        msg="Plain ASCII fallback", args=(), exc_info=None
    )
    json_output = formatter.format(record)
    assert "\\u" not in json_output  # ensure_ascii = True → encoded unicode

def test_build_file_formatter_returns_json(monkeypatch):
    monkeypatch.setitem(_get_config.__globals__['TOML_CONFIG'], "logging", {"log_format": "json"})
    formatter = build_file_formatter()
    assert isinstance(formatter, JsonFormatter)

def test_build_file_formatter_returns_default(monkeypatch):
    monkeypatch.setitem(_get_config.__globals__['TOML_CONFIG'], "logging", {"log_format": "default"})
    formatter = build_file_formatter()
    assert isinstance(formatter, logging.Formatter)
    assert not isinstance(formatter, JsonFormatter)

def test_console_formatter_is_not_json(monkeypatch):
    monkeypatch.setitem(_get_config.__globals__['TOML_CONFIG'], "logging", {"log_format": "json"})
    handler = build_console_handler()
    assert not isinstance(handler.formatter, JsonFormatter)
