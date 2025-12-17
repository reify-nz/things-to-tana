"""
Integration tests for Tana to Things 3 workflow
"""

import pytest
from tana_parser import parse_tana_paste, filter_by_supertag
from things_url_generator import generate_add_url
from tana_to_things import convert_node_to_things_url


def test_simple_workflow():
    """Test the basic workflow from Tana Paste to Things URL."""
    # Simulate Tana Paste content
    tana_content = """%%tana%%
- [ ] Buy groceries #things
  - Milk
  - Bread
  - Eggs"""
    
    # Parse
    nodes = parse_tana_paste(tana_content)
    assert len(nodes) == 1
    
    # Filter by supertag
    filtered = filter_by_supertag(nodes, "things")
    assert len(filtered) == 1
    
    # Convert to Things URL
    url = convert_node_to_things_url(filtered[0])
    
    # Verify URL structure
    assert url.startswith("things:///add?")
    assert "title=Buy%20groceries" in url
    assert "notes=" in url
    assert "checklist" not in url  # Children without checkboxes become notes


def test_workflow_with_checklist():
    """Test workflow with checklist items."""
    tana_content = """- [ ] Shopping list #things
  - [ ] Milk
  - [ ] Bread
  - [x] Eggs"""
    
    nodes = parse_tana_paste(tana_content)
    filtered = filter_by_supertag(nodes, "things")
    
    url = convert_node_to_things_url(filtered[0])
    
    assert "title=Shopping%20list" in url
    assert "checklist-items=" in url


def test_workflow_with_scheduling():
    """Test workflow with scheduling parameter."""
    tana_content = "- [ ] Review report #things"
    
    nodes = parse_tana_paste(tana_content)
    filtered = filter_by_supertag(nodes, "things")
    
    url = convert_node_to_things_url(filtered[0], when="today")
    
    assert "title=Review%20report" in url
    assert "when=today" in url


def test_workflow_with_tags():
    """Test that non-filter tags are preserved."""
    tana_content = "- [ ] Task #things #work #urgent"
    
    nodes = parse_tana_paste(tana_content)
    filtered = filter_by_supertag(nodes, "things")
    
    url = convert_node_to_things_url(filtered[0])
    
    # "things" and "task" should be filtered out
    # "work" and "urgent" should be preserved
    assert "tags=" in url
    assert "work" in url
    assert "urgent" in url


def test_workflow_multiple_tasks():
    """Test workflow with multiple tasks."""
    tana_content = """- [ ] Task 1 #things
- [ ] Task 2 #things
- [ ] Task 3 #other"""
    
    nodes = parse_tana_paste(tana_content)
    filtered = filter_by_supertag(nodes, "things")
    
    assert len(filtered) == 2
    
    url1 = convert_node_to_things_url(filtered[0])
    url2 = convert_node_to_things_url(filtered[1])
    
    assert "title=Task%201" in url1
    assert "title=Task%202" in url2


def test_workflow_nested_task_extraction():
    """Test that nested tasks with the supertag are extracted."""
    tana_content = """- Project without tag
  - [ ] Nested task #things
    - This is a note"""
    
    nodes = parse_tana_paste(tana_content)
    filtered = filter_by_supertag(nodes, "things")
    
    assert len(filtered) == 1
    assert filtered[0].text == "Nested task"
    
    url = convert_node_to_things_url(filtered[0])
    assert "title=Nested%20task" in url
    assert "notes=This%20is%20a%20note" in url


def test_workflow_mixed_children():
    """Test task with both notes and checklist items."""
    tana_content = """- [ ] Plan party #things
  - Venue: Community center
  - [ ] Send invitations
  - [ ] Order cake
  - Budget: $500"""
    
    nodes = parse_tana_paste(tana_content)
    filtered = filter_by_supertag(nodes, "things")
    
    url = convert_node_to_things_url(filtered[0])
    
    # Should have both notes and checklist
    assert "title=Plan%20party" in url
    assert "notes=" in url  # For non-checkbox children
    assert "checklist-items=" in url  # For checkbox children
