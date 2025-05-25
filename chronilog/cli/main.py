import click
import logging

from chronilog import ChroniLog
from chronilog.cli.init import chronilog_init
from chronilog.integrations.sentry import init_sentry, capture_exception

@click.group()
def main():
    """Chronilog CLI entry point."""
    # Optional: Setup logging for CLI tools
    ChroniLog("chronilog.cli")

    # Safe auto-enable of sentry for CLI usage (can be toggled in config)
    init_sentry()

@main.command()
def init():
    """Create a .chronilog.toml config interactively."""
    chronilog_init()

@main.command()
def test_sentry():
    """Trigger a test exception for Sentry (manual use)."""
    logger = ChroniLog("chronilog.test")

    try:
        raise RuntimeError("This is a test exception for Sentry")
    except Exception as e:
        logger.error("Handled test error", exc_info=True)
        capture_exception(e)
        click.echo("🔁 Test exception sent (if Sentry is enabled).")
