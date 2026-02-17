"""
Things 3 URL Scheme Generator

Generates Things 3 URL scheme URLs for adding tasks.
Supports title, notes, tags, when (scheduling), deadline, and checklist items.
"""

from typing import List, Optional
from urllib.parse import quote


def generate_add_url(
    title: str,
    notes: Optional[str] = None,
    when: Optional[str] = None,
    deadline: Optional[str] = None,
    tags: Optional[List[str]] = None,
    checklist_items: Optional[List[str]] = None,
    list_id: Optional[str] = None,
    reveal: bool = False
) -> str:
    """
    Generates a Things 3 URL to add a new task.
    
    Args:
        title: Task title (required)
        notes: Task notes/description
        when: When to schedule (e.g., "today", "tomorrow", "2025-12-31")
        deadline: Due date in YYYY-MM-DD format
        tags: List of tag names
        checklist_items: List of checklist item titles
        list_id: Destination list ID (optional, defaults to Inbox)
        reveal: Whether to show the task in Things after creation
    
    Returns:
        Things 3 URL string
    
    Example:
        >>> generate_add_url("Buy milk", notes="Low fat", when="today", tags=["groceries"])
        'things:///add?title=Buy%20milk&notes=Low%20fat&when=today&tags=groceries'
    """
    if not title:
        raise ValueError("Title is required")
    
    # Start building parameters
    params = [f"title={quote(title)}"]
    
    if notes:
        params.append(f"notes={quote(notes)}")
    
    if when:
        params.append(f"when={quote(when)}")
    
    if deadline:
        params.append(f"deadline={quote(deadline)}")
    
    if tags:
        # Tags are comma-separated
        tags_str = ','.join(tags)
        params.append(f"tags={quote(tags_str)}")
    
    if checklist_items:
        # Checklist items are newline-separated
        checklist_str = '\n'.join(checklist_items)
        params.append(f"checklist-items={quote(checklist_str)}")
    
    if list_id:
        params.append(f"list={quote(list_id)}")
    
    if reveal:
        params.append("reveal=true")
    
    # Construct URL
    url = "things:///add?" + "&".join(params)
    return url


def open_things_url(url: str) -> bool:
    """
    Opens a Things 3 URL using the system's URL handler.
    
    Args:
        url: Things 3 URL to open
    
    Returns:
        True if successful, False otherwise
    """
    import subprocess
    import sys
    
    try:
        if sys.platform == 'darwin':  # macOS
            subprocess.run(['open', url], check=True)
            return True
        else:
            print(f"Warning: URL opening is only supported on macOS")
            print(f"Please open this URL manually: {url}")
            return False
    except subprocess.CalledProcessError as e:
        print(f"Error opening URL: {e}")
        return False
    except FileNotFoundError:
        print(f"Error: 'open' command not found")
        return False
