"""Netskope transformation pipelines and pattern normalization.

This module defines transformers and mappings required to convert
Netskope URL list configurations to and from the universal data model.
"""

import re
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from transformers.action_mapper import ActionMapper
from transformers.base_transformer import BaseTransformer
from transformers.category_mapper import CategoryMapper
from transformers.metadata_enricher import MetadataEnricher
from transformers.pattern_normalizer import PatternNormalizer
from transformers.type_mapper import TypeMapper


class NetskopePatternNormalizer(BaseTransformer):
    """Normalize Netskope URL patterns for vendor compatibility.

    This transformer converts universal URL patterns into Netskope-
    compatible formats:

    - ``literal`` / ``exact`` patterns are preserved.
    - ``wildcard`` patterns are converted into regex.
    - ``regex`` patterns are passed through unchanged.
    """

    def wildcard_to_regex(self, pattern: str) -> str:
        """Convert a wildcard domain pattern to a regex.

        Example:
            ``*.example.com`` → ``^([^.]+\\.)*example\\.com$``

        Args:
            pattern: A wildcard URL pattern.

        Returns:
            A regex representation of the wildcard pattern.
        """
        if pattern.startswith("*."):
            domain = pattern[2:].replace(".", r"\.")
            return rf"^([^.]+\.)*{domain}$"

        return pattern

    def transform(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Transform a URL item into a Netskope-compatible pattern.

        Args:
            item: A universal URL dictionary.

        Returns:
            The transformed dictionary with Netskope pattern semantics.
        """
        raw_pattern = item.get("pattern", "")
        universal_type = item.get("type", "literal")

        if universal_type in ("literal", "exact"):
            item["pattern"] = raw_pattern
            item["netskope_type"] = "exact"

        elif universal_type in ("wildcard", "regex"):
            item["pattern"] = self.wildcard_to_regex(raw_pattern)
            item["netskope_type"] = "regex"

        else:
            item["pattern"] = raw_pattern
            item["netskope_type"] =_]()
