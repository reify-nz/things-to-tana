# Things to Tana Sync

This project provides tools to sync tasks from [Things 3](https://culturedcode.com/things/) to [Tana](https://tana.inc/).

It supports two modes:
1. **Clipboard Sync**: Copies tasks to the clipboard in Tana Paste format.
2. **API Sync**: Sends tasks directly to the Tana Input API with duplicate prevention.

## Setup

This project uses [uv](https://docs.astral.sh/uv/) for dependency management.

1. **Install Dependencies**:
   ```bash
   uv sync
   ```

2. **Configuration**:

   ### For Clipboard Sync (Default)
   No configuration needed! Just run the script and paste into Tana.

   Optional environment variables:
   - `SUPERTAG_NAME`: Name of the supertag to apply (e.g., `"task"` or `"task (Tanarian Brain)"`)

   ### For API Sync (Automated)
   Required environment variables:
   - `TANA_API_TOKEN`: Your Tana API token (get from Tana settings)
   - `SUPERTAG_ID`: Node ID of your supertag in Tana (see below for how to get this)

   Optional environment variables:
   - `TANA_TODAY_NODE_ID`: Node ID for "Today" tasks (defaults to `"INBOX"`)

   #### Getting Your SUPERTAG_ID
   The Tana API requires supertag **node IDs**, not names. To get your supertag ID:

   1. Open Tana
   2. Navigate to your supertag (e.g., "task (Tanarian Brain)")
   3. Run the command **"Show API schema"** on the supertag
   4. Copy the `nodeId` from the schema
   5. Set it as an environment variable:
      ```bash
      export SUPERTAG_ID="your-node-id-here"
      ```

## Usage

### Main Script: `things_to_tana.py`

This script **automatically chooses** between clipboard and API sync:
- **API Sync**: Used when `TANA_API_TOKEN` is configured
- **Clipboard Sync**: Used when no token is configured (fallback)

```bash
# Sync Today's tasks (default)
uv run python things_to_tana.py

# Sync Inbox
uv run python things_to_tana.py inbox

# Sync All tasks (inbox + today)
uv run python things_to_tana.py all
```

#### Example: Clipboard Sync
```bash
uv run python things_to_tana.py today
# → Copies to clipboard, paste with Cmd+V in Tana
```

#### Example: API Sync
```bash
export TANA_API_TOKEN="your-token-here"
export SUPERTAG_ID="your-supertag-node-id"
uv run python things_to_tana.py today
# → Sends directly to Tana API
```

### Alternative: Direct API Sync with `main.py`

For explicit API sync (always uses API, never clipboard):

```bash
# Sync Today's tasks
uv run python main.py today

# Sync Inbox
uv run python main.py inbox

# Sync both
uv run python main.py all
```

## Testing
Run the test suite with pytest:
```bash
uv run pytest
```

All 37 tests should pass.
