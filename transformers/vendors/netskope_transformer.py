"""Netskope transformation pipelines and pattern normalization.

This module defines transformers and mappings required to convert
Netskope URL list configurations to and from the universal data model.
"""
import re
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

import jmespath

from transformers.action_mapper import ActionMapper
from transformers.base_transformer import BaseTransformer
from transformers.category_mapper import CategoryMapper
from transformers.metadata_enricher import MetadataEnricher
from transformers.pattern_normalizer import PatternNormalizer
from transformers.type_mapper import TypeMapper

JMESPATH_NETSKOPE = """
values(@)[?modify_type!='Deleted'].{
  list_name: name,
  list_id: object_id,
  type: data_type,
  urls: values(data_urls)
}
"""

def flatten_netskope_jmespath(url_lists: dict) -> list[dict]:
    """Flatten the structure using jmespath."""  
    extracted = jmespath.search(JMESPATH_NETSKOPE, url_lists) or []
    flat = []

    for lst in extracted:
        for entry in lst.get("urls", []):
            url = entry.get("url")
            if not url:
                continue
            flat.append({
                "pattern": url,
                "action": "allow",
                "category_id": "Uncategorized",
                "list_name": lst["list_name"],
                "list_id": str(lst["list_id"]),
                "type": lst["type"]
            })
    return flat

class NetskopePatternNormalizer(BaseTransformer):
    """Normalize Netskope URL patterns for vendor compatibility.
    
    This transformer converts universal URL patterns into Netskope-
    compatible formats:

    - ``literal`` / ``exact`` patterns are preserved.
    - ``wildcard`` patterns are converted into regex.
    - ``regex`` patterns are passed through unchanged.
    """

    def wildcard_to_regex(self, pattern: str) -> str:
        r"""Convert a wildcard domain pattern to a regex.

        Example:
            ``*.example.com`` → ``^([^.]+\.)*example\.com$``

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
            item["netskope_type"] = "exact"

        return item

    def transform_list(
        self,
        items: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """Transform a list of URL items.

        Args:
            items: A list of universal URL dictionaries.

        Returns:
            A list of Netskope-compatible URL dictionaries.
        """
        return [self.transform(item) for item in items]


class NetskopePatternDenormalizer(BaseTransformer):
    """Convert Netskope patterns back to universal model patterns."""

    def regex_to_wildcard(self, pattern: str) -> Optional[str]:
        r"""Convert a Netskope regex pattern back to wildcard format.

        Example:
            ``^([^.]+\\.)*example\\.com$`` → ``*.example.com``

        Args:
            pattern: A Netskope regex pattern.

        Returns:
            A wildcard pattern if conversion is possible, otherwise ``None``.
        """
        wildcard_regex = (
            r"^\^\(\[\^\.\]\+\\\.\)\*(.+)\\\.([a-zA-Z0-9\-]+)\$$"
        )
        match = re.match(wildcard_regex, pattern)

        if match:
            domain = f"{match.group(1)}.{match.group(2)}"
            return f"*.{domain}"

        return None

    def is_regex(self, pattern: str) -> bool:
        """Determine whether a pattern contains regex syntax.

        Args:
            pattern: A URL pattern string.

        Returns:
            ``True`` if the pattern appears to be a regex, otherwise ``False``.
        """
        regex_markers = ("^", "$", "(", ")", "[", "]", "+", "?", "|", "{", "}")
        return any(marker in pattern for marker in regex_markers)

    def transform(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Transform a Netskope URL item into a universal-compatible form.

        Args:
            item: A Netskope URL dictionary.

        Returns:
            A universal URL dictionary.
        """
        pattern = item.get("pattern", "").replace("\\\\", "\\")

        if pattern.startswith("*.") and pattern.count("*") == 1:
            item["type"] = "wildcard"

        elif "*" in pattern:
            item["type"] = "regex"

        elif self.is_regex(pattern):
            wildcard = self.regex_to_wildcard(pattern)
            if wildcard:
                item["type"] = "wildcard"
                pattern = wildcard
            else:
                item["type"] = "regex"

        else:
            item["type"] = "exact"

        item["pattern"] = pattern
        item.pop("netskope_type", None)

        return item


# ---------------- NETSKOPE MAPPINGS ----------------

NETSKOPE_ACTION_MAP = {
    "block": "deny",
    "allow": "allow",
    "monitor": "allow",
}

NETSKOPE_CATEGORY_MAP = {
    "malware": "malware",
    "phishing": "phishing",
    "gambling": "gambling",
    "uncategorized": "uncategorized",
}

NETSKOPE_TO_UNIVERSAL_TYPE_MAP = {
    "exact": "literal",
    "regex": "regex",
}

UNIVERSAL_TO_NETSKOPE_TYPE_MAP = {
    "literal": "exact",
    "regex": "regex",
    "wildcard": "regex",
    "substring": "regex",
}


# ---------------- NETSKOPE PIPELINES ----------------

VENDOR_TO_UNIVERSAL_PIPELINES = [
    ActionMapper(NETSKOPE_ACTION_MAP),
    TypeMapper(NETSKOPE_TO_UNIVERSAL_TYPE_MAP),
    NetskopePatternDenormalizer(),
    CategoryMapper(NETSKOPE_CATEGORY_MAP),
    MetadataEnricher("netskope"),
]

UNIVERSAL_TO_VENDOR_PIPELINES = [
    ActionMapper({value: key for key, value in NETSKOPE_ACTION_MAP.items()}),
    TypeMapper(UNIVERSAL_TO_NETSKOPE_TYPE_MAP),
    NetskopePatternNormalizer(),
    CategoryMapper({value: key for key, value in NETSKOPE_CATEGORY_MAP.items()}),
    MetadataEnricher("netskope"),
]
