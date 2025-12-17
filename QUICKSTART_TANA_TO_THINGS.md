# Quick Start: Tana to Things 3 Sync

## TL;DR

```bash
# 1. Copy tasks from Tana (Cmd+C)
# 2. Run this command:
uvx --from git+https://github.com/reify-nz/things-to-tana tana-to-things --filter things
```

## Why Use This?

**Tana is great for:**
- ✅ Meeting notes
- ✅ Quick task capture
- ✅ Brainstorming
- ✅ Knowledge management

**Things 3 is great for:**
- ✅ Task management
- ✅ Scheduling
- ✅ Focus and organization
- ✅ Getting things done

**This tool lets you:**
- Capture tasks rapidly in Tana during meetings
- Transfer actionable items to Things 3 for proper task management
- Keep the best of both worlds

## Recommended Workflow

### Step 1: Tag Tasks in Tana

When taking notes in Tana, tag tasks you want to transfer with `#things`:

```
- Meeting with Sarah
  - Discussed Q1 goals
  - [ ] Send follow-up email #things
  - [ ] Review budget proposal #things
  - Personal note: Ask about vacation policy
```

### Step 2: Copy and Sync

After your meeting:

```bash
# Copy nodes from Tana (select nodes, Cmd+C)
# Then run:
uvx --from git+https://github.com/reify-nz/things-to-tana tana-to-things --filter things
```

Only tasks tagged with `#things` are synced!

### Step 3: Manage in Things 3

Tasks now appear in Things 3 where you can:
- Schedule them properly
- Add to projects
- Set priorities
- Actually get them done 📋✅

## Options

```bash
# Filter by tag (recommended)
tana-to-things --filter things

# Schedule all tasks for today
tana-to-things --filter things --when today

# Schedule for tomorrow
tana-to-things --filter things --when tomorrow

# Schedule for specific date
tana-to-things --filter things --when 2025-12-31

# Show tasks in Things after creation
tana-to-things --filter things --reveal
```

## What Gets Synced

From Tana to Things 3:

| Tana Element | Things 3 Destination |
|--------------|---------------------|
| Task title | Task title |
| Child text nodes | Notes |
| Child checkboxes | Checklist items |
| `#work`, `#urgent` tags | Tags |
| `#things`, `#task` tags | Filtered out |

## Tips

1. **Use consistent tagging**: Always use `#things` for tasks you want to sync
2. **Clean separation**: Keep meeting notes in Tana, actionable tasks in Things
3. **Batch sync**: Copy all your meeting notes and sync at once
4. **Review in Things**: After syncing, review and organize tasks in Things 3

## Create an Alias

Save typing by creating an alias:

```bash
echo 'alias ttt-reverse="uvx --from git+https://github.com/reify-nz/things-to-tana tana-to-things --filter things"' >> ~/.zshrc
source ~/.zshrc

# Now just use:
ttt-reverse
ttt-reverse --when today
```

## Troubleshooting

**Nothing happens:**
- Make sure you copied content from Tana first
- Check that tasks have the `#things` tag if using `--filter`

**Tasks don't appear:**
- Ensure Things 3 is installed and running
- On macOS, you may need to grant permission for the script to control Things

**Wrong content synced:**
- Make sure you're copying the right nodes from Tana
- Use `--filter things` to sync only tagged tasks

## Example

**In Tana:**
```
- [ ] Review Q4 report #things #work
  - Focus on revenue section
  - [ ] Check data accuracy
  - [ ] Update charts
```

**Command:**
```bash
tana-to-things --filter things --when today
```

**In Things 3:**
- Title: "Review Q4 report"
- Tags: work
- Notes: "Focus on revenue section"
- Checklist: "Check data accuracy", "Update charts"
- Scheduled: Today
