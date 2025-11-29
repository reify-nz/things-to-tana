import pyperclip
import sys
from tana_formatter import TanaNode, to_tana_paste, tana_date
from things_provider import ThingsProvider
from config import SUPERTAG_NAME, TANA_API_TOKEN
from sync_service import SyncService


def is_api_token_valid():
    """
    Checks if TANA_API_TOKEN is configured and valid.
    Returns False if token is None, empty, or the placeholder value.
    """
    if not TANA_API_TOKEN:
        return False
    if TANA_API_TOKEN == "YOUR_API_TOKEN_HERE":
        return False
    return True


def get_things_tasks(scope="today"):
    """
    Fetches tasks from Things 3 based on scope.
    Scope can be 'today', 'inbox', or 'all'.
    """
    provider = ThingsProvider()
    if scope == "today":
        return provider.get_today_tasks()
    elif scope == "inbox":
        return provider.get_inbox_tasks()
    else:
        # For 'all', we might want to be careful. get_all_tasks() returns all.
        return provider.get_all_tasks()


def convert_task_to_node(task) -> TanaNode:
    """
    Converts a Things 3 task dictionary to a TanaNode.
    """
    title = task.get('title', 'Untitled Task')
    notes = task.get('notes', '')
    tags = task.get('tags', [])
    due_date = task.get('due_date')
    checklist = task.get('checklist', [])
    status = task.get('status', '')

    # Create the main node
    node_text = title

    # Add due date to text if present
    if due_date:
        node_text += f" {tana_date(due_date)}"

    # Determine checkbox state
    checked = False
    if status == 'completed':
        checked = True
    elif status == 'canceled':
        # Tana doesn't have a 'canceled' state for checkboxes natively in paste,
        # but we can mark it checked or add a tag. Let's just mark checked for now.
        checked = True
        node_text += " #canceled"

    node = TanaNode(text=node_text, checked=checked)

    # Add configured supertag
    if SUPERTAG_NAME:
        node.add_supertag(SUPERTAG_NAME)

    # Add tags as supertags (proper Tana format)
    for tag in tags:
        node.add_supertag(tag)

    # Add notes as a child node if they exist
    if notes:
        # Split notes by line to preserve structure
        for line in notes.split('\n'):
            if line.strip():
                node.add_child(TanaNode(text=line))

    # Add checklist items as children
    for item in checklist:
        item_title = item.get('title', '')
        item_status = item.get('status', '')
        item_checked = (item_status == 'completed')
        node.add_child(TanaNode(text=item_title, checked=item_checked))

    return node


def main():
    scope = "today"
    if len(sys.argv) > 1:
        scope = sys.argv[1]

    # Check if API token is configured
    if is_api_token_valid():
        # API Sync Mode
        print(f"Using API sync mode (TANA_API_TOKEN configured)")
        print(f"Syncing '{scope}' tasks from Things 3 to Tana...")

        service = SyncService()

        if scope == "inbox":
            service.sync_inbox()
        elif scope == "today":
            service.sync_today()
        elif scope == "all":
            service.sync_inbox()
            service.sync_today()
        else:
            print(f"Unknown scope: {scope}. Use 'inbox', 'today', or 'all'.")
    else:
        # Clipboard Sync Mode
        print(f"Using clipboard sync mode (no valid TANA_API_TOKEN)")
        print(f"Fetching '{scope}' tasks from Things 3...")

        try:
            tasks = get_things_tasks(scope)
        except Exception as e:
            print(f"Error fetching tasks: {e}")
            print("Make sure Things 3 is running and you have permissions.")
            return

        if not tasks:
            print("No tasks found.")
            return

        tana_nodes = []
        for task in tasks:
            # Filter out projects if they appear in the list (things3-api might return them)
            if task.get('type') == 'project':
                continue
            tana_nodes.append(convert_task_to_node(task))

        tana_paste_text = to_tana_paste(tana_nodes)

        try:
            pyperclip.copy(tana_paste_text)
            print("Successfully copied Tana Paste format to clipboard!")
            print("Go to Tana and paste (Cmd+V).")
        except Exception as e:
            print(f"Could not copy to clipboard: {e}")
            print("Here is the output:\n")
            print(tana_paste_text)


if __name__ == "__main__":
    main()
