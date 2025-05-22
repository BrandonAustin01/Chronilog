from chronilog.core.logger import ChroniLog
from chronilog.core.formatter import PlainFormatter
log = ChroniLog("test_app")

log.info("🚀 Application boot sequence initiated.")
log.debug("🔧 Initializing subsystems...")
log.warning("⚠️ Cache service failed to respond — using fallback mode.")
log.error("❌ Failed to connect to database. Retrying...")
log.critical("🔥 Fatal error: Cannot proceed without DB connection.")
log.info("🧪 Logging test complete.")

def test_custom_formatter():
    logger = ChroniLog("test_custom", file_formatter=PlainFormatter(), use_cache=False)
    logger.info("Custom formatter test")

test_custom_formatter()
