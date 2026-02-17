# Things ↔ Tana Sync

**Bi-directional sync** between [Things 3](https://culturedcode.com/things/) and [Tana](https://tana.inc/) with simple commands.

## Features

### Things → Tana
Sync tasks from Things 3 to Tana:
- **Clipboard Sync** (default): Copies tasks in Tana Paste format - just paste into Tana
- **API Sync** (optional): Sends tasks directly to Tana with automatic duplicate prevention

### Tana → Things (NEW!)
Sync tasks from Tana to Things 3:
- Copy tasks from Tana and sync them to Things 3 using the Things URL scheme
- Filter tasks by supertag (e.g., only sync tasks tagged with `#things`)
- Automatically creates tasks with notes, tags, and checklist items
- Schedule tasks for today, tomorrow, or any date

📖 **[See Quick Start Guide for Tana → Things](QUICKSTART_TANA_TO_THINGS.md)**

## Quick Start

### Things → Tana

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

### Tana → Things

```bash
# 1. Copy tasks from Tana (Cmd+C)

# 2. Run sync - syncs all tasks from clipboard
uvx --from git+https://github.com/reify-nz/things-to-tana tana-to-things

# OR: Only sync tasks tagged with #things
uvx --from git+https://github.com/reify-nz/things-to-tana tana-to-things --filter things

# OR: Schedule all tasks for today
uvx --from git+https://github.com/reify-nz/things-to-tana tana-to-things --when today --reveal
```

Tasks are automatically added to Things 3!

## Tana → Things: Detailed Usage

The reverse workflow is perfect for **capturing tasks in Tana during meetings** and then **managing them in Things 3**.

### How It Works

1. **Capture tasks in Tana** (great for rapid note-taking in meetings)
2. **Tag tasks** you want to sync with `#things` (optional, but recommended)
3. **Copy nodes** from Tana (select nodes and Cmd+C)
4. **Run the sync** command
5. **Tasks appear in Things 3** automatically via URL scheme

### Command Options

```bash
# Basic: Sync all tasks from clipboard
tana-to-things

# Filter: Only sync tasks with specific supertag
tana-to-things --filter things

# Schedule: Add all tasks to today
tana-to-things --when today

# Schedule: Add tasks for tomorrow
tana-to-things --when tomorrow

# Schedule: Add tasks with specific date
tana-to-things --when 2025-12-31

# Reveal: Show tasks in Things after creation
tana-to-things --reveal

# Combine options
tana-to-things --filter things --when today --reveal
```

### What Gets Synced

**From Tana nodes:**
- ✅ Task title
- ✅ Child nodes (non-checkbox) → Notes
- ✅ Child nodes (checkbox) → Checklist items
- ✅ Supertags (except `#things` and `#task`) → Tags
- ✅ Nested structure preserved in notes/checklists

**Example Tana structure:**
```
- [ ] Plan team meeting #things #work
  - Agenda: Q1 review
  - [ ] Book conference room
  - [ ] Send calendar invite
  - Budget: $500
```

**Results in Things 3:**
- Title: "Plan team meeting"
- Tags: work
- Notes: "Agenda: Q1 review\nBudget: $500"
- Checklist: "Book conference room", "Send calendar invite"

### Workflow Recommendation

**Tag-based filtering** is recommended for clarity:

1. In Tana, tag tasks you want to transfer with `#things`
2. Copy your notes/meeting outcomes
3. Run: `tana-to-things --filter things`
4. Only tasks with `#things` tag are synced

This way, you can:
- Keep your meeting notes in Tana
- Only transfer actionable tasks to Things 3
- Avoid cluttering Things with non-task items

## API Sync Setup (Optional - Things → Tana only)

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

### Things → Tana

```bash
# Clipboard sync (default - no setup needed)
uvx --from git+https://github.com/reify-nz/things-to-tana things-to-tana today
# → Copies to clipboard, paste into Tana

# API sync (export environment variables first)
export TANA_API_TOKEN="..."
export SUPERTAG_ID="..."
uvx --from git+https://github.com/reify-nz/things-to-tana things-to-tana inbox
# → Syncs directly to Tana API
```

### Tana → Things

```bash
# 1. Copy tasks from Tana
# 2. Run sync

# Basic: Sync all tasks
uvx --from git+https://github.com/reify-nz/things-to-tana tana-to-things

# With filtering: Only tasks tagged #things
uvx --from git+https://github.com/reify-nz/things-to-tana tana-to-things --filter things

# With scheduling: Add to Today
uvx --from git+https://github.com/reify-nz/things-to-tana tana-to-things --when today --reveal
```

### Create Aliases for Convenience

```bash
# Add to ~/.zshrc or ~/.bashrc
echo 'alias ttt="uvx --from git+https://github.com/reify-nz/things-to-tana things-to-tana"' >> ~/.zshrc
echo 'alias ttt-reverse="uvx --from git+https://github.com/reify-nz/things-to-tana tana-to-things"' >> ~/.zshrc
source ~/.zshrc

# Now you can use short commands:
ttt today              # Things → Tana
ttt-reverse --filter things  # Tana → Things
```

## Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `TANA_API_TOKEN` | No | Your Tana API token (enables API sync mode) |
| `SUPERTAG_ID` | No | Node ID of supertag to apply (for API sync) |
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

### Things → Tana

**"Invalid input" error from Tana API:**
- Make sure `SUPERTAG_ID` is set to a valid node ID, not a name
- Get the ID using "Show API Schema" command or by copying the link and extracting `nodeid=`
- Enable debug mode to see the exact payload being sent: `export DEBUG=true`

**No tasks found:**
- Ensure Things 3 is running
- Check that you have tasks in the specified scope (today/inbox)

**Clipboard not working:**
- The script uses `pyperclip` which requires clipboard access
- Try pasting with Cmd+V in Tana

### Tana → Things

**No tasks synced:**
- Make sure you copied valid Tana Paste content (copy nodes from Tana with Cmd+C)
- If using `--filter`, ensure tasks have the specified supertag
- Check that clipboard contains content

**Things doesn't open:**
- The script only works on macOS (uses the `open` command)
- Ensure Things 3 is installed
- If URLs are printed but not opened, copy and paste them manually into a browser

**Tasks not appearing correctly:**
- Verify the Tana Paste format is correct
- Child nodes with checkboxes become checklist items
- Child nodes without checkboxes become notes
- Supertags (except `#things` and `#task`) become tags

**Permission errors:**
- macOS may ask for permission to control Things 3
- Grant the permission when prompted

## License

MIT
