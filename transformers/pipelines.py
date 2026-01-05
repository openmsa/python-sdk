"""Pipeline helper functions for URL transformations.

This module provides utilities to apply a sequence of transformers
to vendor configuration items, producing universal model dictionaries.
"""

from typing import Any
from typing import Dict
from typing import List

from transformers.base_transformer import BaseTransformer


def apply_transformers(
    items: List[Dict[str, Any]],
    transformers: List[BaseTransformer]
) -> List[Dict[str, Any]]:   
    """Apply a sequence of transformers to a list of items.

    Each item in the input list is processed sequentially by all
    transformers in the given order.

    Args:
        items: A list of dictionaries representing vendor configuration
            entries.
        transformers: An ordered list of transformer instances that
            implement the `transform` method.

    Returns:
        A list of transformed dictionaries.
    """    
    result: List[Dict[str, Any]] = []

    for item in items:
        for transformer in transformers:
            item = transformer.transform(item)
        result.append(item)

    return result
