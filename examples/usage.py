import time
from chronilog.core.logger import get_logger
from chronilog.diagnostics import print_diagnostics

logger = get_logger("demo")

def simulate_startup():
    logger.info("🚀 Application boot sequence initiated.")
    time.sleep(0.3)
    logger.debug("🔧 Initializing subsystems...")
    time.sleep(0.2)
    logger.warning("⚠️ Cache service failed to respond — using fallback mode.")
    time.sleep(0.2)
    logger.error("❌ Failed to connect to database. Retrying...")
    time.sleep(0.2)
    logger.critical("🔥 Fatal error: Cannot proceed without DB connection.")
    logger.info("🧪 Logging test complete.")

def show_diagnostics():
    print_diagnostics()

if __name__ == "__main__":
    print("[Chronilog Demo] Starting usage example...")
    simulate_startup()
    show_diagnostics()