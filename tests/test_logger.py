from chronilog.core.logger import get_logger

def test_logger_initialization():
    logger = get_logger("test")
    assert logger.name == "test"
    assert logger.level > 0
    assert len(logger.handlers) >= 1