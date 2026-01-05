from typing import Dict, Any
from .base_transformer import BaseTransformer

class CategoryMapper(BaseTransformer):
    """Maps categories per vendor."""

    def __init__(self, category_map: Dict[str, str]):
        self.category_map = category_map

    def transform(self, item: Dict[str, Any]) -> Dict[str, Any]:
        cat = item.get("category_id")
        if cat in self.category_map:
            item["category_id"] = self.category_map[cat]
        return item
