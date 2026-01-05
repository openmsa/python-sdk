"""
pipelines.py

Helper functions to run transformation pipelines for URL lists.
"""

from typing import List, Dict, Any
from transformers.base_transformer import BaseTransformer


def apply_transformers(items: List[Dict[str, Any]], transformers: List[BaseTransformer]-> List[Dict[str, Any]]:
    """
    Apply a list of transformers sequentially to a list of items.

    Args:
        items: List of vendor configuration dictionaries.
        transformers: Ordered list of transformer instances.

    Returns:
        List of transformed dictionaries.
    """
  
    result = []
    for item in items:
        for transformer in transformers:
            item = transformer.transform(item)
        result.append(item)
    return result

