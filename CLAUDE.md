# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This project syncs tasks from **Things 3** to **Tana**, supporting two modes:
1. **Clipboard Sync**: Formats tasks as Tana Paste and copies to clipboard
2. **API Sync**: Sends tasks directly to the Tana Input API

## Commands

### Running Scripts
**CRITICAL**: This project uses `uv` for dependency management. Always prefix Python commands with `uv run`:

```bash
# Clipboard Sync
uv run python things_to_tana.py [today|inbox|all]  # default: today

# API Sync
uv run python main.py [today|inbox]

# Testing
uv run pytest
```

### Testing
- Run tests with `uv run pytest`
- Test files follow the pattern `test_*.py`
- Tests are located in the root directory alongside source files

## Architecture

### Data Flow

**Clipboard Sync Flow** (`things_to_tana.py`):
```
Things 3 → ThingsProvider → TanaFormatter → Clipboard (Tana Paste format)
```

**API Sync Flow** (`main.py` → `sync_service.py`):
```
Things 3 → ThingsProvider → SyncService → TanaClient → Tana API
                                ↓
                          HistoryManager (tracks synced tasks)
```

### Core Components

1. **ThingsProvider** (`things_provider.py`): Abstraction layer for fetching tasks from Things 3 using the `things.py` library
   - `get_inbox_tasks()`: Fetches Inbox tasks
   - `get_today_tasks()`: Fetches Today tasks
   - `get_all_tasks()`: Fetches all tasks

2. **TanaNode Model** (`models.py`): Dual-purpose data model
   - Has TWO implementations in the codebase (this is intentional for backward compatibility)
   - `models.py`: API-focused with `to_api_payload()` method for Tana Input API
   - `tana_formatter.py`: Clipboard-focused with `to_string()` method for Tana Paste format
   - Properties: `name`/`text`, `children`, `supertags`, `checked`

3. **TanaFormatter** (`tana_formatter.py`): Converts tasks to Tana Paste format
   - `to_tana_paste()`: Converts TanaNode list to `%%tana%%` prefixed string
   - `tana_tag()`: Formats tags (handles multi-word tags with `#[[tag name]]`)
   - `tana_date()`: Formats dates as `[[date:YYYY-MM-DD]]`
   - `tana_field()`: Formats fields as `name:: value`

4. **SyncService** (`sync_service.py`): Orchestrates API sync workflow
   - `_convert_task_to_node()`: Transforms Things 3 task dict to TanaNode
   - `_process_tasks()`: Filters tasks, prevents duplicates via HistoryManager
   - Skips: completed/canceled tasks, projects, already-synced tasks

5. **TanaClient** (`tana_client.py`): Handles Tana API communication
   - `send_nodes()`: POSTs nodes to Tana Input API endpoint
   - Uses Bearer token authentication

6. **HistoryManager** (`history_manager.py`): Prevents duplicate syncs
   - Tracks task UUIDs that have been synced
   - `has_been_synced()`: Checks if task was previously synced
   - `mark_as_synced()`: Records task as synced

### Configuration (`config.py`)

Environment variables:
- `TANA_API_TOKEN`: Required for API sync (Bearer token)
- `TANA_TODAY_NODE_ID`: Target node ID for Today tasks (defaults to "INBOX")
- `SUPERTAG_NAME`: Supertag applied to synced tasks (defaults to "task")

Hardcoded constants:
- `TANA_API_ENDPOINT`: `https://europe-west1-tagr-prod.cloudfunctions.net/addToNodeV2`
- `TANA_INBOX_NODE_ID`: `"INBOX"` (special Tana identifier)

### Task Conversion Logic

Things 3 tasks are converted to TanaNodes with:
- Title → Node name
- Notes → Child nodes (split by newline)
- Tags → Supertags (in addition to configured `SUPERTAG_NAME`)
- Checklist items → Child nodes with `[x]` or `[ ]` prefix

## Key Constraints

1. **One-way sync**: Only active (incomplete) tasks are synced from Things to Tana
2. **Duplicate prevention**: HistoryManager tracks synced UUIDs to prevent re-syncing
3. **Projects skipped**: Only individual tasks are synced, not project containers
4. **Supertag handling**: Multi-word tags use `#[[tag name]]` syntax in Tana Paste format

## Dependencies

- `things.py`: Things 3 database access
- `pyperclip`: Clipboard operations
- `requests`: HTTP client for Tana API
- `pytest`: Testing framework
- `flask`: Listed but not currently used (future webhook support?)
