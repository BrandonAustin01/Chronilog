# 🪵 Chronilog

**Chronilog** is a professional-grade logging package for Python. It brings structured logging, rotating files, Rich-powered console output, environment-aware configuration, and optional Sentry integration to your projects — with zero hassle.

> Designed for developers who want reliable logs, clean setup, and real-world flexibility.

---

## 🚀 Features

- ✅ `ChroniLog(name)` — get a configured logger in one line  
- 🎨 Rich terminal output (emoji-safe, dark-theme friendly)  
- 📁 Rotating file logs (path, size, backups all configurable)  
- 🔧 Supports `.env` and `.chronilog.toml` for layered config  
- 🧪 Diagnostic tools for troubleshooting setup issues  
- 🔄 Optional JSON logging support  
- 🛡️ Optional [Sentry](https://sentry.io) integration for exception tracking  
- 🧰 Developer-first: testable, extensible, production-ready  

---

## 📦 Installation

```bash
# Clone and install in editable mode (during development)
git clone https://github.com/yourname/chronilog
cd chronilog
pip install -e .
```

> Add `chronilog` to your `requirements.txt` or `pyproject.toml` for production use.

---

## 📖 What Is Chronilog?

Chronilog is a structured, reliable logging system built for real-world Python apps.  
It eliminates guesswork around log setup, integrates rotating file logs, rich console formatting,  
and includes optional diagnostics and error tracking — all with sane defaults.

Use it in everything from CLI tools to production services.

---

## 🧠 Basic Usage

```python
from chronilog import ChroniLog

log = ChroniLog("my_app")

log.info("🚀 App started")
log.warning("⚠️ Something might be wrong...")
log.error("❌ An error occurred!")
```

Chronilog auto-configures sane defaults, file logging, and console formatting.

---

## 🧩 How It Works

Chronilog reads layered config in this order:

1. Environment variables (`CHRONILOG_*`)
2. `.chronilog.toml` file (if present)
3. Internal fallback values

Then it builds:

- A rotating file handler (with custom path, size, backups)
- A rich console handler (with optional emoji fallback)
- An optional JSON or plain formatter
- A logger with the given name (e.g. `ChroniLog("my_app")`)

---

## 🔍 Understanding Log Levels

Chronilog uses Python’s standard logging levels:

| Level     | Description                          |
|-----------|--------------------------------------|
| DEBUG     | Verbose info for debugging           |
| INFO      | General status updates               |
| WARNING   | Recoverable issues or early warnings |
| ERROR     | Errors that need attention           |
| CRITICAL  | Serious failure or crash             |

You can set the level globally via:

- `.env`: `CHRONILOG_LOG_LEVEL=WARNING`
- `.toml`: `log_level = "ERROR"`

---

## ⚙️ Configuration System

Chronilog supports layered configuration from:

1. `.env` — for quick dev overrides  
2. `.chronilog.toml` — for structured project configs  
3. Internal safe defaults — as fallback  

### 🔧 Example `.env`

```ini
CHRONILOG_LOG_PATH=logs/my_app.log
CHRONILOG_LOG_LEVEL=DEBUG
CHRONILOG_LOG_MAX_MB=5
CHRONILOG_LOG_BACKUP_COUNT=3
CHRONILOG_JSON=0
```

### 🔧 Example `.chronilog.toml`

```toml
log_path = "logs/chronilog.log"
log_level = "DEBUG"
max_log_file_size = 5
backup_count = 3
enable_console = true
emoji_fallback = true
enable_sentry = false
sentry_dsn = ""
sentry_level = "ERROR"
sentry_traces_sample_rate = 0.0
```

---

## 🧰 Advanced Usage

```python
from chronilog import ChroniLog
from chronilog.core.formatter import PlainFormatter

log = ChroniLog(
    name="myapp",
    level=logging.INFO,
    file_formatter=PlainFormatter(),
    use_cache=False
)
```

### 🔎 Parameters

| Argument            | Type            | Description                                        |
|---------------------|-----------------|----------------------------------------------------|
| `name`              | `str`           | Logger name (typically `__name__`)                 |
| `level`             | `int` *(opt)*   | Custom log level (`logging.DEBUG`, etc)            |
| `console_formatter` | `Formatter`     | Override console formatting                        |
| `file_formatter`    | `Formatter`     | Override file formatting                           |
| `use_cache`         | `bool`          | Whether to reuse logger instances by name          |

---

## 📁 Log Path Defaults

Chronilog automatically chooses the most appropriate log path:

| OS       | Path Location                         |
|----------|----------------------------------------|
| Windows  | `%LOCALAPPDATA%\chronilog\logs\`       |
| macOS    | `~/Library/Logs/chronilog/`            |
| Linux    | `~/.local/share/chronilog/logs/`       |

---

## 🛠️ How to Integrate Chronilog in Your Project

1. Install Chronilog  
2. Create `.env` or `.chronilog.toml` in your project root  
3. Add `from chronilog import ChroniLog`  
4. Use `log = ChroniLog(__name__)`  
5. Start logging with `log.info(...)`, etc.  

That's it — file and console logs will be active instantly.

---

## 📌 Environment Variables Reference

| Variable Name                | Description                            |
|------------------------------|----------------------------------------|
| CHRONILOG_LOG_PATH           | File log location                      |
| CHRONILOG_LOG_LEVEL          | Log level (e.g., INFO, DEBUG)          |
| CHRONILOG_LOG_MAX_MB         | Max file size in MB before rotating    |
| CHRONILOG_LOG_BACKUP_COUNT   | Number of rotated logs to keep         |
| CHRONILOG_JSON               | Use JSON formatter (1 or 0)            |
| CHRONILOG_DISABLE_CONSOLE    | If true, disables console output       |
| CHRONILOG_EMOJI_FALLBACK     | Replaces emojis on incompatible systems|
| CHRONILOG_ENABLE_SENTRY      | Enables Sentry integration             |
| CHRONILOG_SENTRY_DSN         | Your Sentry DSN string                 |
| CHRONILOG_SENTRY_LEVEL       | Min level to send to Sentry            |
| CHRONILOG_SENTRY_SAMPLE_RATE | Tracing sample rate (0.0 to 1.0)       |

---

## ✨ Sentry Integration (Optional)

Chronilog includes first-class support for [Sentry](https://sentry.io), a powerful error tracking system.

### ✅ Enabling Sentry

1. Install the SDK:

```bash
pip install sentry-sdk
```

2. Add to `.chronilog.toml`:

```toml
enable_sentry = true
sentry_dsn = "https://your_dsn_here@sentry.io/project_id"
sentry_level = "ERROR"
sentry_traces_sample_rate = 0.0
```

3. You can also trigger Sentry manually:

```python
from chronilog.integrations.sentry import init_sentry
init_sentry()
```

### 📡 Manually Capture Exceptions

```python
from chronilog.integrations.sentry import capture_exception

try:
    raise ValueError("Something went wrong")
except Exception as e:
    capture_exception(e)
```

### ❌ Sentry not installed?

Chronilog gracefully disables Sentry if `sentry-sdk` is missing.  
All related tests will automatically be skipped.

---

## 🧪 Diagnostics

Need to verify your setup?

```python
from chronilog.diagnostics import print_diagnostics
print_diagnostics()
```

You'll get a Rich-powered terminal table showing:

- Logger name
- Log level
- Handlers active
- File path
- Config source

---

## 🧪 Testing With Chronilog

Run tests:

```bash
pytest tests/
```

Built-in usage example:

```bash
python examples/usage.py
```

### ✅ Testing tips:

Use `caplog` to capture output:

```python
def test_warning(caplog):
    log = ChroniLog("test")
    log.warning("uh oh!")
    assert "uh oh!" in caplog.text
```

Patch config:

```python
monkeypatch.setattr("chronilog.integrations.sentry._get_config", lambda key: {
    "enable_sentry": "true",
    "sentry_dsn": "invalid"
}.get(key))
```

---

## 🎛️ Configuration Precedence

Chronilog uses the following priority for resolving config:

1. `.env` overrides  
2. `.chronilog.toml`  
3. Hardcoded defaults  

Any of these can be bypassed using keyword args in `ChroniLog(...)`.

---

## 🧯 Troubleshooting

✅ Nothing appears in logs?
- Check `log_level`
- Check that `log_path` is writeable

⛔ Unicode errors on Windows?
- Set `emoji_fallback = true`

🧪 Use `print_diagnostics()` for verification

---

## 📚 Example: Flask Integration

```python
from flask import Flask
from chronilog import ChroniLog

app = Flask(__name__)
log = ChroniLog("flask_app")

@app.route("/")
def home():
    log.info("Homepage accessed")
    return "Hello from Chronilog!"
```

---

## 📚 Example Project Structure

```bash
myapp/
├── main.py
├── .env
├── .chronilog.toml
├── logs/
│   └── chronilog.log # or myapp.log
├── requirements.txt
└── tests/
```

---

---

## 🧑‍💻 Chronilog CLI

Chronilog includes a powerful CLI to help manage configuration and setup.

### 🛠️ `chronilog init`

Interactive setup wizard to generate a `.chronilog.toml` file:

```bash
chronilog init
```

It prompts for:

- Log path (e.g., `logs/chronilog.log`)
- Log level (`DEBUG`, `INFO`, etc.)
- Max log size (in MB)
- Backup count
- Console output toggle
- Emoji fallback toggle
- Sentry enable + DSN + level + trace sample rate

It creates `.chronilog.toml` in your working directory or a custom path.

### ⚙️ CLI Flags

| Flag             | Description                                                  |
|------------------|--------------------------------------------------------------|
| `--dry-run`      | Preview the config it would generate, without writing a file |
| `--config PATH`  | Specify an alternate config file location                    |

### ✅ Example

```bash
chronilog init --dry-run
```

Shows the generated config as TOML without saving.

```bash
chronilog init --config .config/chronilog.toml
```

Saves to a custom path.

### 🔐 Safe Defaults

If a `.chronilog.toml` already exists, Chronilog will:

- Prompt you to overwrite, skip, or cancel
- Validate the structure before writing
- Include comments in the output

---

## 🚧 Coming Soon: CLI Toolkit

Chronilog's CLI is expanding soon with:

- `chronilog config set key=value`  
- `chronilog config delete key`  
- `chronilog diagnostics` — full environment + logger audit  
- `chronilog view` — visual JSON log viewer with filters  
- Profile-based config switching

---


---

## 📜 License

MIT License — open-source, free for commercial and personal use.

---

## 🙌 Credits

Built with ❤️ by [Brandon McKinney](https://brandonmckinney.dev)  
Feedback welcome — open an issue or contribute anytime!
