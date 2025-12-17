#!/usr/bin/env python3
"""
Tana to Things 3 Sync

Syncs tasks from Tana (via clipboard) to Things 3 using the Things URL scheme.
Reads Tana Paste format from clipboard and creates tasks in Things 3.

Usage:
    python tana_to_things.py [--filter SUPERTAG] [--when WHEN] [--reveal]

Examples:
    # Sync all tasks from clipboard
    python tana_to_things.py
    
    # Only sync tasks tagged with #things
    python tana_to_things.py --filter things
    
    # Schedule all tasks for today
    python tana_to_things.py --when today
    
    # Sync and reveal in Things
    python tana_to_things.py --filter things --reveal
"""

import sys
import argparse
import pyperclip
import time
from typing import List, Optional
from tana_parser import parse_tana_paste, filter_by_supertag, ParsedNode
from things_url_generator import generate_add_url, open_things_url


def convert_node_to_things_url(
    node: ParsedNode,
    when: Optional[str] = None,
    reveal: bool = False
) -> str:
    """
    Converts a ParsedNode to a Things 3 URL.
    
    Args:
        node: The parsed node from Tana
        when: When to schedule the task
        reveal: Whether to reveal the task in Things
    
    Returns:
        Things 3 URL string
    """
    title = node.text
    
    # Collect child text as notes
    notes_lines = []
    checklist_items = []
    
    for child in node.children:
        # If child has a checkbox, treat it as a checklist item
        if child.checked is not None:
            checklist_items.append(child.text)
        else:
            # Otherwise, treat as note
            notes_lines.append(child.text)
    
    notes = '\n'.join(notes_lines) if notes_lines else None
    
    # Filter out the "things" tag if present (it's just for filtering)
    # and any other Tana-specific tags you might not want in Things
    tags = [tag for tag in node.supertags if tag not in ['things', 'task']]
    
    return generate_add_url(
        title=title,
        notes=notes,
        when=when,
        tags=tags if tags else None,
        checklist_items=checklist_items if checklist_items else None,
        reveal=reveal
    )


def sync_nodes_to_things(
    nodes: List[ParsedNode],
    when: Optional[str] = None,
    reveal: bool = False,
    delay: float = 0.5
) -> int:
    """
    Syncs a list of nodes to Things 3.
    
    Args:
        nodes: List of ParsedNode objects to sync
        when: When to schedule the tasks
        reveal: Whether to reveal each task in Things
        delay: Delay between opening URLs (seconds)
    
    Returns:
        Number of tasks successfully synced
    """
    if not nodes:
        print("No nodes to sync.")
        return 0
    
    print(f"Syncing {len(nodes)} task(s) to Things 3...")
    
    success_count = 0
    for i, node in enumerate(nodes, 1):
        try:
            url = convert_node_to_things_url(node, when=when, reveal=reveal)
            print(f"  [{i}/{len(nodes)}] {node.text}")
            
            if open_things_url(url):
                success_count += 1
                # Small delay between tasks to avoid overwhelming Things
                # Skip delay after the last task
                if i < len(nodes):
                    time.sleep(delay)
            else:
                print(f"    ⚠️  Failed to open URL for: {node.text}")
        except Exception as e:
            print(f"    ❌ Error processing task: {e}")
    
    return success_count


def main():
    """Main entry point for the Tana to Things 3 sync script."""
    parser = argparse.ArgumentParser(
        description="Sync tasks from Tana (clipboard) to Things 3",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                           # Sync all tasks from clipboard
  %(prog)s --filter things           # Only sync tasks tagged with #things
  %(prog)s --when today --reveal     # Schedule for today and show in Things
        """
    )
    
    parser.add_argument(
        '--filter',
        metavar='SUPERTAG',
        help='Only sync tasks with this supertag (e.g., "things")'
    )
    
    parser.add_argument(
        '--when',
        metavar='WHEN',
        help='Schedule tasks (e.g., "today", "tomorrow", "2025-12-31")'
    )
    
    parser.add_argument(
        '--reveal',
        action='store_true',
        help='Show each task in Things after creation'
    )
    
    parser.add_argument(
        '--delay',
        type=float,
        default=0.5,
        metavar='SECONDS',
        help='Delay between tasks in seconds (default: 0.5)'
    )
    
    args = parser.parse_args()
    
    # Read from clipboard
    print("Reading Tana Paste content from clipboard...")
    try:
        clipboard_content = pyperclip.paste()
    except Exception as e:
        print(f"❌ Error reading clipboard: {e}")
        return 1
    
    if not clipboard_content or not clipboard_content.strip():
        print("❌ Clipboard is empty. Please copy Tana nodes first.")
        return 1
    
    # Parse Tana Paste format
    try:
        nodes = parse_tana_paste(clipboard_content)
    except Exception as e:
        print(f"❌ Error parsing Tana Paste content: {e}")
        print("\nMake sure you copied valid Tana nodes.")
        return 1
    
    if not nodes:
        print("❌ No nodes found in clipboard content.")
        return 1
    
    print(f"✓ Found {len(nodes)} top-level node(s)")
    
    # Filter by supertag if specified
    if args.filter:
        print(f"Filtering by supertag: #{args.filter}")
        nodes = filter_by_supertag(nodes, args.filter)
        
        if not nodes:
            print(f"❌ No nodes found with supertag #{args.filter}")
            return 1
        
        print(f"✓ Found {len(nodes)} node(s) with #{args.filter}")
    
    # Sync to Things 3
    success_count = sync_nodes_to_things(
        nodes,
        when=args.when,
        reveal=args.reveal,
        delay=args.delay
    )
    
    if success_count == len(nodes):
        print(f"\n✅ Successfully synced {success_count} task(s) to Things 3!")
        return 0
    else:
        print(f"\n⚠️  Synced {success_count}/{len(nodes)} task(s)")
        return 1


if __name__ == "__main__":
    sys.exit(main())
