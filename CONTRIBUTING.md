# Contributing to Things to Tana Sync

Thank you for your interest in contributing! This guide covers development setup, testing, and architecture.

## Development Setup

This project uses [uv](https://docs.astral.sh/uv/) for dependency management.

### 1. Clone the Repository

```bash
git clone git@github.com:reify-nz/things-to-tana.git
cd things-to-tana
```

### 2. Install Dependencies

```bash
uv sync
```

This creates a virtual environment and installs all dependencies from `pyproject.toml`.

### 3. Configuration

For local development, use a `.env` file (recommended):

```bash
# Copy the example and edit with your values
cp .env.example .env

# Edit .env with your actual credentials
# Example contents:
# TANA_API_TOKEN=your-token-here
# SUPERTAG_ID=your-supertag-node-id
# SUPERTAG_NAME=task
# TANA_TODAY_NODE_ID=INBOX
```

**Note:** The `.env` file is gitignored to protect your credentials.

When running locally with `uv run`, you need to use the `--env-file` flag:

```bash
# Load environment variables from .env file
uv run --env-file .env python things_to_tana.py today
uv run --env-file .env things-to-tana today
```

Alternatively, you can export variables in your shell:

```bash
export TANA_API_TOKEN="your-token-here"
export SUPERTAG_ID="your-supertag-node-id"
uv run python things_to_tana.py today
```

## Running the Project

### Development Mode

```bash
# Run with uv (using .env file)
uv run --env-file .env python things_to_tana.py today
uv run --env-file .env python things_to_tana.py inbox
uv run --env-file .env python things_to_tana.py all

# Or use the CLI entry point
uv run --env-file .env things-to-tana today

# Without .env file (uses exported environment variables)
uv run python things_to_tana.py today
```

### Testing the CLI Entry Point

```bash
# Install in editable mode (development)
uv pip install -e .

# Now you can run directly
things-to-tana today
```

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

1. **ThingsProvider** (`things_provider.py`): Abstraction layer for fetching tasks from Things 3
   - `get_inbox_tasks()`: Fetches Inbox tasks
   - `get_today_tasks()`: Fetches Today tasks
   - `get_all_tasks()`: Fetches all tasks

2. **TanaNode Model** (`models.py`): Dual-purpose data model
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
- `SUPERTAG_ID`: Supertag node ID for API sync (get via "Show API schema" in Tana)
- `SUPERTAG_NAME`: Supertag name for clipboard sync (e.g., "task" or "task (Tanarian Brain)")
- `TANA_TODAY_NODE_ID`: Target node ID for Today tasks (defaults to "INBOX")

Hardcoded constants:
- `TANA_API_ENDPOINT`: `https://europe-west1-tagr-prod.cloudfunctions.net/addToNodeV2`
- `TANA_INBOX_NODE_ID`: `"INBOX"` (special Tana identifier)

### Task Conversion Logic

Things 3 tasks are converted to TanaNodes with:
- Title → Node name
- Notes → Child nodes (split by newline)
- Tags → Supertags (clipboard mode uses names, API mode requires node IDs)
- Checklist items → Child nodes with `[x]` or `[ ]` prefix (clipboard) or checked state (API)
- Due dates → Formatted as `[[date:YYYY-MM-DD]]` (clipboard mode)

## Testing

### Run All Tests

```bash
uv run pytest
```

### Run Specific Test File

```bash
uv run pytest test_things_to_tana.py -v
uv run pytest test_tana_formatter.py -v
uv run pytest test_modules.py -v
```

### Run Tests in Quiet Mode

```bash
uv run pytest -q
```

### Test Coverage

The project has comprehensive test coverage:
- `test_things_to_tana.py`: Tests for main script, API token validation, dual-mode logic
- `test_tana_formatter.py`: Tests for Tana Paste format generation
- `test_modules.py`: Tests for models and history manager

All 37 tests should pass.

## Code Style

- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Add docstrings to functions and classes
- Keep functions focused and small

## Key Constraints

1. **One-way sync**: Only active (incomplete) tasks are synced from Things to Tana
2. **Duplicate prevention**: HistoryManager tracks synced UUIDs to prevent re-syncing (API mode only)
3. **Projects skipped**: Only individual tasks are synced, not project containers
4. **Supertag handling**:
   - Clipboard mode: Uses tag names with `#[[tag name]]` syntax
   - API mode: Requires node IDs obtained via "Show API schema" command in Tana

## Tana API Documentation

- Official docs: https://tana.inc/docs/input-api
- Sample code: https://github.com/tanainc/tana-input-api-samples
- API endpoint: `https://europe-west1-tagr-prod.cloudfunctions.net/addToNodeV2`

### Important API Notes

- Supertags **must** be referenced by their node ID, not name
- **How to get supertag node IDs:**
  - **Method 1:** Open supertag → Configuration panel → "Show API Schema" command → Copy `supertag id`
  - **Method 2:** Right-click supertag → "Copy link" → Extract node ID from URL after `nodeid=`
- The API expects JSON payload with `targetNodeId` and `nodes` array
- Each node can have: `name`, `description`, `supertags`, `children`

## Making Changes

1. Create a new branch for your feature/fix
2. Make your changes
3. Add/update tests as needed
4. Run the test suite to ensure everything passes
5. Update documentation if needed
6. Submit a pull request

## Questions?

Feel free to open an issue on GitHub if you have questions or need help!
