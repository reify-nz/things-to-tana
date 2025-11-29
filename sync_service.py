from typing import List, Dict, Any
from config import SUPERTAG_NAME, TANA_INBOX_NODE_ID, TANA_TODAY_NODE_ID
from models import TanaNode
from things_provider import ThingsProvider
from tana_client import TanaClient
from history_manager import HistoryManager

class SyncService:
    def __init__(self):
        self.things_provider = ThingsProvider()
        self.tana_client = TanaClient()
        self.history_manager = HistoryManager()

    def _convert_task_to_node(self, task: Dict[str, Any]) -> TanaNode:
        """
        Converts a Things 3 task dictionary to a TanaNode.
        """
        title = task.get('title', 'Untitled Task')
        notes = task.get('notes', '')
        tags = task.get('tags', [])
        # due_date = task.get('due_date') # Tana API might handle dates differently, or we put in name
        checklist = task.get('checklist', [])
        
        # Create the main node
        node = TanaNode(name=title)
        
        # Add configured supertag
        if SUPERTAG_NAME:
            node.add_supertag(SUPERTAG_NAME)
            
        # Add Things tags as Tana tags
        for tag in tags:
            node.add_supertag(tag)
            
        # Add notes as a child node
        if notes:
            # Split notes by line
            for line in notes.split('\n'):
                if line.strip():
                    node.add_child(TanaNode(name=line))
            
        # Add checklist items as children
        for item in checklist:
            item_title = item.get('title', '')
            item_status = item.get('status', '')
            # For now, checklist items are just child nodes. 
            # If we want them to be checkboxes, we might need a specific supertag or property.
            # We'll just add them as children for now.
            child = TanaNode(name=item_title)
            if item_status == 'completed':
                child.name = f"[x] {child.name}" # Visual indicator
            else:
                child.name = f"[ ] {child.name}"
            node.add_child(child)
            
        return node

    def sync_inbox(self):
        """
        Syncs uncompleted tasks from Things Inbox to Tana Inbox.
        """
        print("Syncing Inbox...")
        tasks = self.things_provider.get_inbox_tasks()
        self._process_tasks(tasks, TANA_INBOX_NODE_ID)

    def sync_today(self):
        """
        Syncs uncompleted tasks from Things Today to Tana Today (or Inbox if not configured).
        """
        print("Syncing Today...")
        tasks = self.things_provider.get_today_tasks()
        target_node = TANA_TODAY_NODE_ID if TANA_TODAY_NODE_ID else TANA_INBOX_NODE_ID
        self._process_tasks(tasks, target_node)

    def _process_tasks(self, tasks: List[Dict[str, Any]], target_node_id: str):
        nodes_to_send = []
        task_ids_to_mark = []

        for task in tasks:
            task_id = task.get('uuid')
            status = task.get('status')
            type_ = task.get('type')

            # Skip if already synced
            if self.history_manager.has_been_synced(task_id):
                continue

            # Skip if completed or canceled (One-way sync of active tasks)
            if status in ('completed', 'canceled'):
                continue
            
            # Skip projects (unless we want to handle them differently)
            if type_ == 'project':
                continue

            # Convert and prepare for sending
            node = self._convert_task_to_node(task)
            nodes_to_send.append(node)
            task_ids_to_mark.append(task_id)

        if not nodes_to_send:
            print("No new tasks to sync.")
            return

        # Send to Tana
        success = self.tana_client.send_nodes(nodes_to_send, target_node_id)
        
        # Update history if successful
        if success:
            for tid in task_ids_to_mark:
                self.history_manager.mark_as_synced(tid)
            print(f"Synced {len(nodes_to_send)} tasks.")
        else:
            print("Failed to sync tasks.")
