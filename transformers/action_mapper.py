"""Action mapping transformer.

This module defines a transformer responsible for mapping action values
between vendor-specific representations and the universal data model.
"""

from typing import Any, Dict
from .base_transformer import BaseTransformer

class ActionMapper(BaseTransformer):    
    """Map action values between vendor and universal models.
    This transformer replaces the ``action`` field of an item using a
    predefined mapping dictionary. If the action is not found in the
    mapping, it is left unchanged.
    """
    def __init__(self, action_map: Dict[str, str]) -> None:    
        """Initialize the ActionMapper.

        Args:
            action_map: A dictionary mapping source action values to
                destination action values.
        """  
        self.action_map = action_map

    def transform(self, item: Dict[str, Any]) -> Dict[str, Any]:  
        """Transform an item's action field using the action mapping.

        Args:
            item: A dictionary representing a single rule or configuration
                entry containing an ``action`` field.

        Returns:
            The transformed item with its ``action`` field mapped according
            to the configured action map.
        """     
        action = item.get("action")
        if action in self.action_map:
            item["action"] = self.action_map[action]

        return item
