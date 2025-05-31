import os
from pathlib import Path
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.console import Console
from rich.markup import escape as rich_escape

console = Console()

DEFAULT_CONFIG = {
    "log_level": "DEBUG",
    "log_max_mb": 5,
    "log_backup_count": 3,
    "enable_console": False,
    "emoji_fallback": True,
    "wipe_log_on_startup": False,
    "timestamp_format": "%Y-%m-%d %H:%M:%S",
    "disable_rich_format": False,
    "filter_module_prefix": "",
    "enable_rotation": True,
    "console_output": "stdout",
    "log_format": "default",

    # === Sentry Config ===
    "enable_sentry": False,
    "sentry_dsn": "",
    "sentry_level": "ERROR",
    "sentry_traces_sample_rate": 0.0,
}

FIELD_COMMENTS = {
    "log_path": (
        "# 📁 Path to your log file\n"
        "# Can be relative or absolute. Will be auto-created if missing."
    ),
    "log_level": (
        "# 🪵 Minimum logging level\n"
        "# Options: DEBUG, INFO, SUCCESS, WARNING, ERROR, CRITICAL\n"
        "# Controls which messages get logged."
    ),
    "log_max_mb": (
        "# 📦 Max log file size in megabytes\n"
        "# When this size is exceeded, log rotation begins."
    ),
    "log_backup_count": (
        "# 🔁 Number of rotated log files to keep\n"
        "# Older files beyond this count will be deleted."
    ),
    "enable_console": (
        "# 🖥️ Whether to also log to the console\n"
        "# If false, logs are written to file only."
    ),
    "emoji_fallback": (
        "# 😃 Replace emojis with safe ASCII characters\n"
        "# Useful for environments that can't render Unicode."
    ),
    "wipe_log_on_startup": (
        "# 🧹 Clear the log file every time the app starts\n"
        "# WARNING: This deletes previous log history."
    ),
    "timestamp_format": (
        "# ⏱️ Timestamp format for logs\n"
        "# Uses Python's datetime format (e.g., %Y-%m-%d %H:%M:%S)."
    ),
    "disable_rich_format": (
        "# ❌ Disable all rich/colored output\n"
        "# If true, plain text formatting is used for console logs."
    ),
    "filter_module_prefix": (
        "# 🔍 Only log messages from modules starting with this prefix\n"
        "# Leave empty to log everything."
    ),
    "enable_rotation": (
        "# 🔄 Enable rotating log files based on size\n"
        "# Works with 'log_max_mb' and 'log_backup_count'."
    ),
    "console_output": (
        "# 📤 Which output stream to use for console logs\n"
        "# Options: stdout, stderr"
    ),
    "log_format": (
        "# 📄 Format style for log output\n"
        "# Options: 'default' (styled), or 'json' (structured)"
    ),
    "enable_sentry": (
        "# 🛰️ Enable Sentry error tracking integration\n"
        "# Set to true to activate Sentry logging (requires sentry-sdk)."
    ),
    "sentry_dsn": (
        "# 🔗 Your Sentry DSN URL\n"
        "# You can get this from your Sentry project settings."
    ),
    "sentry_level": (
        "# 🧭 Minimum level to send logs to Sentry\n"
        "# Default is ERROR. Options: DEBUG, INFO, WARNING, ERROR, CRITICAL"
    ),
    "sentry_traces_sample_rate": (
        "# 📊 Trace sampling rate for performance monitoring\n"
        "# 0.0 disables tracing. Use >0.0 to enable transaction capture."
    ),
}

def chronilog_init(dry_run: bool = False):
    console.print("\n[bold cyan]Chronilog Config Wizard[/bold cyan] 🛠️")
    console.print("This will create a [green].chronilog.toml[/green] file in the current directory.\n")

    config = {}

    # ✅ Prompt for log folder and log file name
    log_dir = Prompt.ask("📁 Log folder?", default="logs").strip().replace("\\", "/")
    log_file = Prompt.ask("📄 Log file name?", default="app.log").strip()
    if not log_file.lower().endswith(".log"):
        log_file += ".log"

    log_path = str(Path(log_dir) / log_file).replace("\\", "/")
    console.print(f"📝 Final log path will be: [bold green]{log_path}[/bold green]\n")
    config["log_path"] = log_path

    for key, default in DEFAULT_CONFIG.items():
        if key == "log_path":
            continue
        emoji = FIELD_COMMENTS.get(key, "").split()[0].replace("#", "").strip()
        prompt_label = f"{emoji} {key.replace('_', ' ').capitalize()}?" if emoji else f"{key.replace('_', ' ').capitalize()}?"

        if isinstance(default, bool):
            value = Confirm.ask(prompt_label, default=default)
        elif isinstance(default, int):
            value = IntPrompt.ask(prompt_label, default=default)
        else:
            value = Prompt.ask(prompt_label, default=str(default))

        config[key] = value

    if dry_run:
        console.print("\n📄 [bold]Preview of .chronilog.toml[/bold] (not written):\n")
        console.print("[italic dim]# You can copy and paste this manually[/italic dim]\n")
        console.print("[bold green][logging][/bold green]")
        for key, value in config.items():
            comment = FIELD_COMMENTS.get(key)
            if comment:
                console.print(f"[dim]{comment}[/dim]")

            if isinstance(value, str):
                if key == "log_path":
                    raw_path = Path(value)
                    cwd = Path.cwd()
                    try:
                        value = str(raw_path.relative_to(cwd)).replace("\\", "/")
                    except ValueError:
                        value = str(raw_path).replace("\\", "/")
                console.print(f'{key} = "{rich_escape(value)}"')
            else:
                console.print(f"{key} = {str(value).lower() if isinstance(value, bool) else value}")
        return

    output_path = Path(".chronilog.toml")
    if output_path.exists():
        overwrite = Confirm.ask("\n⚠️ .chronilog.toml already exists. Overwrite?", default=False)
        if not overwrite:
            console.print("[yellow]❌ Aborting config creation.[/yellow]\n")
            return

    with output_path.open("w", encoding="utf-8") as f:
        f.write("# ========================================\n")
        f.write("# 🛠️  Chronilog Configuration\n")
        f.write("# ========================================\n\n")
        f.write("[logging]\n")

        for key, value in config.items():
            comment = FIELD_COMMENTS.get(key)
            if comment:
                f.write(f"{comment}\n")

            if isinstance(value, str):
                if key == "log_path":
                    raw_path = Path(value)
                    cwd = Path.cwd()
                    try:
                        value = str(raw_path.relative_to(cwd)).replace("\\", "/")
                    except ValueError:
                        value = str(raw_path).replace("\\", "/")
                f.write(f'{key} = "{value}"\n')
            else:
                f.write(f"{key} = {str(value).lower() if isinstance(value, bool) else value}\n")
            f.write("\n")

    try:
        display_path = output_path.relative_to(Path.cwd())
    except ValueError:
        display_path = output_path.resolve()
    
    console.print(f"\n✅ [green].chronilog.toml created[/green] → [bold]{display_path}[/bold]\n")