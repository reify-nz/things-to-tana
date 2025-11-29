import pytest
from tana_formatter import TanaNode, to_tana_paste, tana_date, tana_tag, tana_field

def test_tana_node_structure():
    node = TanaNode(text="Parent")
    child = TanaNode(text="Child")
    node.add_child(child)
    
    assert node.text == "Parent"
    assert len(node.children) == 1
    assert node.children[0].text == "Child"

def test_tana_paste_format():
    node = TanaNode(text="Task 1")
    node.add_child(TanaNode(text="Subtask 1"))
    
    output = to_tana_paste([node])
    expected = "%%tana%%\n- Task 1\n  - Subtask 1"
    assert output == expected

def test_checkbox_rendering():
    node = TanaNode(text="Task", checked=True)
    assert "[x] Task" in node.to_string()
    
    node_unchecked = TanaNode(text="Task", checked=False)
    assert "[ ] Task" in node_unchecked.to_string()
    
    node_none = TanaNode(text="Task", checked=None)
    assert "- Task" in node_none.to_string()
    assert "[ ]" not in node_none.to_string()
    assert "[x]" not in node_none.to_string()

def test_tana_date():
    assert tana_date("2023-10-27") == "[[date:2023-10-27]]"

def test_tana_tag():
    assert tana_tag("work") == "#work"
    assert tana_tag("deep work") == "#[[deep work]]"

def test_tana_field():
    assert tana_field("Status", "Active") == "Status:: Active"

def test_supertag_single_word():
    """Test that a single-word supertag is formatted correctly."""
    node = TanaNode(text="Task")
    node.add_supertag("work")
    
    output = node.to_string()
    assert "#work" in output
    assert "Task" in output
    # Supertag should come after the text
    assert output.index("Task") < output.index("#work")
    # Should match the expected format
    assert output == "- Task #work"

def test_supertag_multi_word():
    """Test that a multi-word supertag is formatted correctly."""
    node = TanaNode(text="Task")
    node.add_supertag("deep work")
    
    output = node.to_string()
    assert "#[[deep work]]" in output
    assert "Task" in output
    # Supertag should come after the text
    assert output.index("Task") < output.index("#[[deep work]]")
    # Should match the expected format
    assert output == "- Task #[[deep work]]"

def test_supertag_multiple():
    """Test that multiple supertags are formatted correctly."""
    node = TanaNode(text="Task")
    node.add_supertag("work")
    node.add_supertag("important")
    
    output = node.to_string()
    assert "#work" in output
    assert "#important" in output
    # Both tags should appear after the text
    assert output.index("Task") < output.index("#work")
    assert output.index("Task") < output.index("#important")

def test_supertag_with_checkbox():
    """Test that supertags work correctly with checkboxes."""
    node = TanaNode(text="Task", checked=False)
    node.add_supertag("work")
    
    output = node.to_string()
    assert "[ ]" in output
    assert "#work" in output
    assert "Task" in output
    # Checkbox should come first, then text, then supertag
    assert output.index("[ ]") < output.index("Task")
    assert output.index("Task") < output.index("#work")
    # Should match the expected format
    assert output == "- [ ] Task #work"

def test_supertag_with_checked_checkbox():
    """Test that supertags work correctly with checked checkboxes."""
    node = TanaNode(text="Task", checked=True)
    node.add_supertag("work")
    
    output = node.to_string()
    assert "[x]" in output
    assert "#work" in output
    assert "Task" in output
    # Should match the expected format
    assert output == "- [x] Task #work"

def test_supertag_duplicate_prevention():
    """Test that adding the same supertag twice doesn't create duplicates."""
    node = TanaNode(text="Task")
    node.add_supertag("work")
    node.add_supertag("work")
    
    output = node.to_string()
    # Should only appear once
    assert output.count("#work") == 1

def test_supertag_in_paste_format():
    """Test that supertags are included in the full Tana paste format."""
    node = TanaNode(text="Task")
    node.add_supertag("work")
    
    output = to_tana_paste([node])
    assert "%%tana%%" in output
    assert "#work" in output
    assert "Task" in output

def test_supertag_with_children():
    """Test that supertags work correctly with child nodes."""
    node = TanaNode(text="Parent")
    node.add_supertag("work")
    node.add_child(TanaNode(text="Child"))
    
    output = node.to_string()
    assert "#work" in output
    assert "Parent" in output
    assert "Child" in output
    # Child should be indented
    assert "  - Child" in output

def test_supertag_complex():
    """Test a complex node with checkbox, supertags, and children."""
    node = TanaNode(text="Main Task", checked=False)
    node.add_supertag("work")
    node.add_supertag("important")
    node.add_child(TanaNode(text="Subtask 1", checked=True))
    node.add_child(TanaNode(text="Subtask 2"))
    
    output = node.to_string()
    assert "[ ]" in output
    assert "#work" in output
    assert "#important" in output
    assert "Main Task" in output
    assert "[x]" in output  # From child
    assert "Subtask 1" in output
    assert "Subtask 2" in output
