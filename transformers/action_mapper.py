from typing import Dict, Any
from .base_transformer import BaseTransformer

class ActionMapper(BaseTransformer):
    """Maps actions from vendor to universal and vice versa."""

    def __init__(self, action_map: Dict[str, str]):
        self.action_map = action_map

    def transform(self, item: Dict[str, Any]) -> Dict[str, Any]:
        action = item.get("action")
        if action in self.action_map:
            item["action"] = self.action_map[action]
        return item
