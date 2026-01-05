from typing import Dict, Any
from .base_transformer import BaseTransformer
from datetime import datetime

class MetadataEnricher(BaseTransformer):
    """Adds vendor and metadata information."""

    def __init__(self, vendor: str):
        self.vendor = vendor

    def transform(self, item: Dict[str, Any]) -> Dict[str, Any]:
        item["vendor"] = self.vendor
        if "metadata" not in item:
            item["metadata"] = {}
        item["metadata"]["processed_at"] = datetime.utcnow().isoformat()
        return item
