"""Pattern normalization transformer.

This module defines a generic pattern normalizer that ensures each item
has a ``pattern`` field. Currently, this transformer acts as a pass-through.
"""

from typing import Any, Dict

from .base_transformer import BaseTransformer


class PatternNormalizer(BaseTransformer):
    """Normalize or enforce the presence of a pattern field in items.

    This transformer guarantees that each dictionary item contains a
    ``pattern`` key. If the key is missing, it is initialized to an empty string.
    """

    def transform(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Ensure the item has a pattern field.

        Args:
            item: A dictionary representing a single configuration or URL entry.

        Returns:
            The same dictionary with a ``pattern`` key ensured.
        """
        
        item["pattern"] = item.get("pattern", "")
        return item
