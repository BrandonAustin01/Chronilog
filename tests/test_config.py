from chronilog.core import config

def test_log_level_default():
    level = config.get_log_level()
    assert isinstance(level, int)
    assert level in [10, 20, 30, 40, 50]  # DEBUG–CRITICAL

def test_log_path_fallback():
    path = config.get_log_path()
    assert isinstance(path, str)
    assert "log" in path.lower()
    assert path.endswith(".log")

def test_max_log_size_safe():
    size = config.get_max_log_size()
    assert isinstance(size, int)
    assert size > 0