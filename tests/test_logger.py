from chronilog.core.logger import ChroniLog

def test_logger_initialization():
    logger = ChroniLog("test")
    assert logger.name == "test"
    assert logger.level > 0
    assert len(logger.handlers) >= 1