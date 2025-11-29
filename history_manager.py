import json
import os
from typing import Set

HISTORY_FILE = "history.json"

class HistoryManager:
    def __init__(self, file_path: str = HISTORY_FILE):
        self.file_path = file_path
        self.synced_ids: Set[str] = self._load_history()

    def _load_history(self) -> Set[str]:
        if not os.path.exists(self.file_path):
            return set()
        try:
            with open(self.file_path, 'r') as f:
                data = json.load(f)
                return set(data.get("synced_ids", []))
        except (json.JSONDecodeError, IOError):
            return set()

    def _save_history(self):
        try:
            with open(self.file_path, 'w') as f:
                json.dump({"synced_ids": list(self.synced_ids)}, f, indent=2)
        except IOError as e:
            print(f"Warning: Could not save history: {e}")

    def has_been_synced(self, task_id: str) -> bool:
        return task_id in self.synced_ids

    def mark_as_synced(self, task_id: str):
        self.synced_ids.add(task_id)
        self._save_history()
