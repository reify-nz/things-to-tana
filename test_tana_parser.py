"""
Tests for Tana Paste Parser
"""

import pytest
from tana_parser import (
    parse_tana_paste,
    filter_by_supertag,
    ParsedNode,
    _get_indent_level,
    _parse_line
)


def test_parse_simple_node():
    """Test parsing a simple node without any special formatting."""
    content = "- Task title"
    nodes = parse_tana_paste(content)
    
    assert len(nodes) == 1
    assert nodes[0].text == "Task title"
    assert nodes[0].checked is None
    assert nodes[0].supertags == []
    assert nodes[0].children == []


def test_parse_with_header():
    """Test parsing content that starts with %%tana%% header."""
    content = """%%tana%%
- Task title"""
    nodes = parse_tana_paste(content)
    
    assert len(nodes) == 1
    assert nodes[0].text == "Task title"


def test_parse_unchecked_task():
    """Test parsing an unchecked checkbox task."""
    content = "- [ ] Uncompleted task"
    nodes = parse_tana_paste(content)
    
    assert len(nodes) == 1
    assert nodes[0].text == "Uncompleted task"
    assert nodes[0].checked is False


def test_parse_checked_task():
    """Test parsing a checked checkbox task."""
    content = "- [x] Completed task"
    nodes = parse_tana_paste(content)
    
    assert len(nodes) == 1
    assert nodes[0].text == "Completed task"
    assert nodes[0].checked is True


def test_parse_single_word_supertag():
    """Test parsing a node with a single-word supertag."""
    content = "- Task title #work"
    nodes = parse_tana_paste(content)
    
    assert len(nodes) == 1
    assert nodes[0].text == "Task title"
    assert "work" in nodes[0].supertags


def test_parse_multi_word_supertag():
    """Test parsing a node with a multi-word supertag."""
    content = "- Task title #[[deep work]]"
    nodes = parse_tana_paste(content)
    
    assert len(nodes) == 1
    assert nodes[0].text == "Task title"
    assert "deep work" in nodes[0].supertags


def test_parse_multiple_supertags():
    """Test parsing a node with multiple supertags."""
    content = "- Task title #work #important #[[high priority]]"
    nodes = parse_tana_paste(content)
    
    assert len(nodes) == 1
    assert nodes[0].text == "Task title"
    assert "work" in nodes[0].supertags
    assert "important" in nodes[0].supertags
    assert "high priority" in nodes[0].supertags


def test_parse_complex_node():
    """Test parsing a node with checkbox and supertags."""
    content = "- [ ] Buy groceries #things #personal"
    nodes = parse_tana_paste(content)
    
    assert len(nodes) == 1
    assert nodes[0].text == "Buy groceries"
    assert nodes[0].checked is False
    assert "things" in nodes[0].supertags
    assert "personal" in nodes[0].supertags


def test_parse_with_children():
    """Test parsing a node with child nodes."""
    content = """- Parent task
  - Child task 1
  - Child task 2"""
    nodes = parse_tana_paste(content)
    
    assert len(nodes) == 1
    assert nodes[0].text == "Parent task"
    assert len(nodes[0].children) == 2
    assert nodes[0].children[0].text == "Child task 1"
    assert nodes[0].children[1].text == "Child task 2"


def test_parse_nested_children():
    """Test parsing deeply nested children."""
    content = """- Level 1
  - Level 2
    - Level 3"""
    nodes = parse_tana_paste(content)
    
    assert len(nodes) == 1
    assert nodes[0].text == "Level 1"
    assert len(nodes[0].children) == 1
    assert nodes[0].children[0].text == "Level 2"
    assert len(nodes[0].children[0].children) == 1
    assert nodes[0].children[0].children[0].text == "Level 3"


def test_parse_multiple_top_level_nodes():
    """Test parsing multiple top-level nodes."""
    content = """- Task 1
- Task 2
- Task 3"""
    nodes = parse_tana_paste(content)
    
    assert len(nodes) == 3
    assert nodes[0].text == "Task 1"
    assert nodes[1].text == "Task 2"
    assert nodes[2].text == "Task 3"


def test_parse_complex_structure():
    """Test parsing a complex structure with all features."""
    content = """%%tana%%
- [ ] Main task #things #work
  - First note
  - [x] Completed subtask
  - [ ] Pending subtask #urgent"""
    
    nodes = parse_tana_paste(content)
    
    assert len(nodes) == 1
    main = nodes[0]
    assert main.text == "Main task"
    assert main.checked is False
    assert "things" in main.supertags
    assert "work" in main.supertags
    
    assert len(main.children) == 3
    assert main.children[0].text == "First note"
    assert main.children[0].checked is None
    
    assert main.children[1].text == "Completed subtask"
    assert main.children[1].checked is True
    
    assert main.children[2].text == "Pending subtask"
    assert main.children[2].checked is False
    assert "urgent" in main.children[2].supertags


def test_filter_by_supertag():
    """Test filtering nodes by supertag."""
    content = """- Task 1 #things
- Task 2 #other
- Task 3 #things"""
    
    nodes = parse_tana_paste(content)
    filtered = filter_by_supertag(nodes, "things")
    
    assert len(filtered) == 2
    assert filtered[0].text == "Task 1"
    assert filtered[1].text == "Task 3"


def test_filter_by_supertag_in_children():
    """Test filtering finds supertags in children."""
    content = """- Parent without tag
  - Child with tag #things"""
    
    nodes = parse_tana_paste(content)
    filtered = filter_by_supertag(nodes, "things")
    
    assert len(filtered) == 1
    assert filtered[0].text == "Child with tag"


def test_filter_no_matches():
    """Test filtering with no matches."""
    content = """- Task 1 #work
- Task 2 #personal"""
    
    nodes = parse_tana_paste(content)
    filtered = filter_by_supertag(nodes, "things")
    
    assert len(filtered) == 0


def test_get_indent_level():
    """Test indent level calculation."""
    assert _get_indent_level("- Task") == 0
    assert _get_indent_level("  - Task") == 1
    assert _get_indent_level("    - Task") == 2
    assert _get_indent_level("      - Task") == 3


def test_parse_line_basic():
    """Test basic line parsing."""
    node = _parse_line("- Simple task")
    assert node.text == "Simple task"
    assert node.checked is None
    assert node.supertags == []


def test_parse_line_with_checkbox():
    """Test line parsing with checkbox."""
    node = _parse_line("- [ ] Unchecked")
    assert node.text == "Unchecked"
    assert node.checked is False
    
    node = _parse_line("- [x] Checked")
    assert node.text == "Checked"
    assert node.checked is True


def test_parse_line_with_supertags():
    """Test line parsing with supertags."""
    node = _parse_line("- Task #tag1 #[[multi word]]")
    assert node.text == "Task"
    assert "tag1" in node.supertags
    assert "multi word" in node.supertags


def test_parse_empty_lines():
    """Test that empty lines are skipped."""
    content = """- Task 1

- Task 2

"""
    nodes = parse_tana_paste(content)
    assert len(nodes) == 2


def test_parse_whitespace_handling():
    """Test that extra whitespace is handled correctly."""
    content = "- Task   with   extra   spaces   #tag"
    nodes = parse_tana_paste(content)
    
    assert nodes[0].text == "Task with extra spaces"
    assert "tag" in nodes[0].supertags
