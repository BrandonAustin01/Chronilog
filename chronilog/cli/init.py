import os
from pathlib import Path
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.console import Console
from rich.markup import escape as rich_escape

console = Console()

DEFAULT_CONFIG = {
    "log_path": "chronilog.log",
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
    "log_format": "default"
}

FIELD_COMMENTS = {
    "log_path": "# 📁 Path to your log file",
    "log_level": "# 🪵 Minimum logging level (e.g., DEBUG, INFO)",
    "log_max_mb": "# 📦 Max file size before rotating (MB)",
    "log_backup_count": "# 🔁 Number of rotated backups to keep",
    "enable_console": "# 🖥️ Output logs to console?",
    "emoji_fallback": "# 😃 Replace emoji with safe characters?",
    "wipe_log_on_startup": "# 🧹 Wipe log file every run?",
    "timestamp_format": "# ⏱️ Timestamp format for logs",
    "disable_rich_format": "# ❌ Use plain text instead of Rich formatting?",
    "filter_module_prefix": "# 🔍 Only log modules matching this prefix",
    "enable_rotation": "# 🔄 Enable rotating log files?",
    "console_output": "# 📤 Console output stream (stdout or stderr)",
    "log_format": "# 📄 Format: 'default' or 'json'",
}


def chronilog_init(dry_run: bool = False):
    console.print("\n[bold cyan]Chronilog Config Wizard[/bold cyan] 🛠️")
    console.print("This will create a [green].chronilog.toml[/green] file in the current directory.\n")

    config = {}

    for key, default in DEFAULT_CONFIG.items():
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
                f.write(f'{key} = "{value}"\n')
            else:
                f.write(f"{key} = {str(value).lower() if isinstance(value, bool) else value}\n")
            f.write("\n")

    console.print(f"\n✅ [green].chronilog.toml created[/green] at [bold]{output_path.resolve()}[/bold]\n")
