import logging
import os
import sys

try:
    import sentry_sdk
    from sentry_sdk.integrations.logging import LoggingIntegration
except ImportError:
    sentry_sdk = None

from chronilog.core.config import _get_config

logger = logging.getLogger("chronilog.integrations.sentry")

def init_sentry(force: bool = False, install_excepthook: bool = True):
    """
    Initialize Sentry if enabled via config or forced.

    Reads from:
    - enable_sentry
    - sentry_dsn
    - sentry_level
    - sentry_traces_sample_rate

    Attaches LoggingIntegration and optionally sys.excepthook.
    """
    if sentry_sdk is None:
        logger.warning("Sentry SDK not installed. Run: pip install sentry-sdk")
        return

    enabled = force or str(_get_config("enable_sentry")).lower() == "true"
    if not enabled:
        logger.debug("Sentry is disabled in config.")
        return

    dsn = _get_config("sentry_dsn") or os.getenv("SENTRY_DSN")
    if not dsn:
        logger.warning("Sentry enabled but no DSN provided.")
        return

    level = str(_get_config("sentry_level") or "ERROR").upper()
    sample_rate = float(_get_config("sentry_traces_sample_rate") or 0.0)

    sentry_logging = LoggingIntegration(
        level=getattr(logging, level, logging.ERROR),
        event_level=logging.ERROR
    )

    try:
        sentry_sdk.init(
            dsn=dsn,
            integrations=[sentry_logging],
            traces_sample_rate=sample_rate
        )
    except Exception as e:
        logger.warning("❌ Failed to initialize Sentry: %s", e)

        # Force log flushing for pytest/caplog visibility
        for handler in logger.handlers:
            if hasattr(handler, "flush"):
                try:
                    handler.flush()
                except Exception:
                    pass
        return

    if install_excepthook:
        def _sentry_excepthook(exc_type, exc_value, tb):
            sentry_sdk.capture_exception(exc_value)
            sys.__excepthook__(exc_type, exc_value, tb)
        sys.excepthook = _sentry_excepthook

    logger.info("✅ Sentry initialized with level %s (sample_rate=%.2f)", level, sample_rate)


def capture_exception(exc: Exception):
    """Manually report a handled exception to Sentry."""
    if sentry_sdk is not None:
        sentry_sdk.capture_exception(exc)
