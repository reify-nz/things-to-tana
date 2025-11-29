import things3.things3_api as things
import pyperclip
import sys
from tana_formatter import TanaNode, to_tana_paste, tana_date, tana_tag, tana_field

def get_things_tasks(scope="today"):
    """
    Fetches tasks from Things 3 based on scope.
    Scope can be 'today', 'inbox', or 'all'.
    """
    if scope == "today":
        return things.today()
    elif scope == "inbox":
        return things.inbox()
    else:
        # For 'all', we might want to be careful. things.todos() returns all.
        return things.todos()

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
    
    # Add tags
    for tag in tags:
        node_text += f" {tana_tag(tag)}"
    
    # Add due date
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
