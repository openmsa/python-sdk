"""Metadata enrichment transformer.

This module defines a transformer that adds vendor information and
metadata timestamps to each item in the transformation pipeline.
"""

from datetime import datetime
from typing import Any
from typing import Dict

from .base_transformer import BaseTransformer


class MetadataEnricher(BaseTransformer):
    """Enrich items with vendor and metadata information.

    This transformer adds a ``vendor`` field and a ``metadata`` dictionary
    containing a ``processed_at`` timestamp to each item.
    """
    
    def __init__(self, vendor: str) -> None:        
        """Initialize the MetadataEnricher.

        Args:
            vendor: The vendor name to attach to each item.
        """      
        self.vendor = vendor

    def transform(self, item: Dict[str, Any]) -> Dict[str, Any]:        
        """Add vendor and metadata information to an item.

        Args:
            item: A dictionary representing a single configuration or URL entry.

        Returns:
            The transformed dictionary containing the ``vendor`` field and
            a ``metadata.processed_at`` timestamp.
        """        
        item["vendor"] = self.vendor
        if "metadata" not in item:
            item["metadata"] = {}

        item["metadata"]["processed_at"] = datetime.utcnow().isoformat()

        return item
