"""Type mapping transformer.

This module defines a transformer that maps item types (e.g., literal,
wildcard, regex, substring) between vendor-specific representations
and the universal data model.
"""

from typing import Any, Dict
from .base_transformer import BaseTransformer

class TypeMapper(BaseTransformer):
    """Map type values between vendor and universal models.

    This transformer replaces the ``type`` field of an item using a
    predefined mapping dictionary. If the type is not found in the
    mapping, it is left unchanged.
    """

    def __init__(self, type_map: Dict[str, str]) -> None:
        """Initialize the TypeMapper.

        Args:
            type_map: A dictionary mapping source type values to
                destination type values.
        """
        
        self.type_map = type_map

    def transform(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Transform an item's type field using the type mapping.

        Args:
            item: A dictionary representing a single rule or configuration
                entry containing a ``type`` field.

        Returns:
            The transformed item with its ``type`` field mapped according
            to the configured type map.
        """
        
        item_type = item.get("type")
        if item_type in self.type_map:
            item["type"] = self.type_map[item_type]

        return item
