# Repository Guide for Coding Agents

This repository, `tana-sync`, provides tools to synchronize tasks from **Things 3** to **Tana**.

## Overview

The project supports two main synchronization modes:
1.  **Clipboard Sync**: Fetches tasks from Things 3, formats them as Tana Paste, and copies them to the clipboard.
2.  **API Sync**: Fetches tasks and sends them directly to the Tana Input API.

## Key Files

- **`things_to_tana.py`**: The main script for **Clipboard Sync**. It fetches tasks and copies the Tana Paste format to the clipboard.
- **`main.py`**: The entry point for **API Sync**. It uses `sync_service.py` to send tasks to Tana via the API.
- **`tana_formatter.py`**: Contains logic for formatting data into Tana Paste format (nodes, children, supertags).
- **`things_provider.py`**: Abstraction layer for fetching tasks from Things 3 using the `things.py` library.
- **`config.py`**: Configuration file for API tokens and default settings.
- **`pyproject.toml`**: Project metadata and dependencies.

## Running the Code

**IMPORTANT**: This project uses `uv` for dependency management and running scripts. Always use `uv run` to execute Python commands.

### 1. Clipboard Sync (Manual)
To run the clipboard sync script:

```bash
# Sync Today's tasks (default)
uv run python things_to_tana.py

# Sync Inbox
uv run python things_to_tana.py inbox

# Sync All tasks
uv run python things_to_tana.py all
```

### 2. API Sync (Automated)
To run the API sync service:

```bash
# Sync Today's tasks
uv run python main.py today

# Sync Inbox
uv run python main.py inbox
```

### 3. Testing
To run the test suite:

```bash
uv run pytest
```

## Dependencies

Dependencies are managed in `pyproject.toml`. Key dependencies include:
- `things.py`: For interacting with the Things 3 database.
- `pyperclip`: For clipboard operations.
- `requests`: For making API calls to Tana.
- `flask`: (Likely for a future webhook or local server component).
