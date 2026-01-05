from typing import Dict, Any
from .base_transformer import BaseTransformer

class PatternNormalizer(BaseTransformer):
    """Generic pattern normalizer (pass-through)."""

    def transform(self, item: Dict[str, Any]) -> Dict[str, Any]:
        item["pattern"] = item.get("pattern", "")
        return item
