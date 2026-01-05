"""Category mapping transformer.

This module defines a transformer responsible for mapping category
identifiers between vendor-specific representations and the universal
data model.
"""

from typing import Any, Dict
from .base_transformer import BaseTransformer

class CategoryMapper(BaseTransformer):   
    """Map category identifiers between vendor and universal models.

    This transformer replaces the ``category_id`` field of an item using
    a predefined mapping dictionary. If the category is not found in the
    mapping, it is left unchanged.
    """
    def __init__(self, category_map: Dict[str, str]) -> None:  
        """Initialize the CategoryMapper.

        Args:
            category_map: A dictionary mapping source category identifiers
                to destination category identifiers.
        """
        self.category_map = category_map

    def transform(self, item: Dict[str, Any]) -> Dict[str, Any]: 
        """Transform an item's category identifier using the category map.

        Args:
            item: A dictionary representing a single rule or configuration
                entry containing a ``category_id`` field.

        Returns:
            The transformed item with its ``category_id`` field mapped
            according to the configured category map.
        """
        category_id = item.get("category_id")
        if category_id in self.category_map:
            item["category_id"] = self.category_map[category_id]

        return item
