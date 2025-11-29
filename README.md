# Things to Tana Sync

Sync tasks from [Things 3](https://culturedcode.com/things/) to [Tana](https://tana.inc/) with a single command.

Two sync modes:
- **Clipboard Sync** (default): Copies tasks in Tana Paste format - just paste into Tana
- **API Sync** (optional): Sends tasks directly to Tana with automatic duplicate prevention

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

## API Sync Setup (Optional)

For automatic sync to Tana without clipboard:

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

### 4. Run with API Sync

```bash
# Environment variables must be exported first
uvx --from git+https://github.com/reify-nz/things-to-tana things-to-tana today
```

## Usage Examples

```bash
# Clipboard sync (default - no setup needed)
uvx --from git+https://github.com/reify-nz/things-to-tana things-to-tana today
# → Copies to clipboard, paste into Tana

# API sync (export environment variables first)
export TANA_API_TOKEN="..."
export SUPERTAG_ID="..."
uvx --from git+https://github.com/reify-nz/things-to-tana things-to-tana inbox
# → Syncs directly to Tana API

# Create an alias for convenience
echo 'alias ttt="uvx --from git+https://github.com/reify-nz/things-to-tana things-to-tana"' >> ~/.zshrc
source ~/.zshrc

# Now you can just run:
ttt today
ttt inbox
ttt all
```

## Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `TANA_API_TOKEN` | No | Your Tana API token (enables API sync mode) |
| `SUPERTAG_ID` | No | Node ID of supertag to apply (for API sync) |
| `SUPERTAG_NAME` | No | Name of supertag to apply (for clipboard sync) |
| `TANA_TODAY_NODE_ID` | No | Target node for "today" tasks (defaults to "INBOX") |

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

**"Invalid input" error from Tana API:**
- Make sure `SUPERTAG_ID` is set to a valid node ID, not a name
- Get the ID using "Show API Schema" command or by copying the link and extracting `nodeid=`

**No tasks found:**
- Ensure Things 3 is running
- Check that you have tasks in the specified scope (today/inbox)

**Clipboard not working:**
- The script uses `pyperclip` which requires clipboard access
- Try pasting with Cmd+V in Tana

## License

MIT
