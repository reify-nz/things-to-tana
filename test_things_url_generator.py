"""
Tests for Things 3 URL Generator
"""

import pytest
from things_url_generator import generate_add_url


def test_generate_simple_task():
    """Test generating URL for a simple task."""
    url = generate_add_url("Buy milk")
    assert url.startswith("things:///add?")
    assert "title=Buy%20milk" in url


def test_generate_task_with_notes():
    """Test generating URL for a task with notes."""
    url = generate_add_url("Buy milk", notes="Low fat")
    assert "title=Buy%20milk" in url
    assert "notes=Low%20fat" in url


def test_generate_task_with_when():
    """Test generating URL for a scheduled task."""
    url = generate_add_url("Buy milk", when="today")
    assert "title=Buy%20milk" in url
    assert "when=today" in url


def test_generate_task_with_deadline():
    """Test generating URL for a task with deadline."""
    url = generate_add_url("Buy milk", deadline="2025-12-31")
    assert "title=Buy%20milk" in url
    assert "deadline=2025-12-31" in url


def test_generate_task_with_single_tag():
    """Test generating URL for a task with one tag."""
    url = generate_add_url("Buy milk", tags=["groceries"])
    assert "title=Buy%20milk" in url
    assert "tags=groceries" in url


def test_generate_task_with_multiple_tags():
    """Test generating URL for a task with multiple tags."""
    url = generate_add_url("Buy milk", tags=["groceries", "urgent"])
    assert "title=Buy%20milk" in url
    assert "tags=groceries%2Curgent" in url


def test_generate_task_with_checklist():
    """Test generating URL for a task with checklist items."""
    url = generate_add_url("Shopping", checklist_items=["Milk", "Bread", "Eggs"])
    assert "title=Shopping" in url
    assert "checklist-items=Milk%0ABread%0AEggs" in url


def test_generate_task_with_list_id():
    """Test generating URL for a task with specific list."""
    url = generate_add_url("Buy milk", list_id="work-inbox")
    assert "title=Buy%20milk" in url
    assert "list=work-inbox" in url


def test_generate_task_with_reveal():
    """Test generating URL for a task with reveal flag."""
    url = generate_add_url("Buy milk", reveal=True)
    assert "title=Buy%20milk" in url
    assert "reveal=true" in url


def test_generate_task_complex():
    """Test generating URL for a complex task with all parameters."""
    url = generate_add_url(
        title="Complete project report",
        notes="Include Q4 financials and market analysis",
        when="tomorrow",
        deadline="2025-12-25",
        tags=["work", "urgent"],
        checklist_items=["Gather data", "Write draft", "Review"],
        reveal=True
    )
    
    assert "title=Complete%20project%20report" in url
    assert "notes=Include%20Q4%20financials" in url
    assert "when=tomorrow" in url
    assert "deadline=2025-12-25" in url
    assert "tags=work%2Curgent" in url
    assert "checklist-items=" in url
    assert "reveal=true" in url


def test_generate_task_special_characters():
    """Test URL encoding of special characters."""
    url = generate_add_url(
        "Task & Work",
        notes="Review @ 3pm",
        tags=["high-priority"]
    )
    
    assert "title=Task%20%26%20Work" in url
    assert "notes=Review%20%40%203pm" in url


def test_generate_task_empty_title_raises():
    """Test that empty title raises ValueError."""
    with pytest.raises(ValueError, match="Title is required"):
        generate_add_url("")


def test_generate_task_none_title_raises():
    """Test that None title raises ValueError."""
    with pytest.raises(ValueError, match="Title is required"):
        generate_add_url(None)


def test_generate_task_with_multiline_notes():
    """Test generating URL for a task with multi-line notes."""
    url = generate_add_url(
        "Shopping list",
        notes="Remember to:\n- Check prices\n- Use coupons"
    )
    
    assert "title=Shopping%20list" in url
    assert "notes=" in url


def test_generate_task_empty_tags_list():
    """Test that empty tags list is handled correctly."""
    url = generate_add_url("Task", tags=[])
    # Empty tags should not add tags parameter
    assert "title=Task" in url
    # tags parameter should not be present or should be empty


def test_generate_task_empty_checklist():
    """Test that empty checklist is handled correctly."""
    url = generate_add_url("Task", checklist_items=[])
    assert "title=Task" in url
    # checklist-items parameter should not be present or should be empty


def test_url_format():
    """Test that generated URL has correct format."""
    url = generate_add_url("Test")
    
    # Should start with things:///add?
    assert url.startswith("things:///add?")
    
    # Should contain title parameter
    assert "title=" in url
    
    # Should use & to separate parameters
    if "&" in url:
        # If there are multiple parameters
        parts = url.split("?", 1)[1].split("&")
        for part in parts:
            assert "=" in part, f"Invalid parameter format: {part}"
