import pytest
from models import TanaNode
from history_manager import HistoryManager
import os
import json

# --- Models Tests ---
def test_tana_node_api_payload():
    node = TanaNode(name="Task 1")
    node.add_child(TanaNode(name="Subtask 1"))
    node.add_supertag("task")
    
    payload = node.to_api_payload()
    
    assert payload["name"] == "Task 1"
    assert len(payload["children"]) == 1
    assert payload["children"][0]["name"] == "Subtask 1"
    assert payload["supertags"][0]["name"] == "task"

# --- History Manager Tests ---
def test_history_manager(tmp_path):
    # Use a temporary file for history
    history_file = tmp_path / "test_history.json"
    manager = HistoryManager(str(history_file))
    
    assert manager.has_been_synced("123") == False
    
    manager.mark_as_synced("123")
    assert manager.has_been_synced("123") == True
    
    # Reload from file
    manager2 = HistoryManager(str(history_file))
    assert manager2.has_been_synced("123") == True
