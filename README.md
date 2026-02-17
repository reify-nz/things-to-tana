# Things to Tana Sync

Sync tasks from [Things 3](https://culturedcode.com/things/) to [Tana](https://tana.inc/) with a single command.

Three sync modes:
- **Clipboard Sync** (default): Copies tasks in Tana Paste format - just paste into Tana
- **Local API Sync** (optional): Sends tasks directly via Tana desktop app's local API
- **Cloud API Sync** (optional): Sends tasks to Tana cloud with automatic duplicate prevention

## Quick Start

No installation required! Use [uvx](https://docs.astral.sh/uv/) to run directly from GitHub:

```bash
# Sync today's tasks to clipboard
uvx --from git+https://github.com/reify-nz/things-to-tana things-to-tana today

# Sync inbox to clipboard
uvx --from git+https://github.com/reify-nz/things-to-tana things-to-tana inbox

# Sync all tasks to clipboard
uvx --from git+https://github.com/reify-nz/things-to-tana things-to-tana all
```

After running, paste into Tana with **Cmd+V**.

## Local API Sync Setup (Optional)

Sync directly to Tana desktop app without needing API tokens or clipboard.

### 1. Enable Local API in Tana Desktop

1. Open Tana desktop app
2. Go to Settings (top right)
3. Navigate to **Tana Labs**
4. Enable **"Local API/MCP server (Alpha)"**
5. Keep Tana desktop app running

### 2. Use Local API Sync

```bash
# Sync with local API (Tana desktop must be running)
uvx --from git+https://github.com/reify-nz/things-to-tana things-to-tana today --local-api

uvx --from git+https://github.com/reify-nz/things-to-tana things-to-tana inbox --local-api

uvx --from git+https://github.com/reify-nz/things-to-tana things-to-tana all --local-api
```

**Note:** The local API runs on `http://localhost:8262` by default. You can customize this with the `TANA_LOCAL_API_URL` environment variable if needed.

## Cloud API Sync Setup (Optional)

For automatic sync to Tana cloud without clipboard:

### 1. Get Your Tana API Token

Get your token from Tana settings.

### 2. Get Your Supertag ID

To apply a supertag (like "task") to synced items, you need its node ID:

**Method 1: Using API Schema (Recommended)**
1. Open the supertag definition in Tana (e.g., "task" or "task (Tanarian Brain)")
2. Open its configuration panel
3. In the title, invoke the command palette and choose **"Show API Schema"**
4. Copy the displayed `supertag id` (this is your `SUPERTAG_ID`)

**Method 2: Using Copy Link**
1. Right-click on the supertag in Tana
2. Choose **"Copy link"**
3. The link will look like: `https://app.tana.inc?nodeid=ABC123...`
4. Extract the node ID after `nodeid=` - that's your `SUPERTAG_ID`

### 3. Set Environment Variables

```bash
export TANA_API_TOKEN="your-token-here"
export SUPERTAG_ID="your-supertag-node-id"
```

Add these to your `~/.zshrc` or `~/.bashrc` to make them permanent.

### 4. Run with Cloud API Sync

```bash
# Environment variables must be exported first
uvx --from git+https://github.com/reify-nz/things-to-tana things-to-tana today
```

## Usage Examples

```bash
# Clipboard sync (default - no setup needed)
uvx --from git+https://github.com/reify-nz/things-to-tana things-to-tana today
# → Copies to clipboard, paste into Tana

# Local API sync (Tana desktop app must be running with Local API enabled)
uvx --from git+https://github.com/reify-nz/things-to-tana things-to-tana inbox --local-api
# → Syncs directly to Tana desktop via local API

# Cloud API sync (export environment variables first)
export TANA_API_TOKEN="..."
export SUPERTAG_ID="..."
uvx --from git+https://github.com/reify-nz/things-to-tana things-to-tana inbox
# → Syncs directly to Tana cloud API

# Create an alias for convenience
echo 'alias ttt="uvx --from git+https://github.com/reify-nz/things-to-tana things-to-tana"' >> ~/.zshrc
source ~/.zshrc

# Now you can just run:
ttt today                  # Clipboard
ttt inbox --local-api      # Local API
ttt all                    # Cloud API (if TANA_API_TOKEN is set)
```

## Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `TANA_API_TOKEN` | No | Your Tana cloud API token (enables cloud API sync mode) |
| `TANA_LOCAL_API_URL` | No | URL for Tana local API (default: `http://localhost:8262`) |
| `SUPERTAG_ID` | No | Node ID of supertag to apply (for API sync modes) |
| `SUPERTAG_NAME` | No | Name of supertag to apply (for clipboard sync) |
| `TANA_TODAY_NODE_ID` | No | Target node for "today" tasks (defaults to "INBOX") |
| `DEBUG` | No | Set to `"true"` to see detailed API payload info (for troubleshooting) |

All environment variables should be exported in your shell (e.g., in `~/.zshrc` or `~/.bashrc`).

### Getting Node IDs

The Tana API requires **node IDs**, not names. Here's how to get them:

**For Supertags:**
- **Method 1:** Open supertag → Configuration panel → "Show API Schema" command → Copy `supertag id`
- **Method 2:** Right-click supertag → "Copy link" → Extract node ID from URL after `nodeid=`

**For Regular Nodes:**
- Right-click on any node → "Copy link" → Extract node ID from URL after `nodeid=`

## Development

Want to contribute? See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup, architecture, and testing.

## Troubleshooting

**Local API connection error:**
- Make sure Tana desktop app is running
- Check that Local API is enabled: Settings > Tana Labs > "Local API/MCP server (Alpha)"
- Verify the local API is accessible at `http://localhost:8262/health`
- If using a custom port, set `TANA_LOCAL_API_URL` environment variable

**"Invalid input" error from Tana Cloud API:**
- Make sure `SUPERTAG_ID` is set to a valid node ID, not a name
- Get the ID using "Show API Schema" command or by copying the link and extracting `nodeid=`
- Enable debug mode to see the exact payload being sent: `export DEBUG=true`

**No tasks found:**
- Ensure Things 3 is running
- Check that you have tasks in the specified scope (today/inbox)

**Clipboard not working:**
- The script uses `pyperclip` which requires clipboard access
- Try pasting with Cmd+V in Tana

## License

MIT
