import click
from chronilog.cli.init import chronilog_init

@click.group()
def main():
    pass

@main.command()
def init():
    """Create a .chronilog.toml config interactively."""
    chronilog_init()
