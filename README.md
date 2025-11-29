# Things to Tana Sync

This project provides tools to sync tasks from [Things 3](https://culturedcode.com/things/) to [Tana](https://tana.inc/).

It supports two modes:
1. **Clipboard Sync**: Copies tasks to the clipboard in Tana Paste format.
2. **API Sync**: Sends tasks directly to the Tana Input API.

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configuration**:
   - For API Sync, you need to set your Tana API Token.
   - You can set it in `config.py` or as an environment variable `TANA_API_TOKEN`.
   - Other optional environment variables:
     - `TANA_TODAY_NODE_ID`: Node ID for "Today" tasks (defaults to Inbox).
     - `SUPERTAG_NAME`: Name of the supertag to apply (defaults to "task").

## Usage

### Clipboard Sync (Manual)
Run the script to copy tasks to your clipboard, then paste them into Tana.

```bash
# Sync Today's tasks (default)
python things_to_tana.py

# Sync Inbox
python things_to_tana.py inbox

# Sync All tasks
python things_to_tana.py all
```

### API Sync (Automated)
Run the sync service to send tasks directly to Tana.

```bash
# Sync Today's tasks
python main.py today

# Sync Inbox
python main.py inbox
```

## Testing
Run the test suite with pytest:
```bash
pytest
```
