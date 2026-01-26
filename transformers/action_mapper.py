"""Action mapping transformer.

This module provides the ActionMapper class, which converts action values
between vendor-specific and universal representations.
"""

from typing import Dict
from typing import Any

from .base_transformer import BaseTransformer


class ActionMapper(BaseTransformer):
    """Maps actions from vendor-specific values to universal values and vice versa."""

    def __init__(self, action_map: Dict[str, str]) -> None:
        """Initialize the ActionMapper.

        Args:
            action_map: A mapping from vendor-specific action names
                to universal action names.
        """
        self.action_map = action_map

    def transform(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Transform the action field of an item using the action map.

        If the item's ``action`` value exists in the action map, it is
        replaced with the mapped universal value.

        Args:
            item: A dictionary representing the item to transform.

        Returns:
            The transformed item dictionary.
        """
        action = item.get("action")
        if action in self.action_map:
            item["action"] = self.action_map[action]
        return item
