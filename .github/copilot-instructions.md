# Copilot Instructions for Things to Tana Sync

## Project Overview

This is a Python project that synchronizes tasks from Things 3 (macOS task manager) to Tana (knowledge management tool). The project supports two modes:
1. **Clipboard Sync**: Formats tasks as Tana Paste and copies to clipboard
2. **API Sync**: Sends tasks directly to Tana via the Input API

## Technology Stack

- **Language**: Python 3.13+
- **Package Manager**: `uv` (NOT pip or poetry)
- **Testing**: pytest
- **Key Libraries**: 
  - `things.py` for Things 3 database access
  - `pyperclip` for clipboard operations
  - `requests` for API calls
  - `flask` for future webhook functionality

## Development Commands

Always use `uv` for running commands:

```bash
# Install dependencies
uv sync

# Run the main script
uv run things-to-tana [today|inbox|all]

# Run with environment file
uv run --env-file .env things-to-tana today

# Run tests
uv run pytest

# Run specific test file
uv run pytest test_tana_formatter.py -v
```

**NEVER** use `pip install` or create virtual environments manually - `uv` handles this automatically.

## Code Style and Conventions

- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Add docstrings to functions and classes
- Keep functions focused and small
- Use descriptive variable names (e.g., `task_uuid` not `tid`)
- Environment variables should be UPPER_CASE (e.g., `TANA_API_TOKEN`)
- File names should be snake_case (e.g., `things_provider.py`)

## Architecture Patterns

### Core Components

1. **ThingsProvider** (`things_provider.py`): Abstraction for Things 3 database
   - Methods: `get_inbox_tasks()`, `get_today_tasks()`, `get_all_tasks()`

2. **TanaNode (API sync model)** (`models.py`): Data model for Tana Input API sync
   - Has a `name` field and `to_api_payload()` for API mode
   - Not used for clipboard / Tana Paste mode

3. **Tana clipboard formatting utilities** (`tana_formatter.py`): Converts nodes to Tana Paste format
   - Defines a separate `TanaNode` class with a `text` field for clipboard sync
   - Exposes a module-level `to_tana_paste(nodes)` function that takes a list of these `TanaNode` instances and returns Tana Paste text
   - Formats: tags (`#[[tag]]`), dates (`[[date:YYYY-MM-DD]]`), fields (`name:: value`)

4. **SyncService** (`sync_service.py`): Orchestrates API sync
   - Filters completed/canceled tasks
   - Prevents duplicates via HistoryManager

5. **TanaClient** (`tana_client.py`): Handles API communication
   - Uses Bearer token authentication
   - Endpoint: `https://europe-west1-tagr-prod.cloudfunctions.net/addToNodeV2`

6. **HistoryManager** (`history_manager.py`): Tracks synced tasks
   - Prevents duplicate syncs using task UUIDs

### Data Flow

**Clipboard Sync**: Things 3 → ThingsProvider → TanaFormatter → Clipboard

**API Sync**: Things 3 → ThingsProvider → SyncService → TanaClient → Tana API
                                                ↓
                                         HistoryManager

## Testing Conventions

- All test files start with `test_` (e.g., `test_tana_formatter.py`)
- Test functions start with `test_` (e.g., `test_format_basic_node()`)
- Use descriptive test names that explain what is being tested
- Mock external dependencies (Things 3 database, Tana API, clipboard)
- Each test should be independent and not rely on other tests
- Run `uv run pytest` before committing changes

## Important Constraints

1. **Active tasks only**: Skip completed, canceled, and project containers
2. **Duplicate prevention**: HistoryManager tracks UUIDs (API mode only)
3. **Supertag handling**:
   - Clipboard mode: Use tag names (`SUPERTAG_NAME`)
   - API mode: Use node IDs (`SUPERTAG_ID`)

## Environment Variables

Required for API sync:
- `TANA_API_TOKEN`: Bearer token for Tana API
- `SUPERTAG_ID`: Node ID of supertag (get via "Show API Schema" in Tana)

Optional:
- `SUPERTAG_NAME`: Supertag name for clipboard mode (default: "task")
- `TANA_TODAY_NODE_ID`: Target node for today tasks (default: "INBOX")
- `DEBUG`: Set to "true" for detailed logging

Never commit `.env` files - they are gitignored.

## API Integration Notes

### Things 3
- Uses `things.py` library to read SQLite database
- Database location: `~/Library/Group Containers/JLMPQHK86H.com.culturedcode.ThingsMac/Things Database.thingsdatabase/main.sqlite`
- Returns task dictionaries with keys: `uuid`, `title`, `notes`, `status`, `due`, etc.

### Tana Input API
- Endpoint: `https://europe-west1-tagr-prod.cloudfunctions.net/addToNodeV2`
- Authentication: Bearer token in header
- Payload structure: `{ "targetNodeId": "INBOX", "nodes": [...] }`
- Node structure: `{ "name": "...", "description": "...", "supertags": [...], "children": [...] }`
- Supertags must use node IDs, not names
- Special node ID: "INBOX" for Tana inbox

### Tana Paste Format
- Prefix: `%%tana%%`
- Nodes start with `-` or `  -` for children
- Tags: `#tag` or `#[[multi word tag]]`
- Dates: `[[date:YYYY-MM-DD]]`
- Fields: `name:: value`
- Checkboxes: `- [x]` or `- [ ]`

## When Making Changes

1. Read existing code to understand patterns before adding new features
2. Maintain consistency with existing code style
3. Add tests for new functionality
4. Update `README.md` or `CONTRIBUTING.md` if user-facing behavior changes
5. Ensure `uv run pytest` passes before submitting
6. Consider both clipboard and API modes when making changes

## Common Pitfalls to Avoid

- Don't use `pip` - always use `uv`
- Don't hardcode API tokens - use environment variables
- Don't sync completed or canceled tasks
- Don't sync project containers, only individual tasks
- Don't use supertag names in API mode - use node IDs
- Don't commit `.env` files
- Don't create complex nested logic - keep functions simple and focused
