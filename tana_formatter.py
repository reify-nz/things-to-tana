from dataclasses import dataclass, field
from typing import List, Optional, Union

@dataclass
class TanaNode:
    text: str
    children: List['TanaNode'] = field(default_factory=list)
    checked: Optional[bool] = None  # None = no checkbox, False = [ ], True = [x]
    
    def add_child(self, child: 'TanaNode'):
        self.children.append(child)
        return self

    def to_string(self, indent_level: int = 0) -> str:
        indent = "  " * indent_level
        checkbox = ""
        if self.checked is not None:
            checkbox = "[x] " if self.checked else "[ ] "
        
        lines = [f"{indent}- {checkbox}{self.text}"]
        for child in self.children:
            lines.append(child.to_string(indent_level + 1))
        return "\n".join(lines)

def to_tana_paste(nodes: List[TanaNode]) -> str:
    """
    Converts a list of TanaNodes into a Tana Paste formatted string.
    Prepends %%tana%% to the output.
    """
    output = ["%%tana%%"]
    for node in nodes:
        output.append(node.to_string(0))
    return "\n".join(output)

def tana_date(date_str: str) -> str:
    """
    Formats a date string into Tana date format [[date:YYYY-MM-DD]].
    Assumes date_str is already in a compatible format or is a simple YYYY-MM-DD.
    """
    return f"[[date:{date_str}]]"

def tana_tag(tag_name: str) -> str:
    """
    Formats a tag. Handles multi-word tags by wrapping in [[ ]].
    """
    if " " in tag_name:
        return f"#[[{tag_name}]]"
    return f"#{tag_name}"

def tana_field(name: str, value: str) -> str:
    """
    Formats a field as 'name:: value'.
    """
    return f"{name}:: {value}"
