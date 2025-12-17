"""
Tana Paste Format Parser

Parses Tana Paste format (clipboard content) into structured TanaNode objects.
Supports parsing checkboxes, supertags, and hierarchical node structures.
"""

import re
from typing import List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class ParsedNode:
    """Represents a parsed node from Tana Paste format."""
    text: str
    supertags: List[str]
    checked: Optional[bool] = None
    children: List['ParsedNode'] = None
    
    def __post_init__(self):
        if self.children is None:
            self.children = []


def parse_tana_paste(content: str) -> List[ParsedNode]:
    """
    Parses Tana Paste format content into a list of ParsedNode objects.
    
    Args:
        content: Tana Paste format text (may start with %%tana%%)
    
    Returns:
        List of top-level ParsedNode objects
    """
    lines = content.strip().split('\n')
    
    # Skip %%tana%% header if present
    if lines and lines[0].strip() == '%%tana%%':
        lines = lines[1:]
    
    return _parse_lines(lines)


def _parse_lines(lines: List[str]) -> List[ParsedNode]:
    """
    Recursively parses lines into a tree structure.
    
    Args:
        lines: List of lines to parse
    
    Returns:
        List of ParsedNode objects
    """
    if not lines:
        return []
    
    nodes = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Skip empty lines
        if not line.strip():
            i += 1
            continue
        
        # Calculate indent level
        indent = _get_indent_level(line)
        
        # Parse the current line
        node = _parse_line(line)
        
        # Find children (lines with greater indent)
        j = i + 1
        child_lines = []
        while j < len(lines):
            child_indent = _get_indent_level(lines[j])
            if child_indent > indent:
                child_lines.append(lines[j])
                j += 1
            else:
                break
        
        # Recursively parse children
        if child_lines:
            node.children = _parse_lines(child_lines)
        
        nodes.append(node)
        i = j
    
    return nodes


def _get_indent_level(line: str) -> int:
    """
    Calculates the indentation level of a line.
    Each two spaces = one indent level.
    
    Args:
        line: The line to analyze
    
    Returns:
        Indent level (0 for no indent)
    """
    # Count leading spaces
    spaces = len(line) - len(line.lstrip(' '))
    return spaces // 2


def _parse_line(line: str) -> ParsedNode:
    """
    Parses a single line into a ParsedNode.
    Extracts checkbox state, text, and supertags.
    
    Args:
        line: Single line from Tana Paste format
    
    Returns:
        ParsedNode object
    """
    # Remove leading whitespace and bullet point
    content = line.lstrip(' ')
    if content.startswith('- '):
        content = content[2:]
    
    # Check for checkbox
    checked = None
    if content.startswith('[x] '):
        checked = True
        content = content[4:]
    elif content.startswith('[ ] '):
        checked = False
        content = content[4:]
    
    # Extract supertags
    supertags = []
    
    # Pattern for multi-word supertags: #[[tag name]]
    multi_word_pattern = r'#\[\[([^\]]+)\]\]'
    for match in re.finditer(multi_word_pattern, content):
        supertags.append(match.group(1))
    content = re.sub(multi_word_pattern, '', content)
    
    # Pattern for single-word supertags: #tagname
    single_word_pattern = r'#([a-zA-Z0-9_-]+)'
    for match in re.finditer(single_word_pattern, content):
        supertags.append(match.group(1))
    content = re.sub(single_word_pattern, '', content)
    
    # Clean up extra whitespace
    text = ' '.join(content.split()).strip()
    
    return ParsedNode(text=text, supertags=supertags, checked=checked)


def filter_by_supertag(nodes: List[ParsedNode], supertag: str) -> List[ParsedNode]:
    """
    Filters nodes to only include those with the specified supertag.
    Recursively checks children as well.
    
    Args:
        nodes: List of ParsedNode objects
        supertag: The supertag to filter by (e.g., "things")
    
    Returns:
        List of nodes that have the specified supertag
    """
    filtered = []
    
    for node in nodes:
        # Check if this node has the supertag
        if supertag in node.supertags:
            # Create a copy to avoid modifying original
            filtered_node = ParsedNode(
                text=node.text,
                supertags=node.supertags,
                checked=node.checked,
                children=node.children.copy() if node.children else []
            )
            filtered.append(filtered_node)
        else:
            # Check children recursively
            filtered_children = filter_by_supertag(node.children, supertag)
            if filtered_children:
                filtered.extend(filtered_children)
    
    return filtered
