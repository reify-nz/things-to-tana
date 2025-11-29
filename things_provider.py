import things3.things3_api as things
from typing import List, Dict, Any

class ThingsProvider:
    def get_inbox_tasks(self) -> List[Dict[str, Any]]:
        """
        Fetches tasks from Things 3 Inbox.
        """
        return things.inbox()

    def get_today_tasks(self) -> List[Dict[str, Any]]:
        """
        Fetches tasks from Things 3 Today list.
        """
        return things.today()

    def get_all_tasks(self) -> List[Dict[str, Any]]:
        """
        Fetches all tasks.
        """
        return things.todos()
