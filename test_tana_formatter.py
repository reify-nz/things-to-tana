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
