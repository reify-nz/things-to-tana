from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

@dataclass
class TanaNode:
    name: str
    description: Optional[str] = None
    children: List['TanaNode'] = field(default_factory=list)
    supertags: List[str] = field(default_factory=list)
    checked: Optional[bool] = None
    
    def add_child(self, child: 'TanaNode'):
        self.children.append(child)
        return self

    def add_supertag(self, tag: str):
        if tag not in self.supertags:
            self.supertags.append(tag)
        return self

    def to_api_payload(self) -> Dict[str, Any]:
        """
        Converts the node to the Tana Input API JSON format.
        """
        payload = {
            "name": self.name
        }
        
        if self.description:
            payload["description"] = self.description
            
        if self.supertags:
            # API expects supertags as an array of objects with 'id'
            # The tag value should be the node ID of the supertag in Tana
            payload["supertags"] = [{"id": tag} for tag in self.supertags]
            
        if self.children:
            payload["children"] = [child.to_api_payload() for child in self.children]
            
        if self.checked is not None:
            # The API documentation for checkboxes is a bit sparse, 
            # but often it's handled via a supertag or specific field.
            # For now, we'll append status to name if it's not supported directly,
            # OR we can try to set a 'checked' property if the API supports it.
            # Based on research, 'checked' might not be a direct property of a plain node 
            # unless it's a checkbox node type. 
            # Let's assume we create a plain node. If it needs to be a checkbox, 
            # we might need to set a specific supertag or property.
            # For simplicity in this MVP, we will rely on the supertag to define it as a task.
            pass

        return payload

    def to_tana_paste(self, indent_level: int = 0) -> str:
        """
        Legacy/Debug: Converts to Tana Paste format.
        """
        indent = "  " * indent_level
        checkbox = ""
        if self.checked is not None:
            checkbox = "[x] " if self.checked else "[ ] "
        
        tags = ""
        for tag in self.supertags:
            if " " in tag:
                tags += f" #[[{tag}]]"
            else:
                tags += f" #{tag}"

        lines = [f"{indent}- {checkbox}{self.name}{tags}"]
        if self.description:
             # Description usually goes as a child or inline? 
             # In Tana Paste, it's often a child node or just extra text.
             # Let's add it as a child for clarity in paste format.
             lines.append(f"{indent}  - {self.description}")

        for child in self.children:
            lines.append(child.to_tana_paste(indent_level + 1))
        return "\n".join(lines)
