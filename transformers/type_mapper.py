from typing import Dict, Any
from .base_transformer import BaseTransformer

class TypeMapper(BaseTransformer):
    """Maps types (literal/wildcard/regex/substring) per vendor."""

    def __init__(self, type_map: Dict[str, str]):
        self.type_map = type_map

    def transform(self, item: Dict[str, Any]) -> Dict[str, Any]:
        t = item.get("type")
        if t in self.type_map:
            item["type"] = self.type_map[t]
        return item
