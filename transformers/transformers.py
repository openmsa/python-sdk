"""
Single-file SDK for bidirectional URL-filter migration transformers.

This module provides:
- Universal intermediate URL-filter model
- Vendor-specific transformers for: Fortinet, Netskope, Zscaler, Prisma Access
- Modular basic transformers (action, pattern, type, category, metadata)
- Transformer pipelines (vendor → universal and universal → vendor)
- CLI and unit-test support
- Built-in sample mappings for immediate use
"""

from typing import List, Dict, Any
from dataclasses import dataclass, field


# ---------------- UNIVERSAL DATA MODEL ----------------


@dataclass
class UniversalURLFilter:
    """
    Universal URL Filter Model.

    Attributes:
        pattern: URL pattern from vendor configuration.
        action: Universal action (allow, block, monitor, etc.).
        category: Universal category name.
        list_name: Optional list name.
        list_id: Optional list identifier.
        type: Pattern type (literal, wildcard, regex, substring).
        vendor: Originating vendor name.
        metadata: Additional vendor-specific fields.
    """

    pattern: str
    action: str
    category: str
    list_name: str = ""
    list_id: str = ""
    type: str = "literal"
    vendor: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


# ---------------- BASIC TRANSFORMERS ----------------


class BaseTransformer:
    """
    Abstract transformer base class.

    All transformers must implement the ``transform`` method.
    """

    def transform(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform a single item.

        Args:
            item: Input dictionary from vendor configuration.

        Returns:
            Transformed dictionary.

        Raises:
            NotImplementedError: If the subclass does not override this method.
        """
        raise NotImplementedError


class ActionMapper(BaseTransformer):
    """
    Transformer to map vendor actions to universal actions (or vice versa).
    """

    def __init__(self, action_map: Dict[str, str]):
        """
        Initialize the ActionMapper.

        Args:
            action_map: Dictionary mapping vendor actions to universal actions.
        """
        self.action_map = action_map

    def transform(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Map the action field using the configured mapping.

        Args:
            item: Input dictionary to transform.

        Returns:
            Updated dictionary with mapped action.
        """
        item["action"] = self.action_map.get(item.get("action"), item.get("action"))
        return item


class PatternNormalizer(BaseTransformer):
    """
    Transformer that normalizes or passes through patterns unchanged.
    """

    def transform(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize the pattern of the item.

        Args:
            item: Input dictionary.

        Returns:
            Updated dictionary with normalized pattern.
        """
        item["pattern"] = item.get("pattern", "")
        return item


class TypeMapper(BaseTransformer):
    """
    Transformer that maps vendor pattern types to universal types (or reverse).
    """

    def __init__(self, type_map: Dict[str, str]):
        """
        Initialize the TypeMapper.

        Args:
            type_map: Mapping from vendor type to universal type.
        """
        self.type_map = type_map

    def transform(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Map the pattern type, normalizing case when necessary.

        Args:
            item: Input dictionary.

        Returns:
            Updated dictionary with normalized pattern type.
        """
        vendor_type = item.get("type", "simple")

        vendor_type_normalized = (
            vendor_type.upper()
            if vendor_type in ["STRING", "WILDCARD", "REGEX"]
            else vendor_type.lower()
        )

        item["type"] = self.type_map.get(vendor_type_normalized, "literal")
        return item


class CategoryMapper(BaseTransformer):
    """
    Transformer to map vendor category IDs or names to universal names.
    """

    def __init__(self, category_map: Dict[str, str]):
        """
        Initialize the CategoryMapper.

        Args:
            category_map: Mapping from vendor category to universal category.
        """
        self.category_map = category_map

    def transform(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Map vendor category to a universal category.

        Args:
            item: Input dictionary.

        Returns:
            Updated dictionary with normalized category.
        """
        vendor_cat = str(item.get("category_id", "default"))
        item["category"] = self.category_map.get(vendor_cat, "uncategorized")
        return item


class MetadataEnricher(BaseTransformer):
    """
    Transformer that enriches items with vendor metadata fields.
    """

    def __init__(self, vendor: str, extra_fields: List[str] | None = None):
        """
        Initialize the MetadataEnricher.

        Args:
            vendor: Vendor identifier.
            extra_fields: Optional list of field names to embed in metadata.
        """
        self.vendor = vendor
        self.extra_fields = extra_fields or []

    def transform(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add vendor metadata to the item.

        Args:
            item: Input dictionary.

        Returns:
            Updated dictionary enriched with metadata.
        """
        item["vendor"] = self.vendor
        item.setdefault("metadata", {})

        for field_name in self.extra_fields:
            if field_name in item:
                item["metadata"][field_name] = item[field_name]

        return item


# ---------------- PIPELINE EXECUTOR ----------------


def apply_transformers(
    items: List[Dict[str, Any]], transformers: List[BaseTransformer]
) -> List[Dict[str, Any]]:
    """
    Apply a list of transformers sequentially to a list of items.

    Args:
        items: List of vendor configuration dictionaries.
        transformers: Ordered list of transformer instances.

    Returns:
        A list of transformed dictionaries.
    """
    result = []
    for item in items:
        for transformer in transformers:
            item = transformer.transform(item)
        result.append(item)
    return result


# ---------------- VENDOR MAPPINGS ----------------
# (constant values do not require docstrings)

FORTINET_ACTION_MAP = {"block": "block", "allow": "allow", "monitor": "monitor"}
FORTINET_CATEGORY_MAP = {
    "3": "malware",
    "4": "phishing",
    "5": "gambling",
    "default": "uncategorized",
}
FORTINET_TYPE_MAP = {
    "simple": "literal",
    "wildcard": "wildcard",
    "regex": "regex",
    "substring": "substring",
}

NETSKOPE_ACTION_MAP = {"block": "deny", "allow": "allow", "monitor": "monitor"}
NETSKOPE_CATEGORY_MAP = {
    "malware": "malware",
    "phishing": "phishing",
    "gambling": "gambling",
    "uncategorized": "uncategorized",
}
NETSKOPE_TYPE_MAP = {
    "exact": "literal",
    "wildcard": "wildcard",
    "regex": "regex",
    "substring": "substring",
}

ZSCALER_ACTION_MAP = {"block": "BLOCK", "allow": "ALLOW", "monitor": "MONITOR"}
ZSCALER_CATEGORY_MAP = {
    "malware": "malware",
    "phishing": "phishing",
    "gambling": "gambling",
    "uncategorized": "uncategorized",
}
ZSCALER_TYPE_MAP = {"STRING": "literal", "WILDCARD": "wildcard", "REGEX": "regex"}

PRISMA_ACTION_MAP = {"block": "deny", "allow": "allow", "monitor": "alert"}
PRISMA_CATEGORY_MAP = {
    "malware": "malware",
    "phishing": "phishing",
    "gambling": "gambling",
    "uncategorized": "uncategorized",
}
PRISMA_TYPE_MAP = {
    "simple": "literal",
    "wildcard": "wildcard",
    "regex": "regex",
    "substring": "substring",
}


# ---------------- PIPELINE DEFINITIONS ----------------

VENDOR_TO_UNIVERSAL_PIPELINES = {
    "fortinet": [
        ActionMapper(FORTINET_ACTION_MAP),
        PatternNormalizer(),
        TypeMapper(FORTINET_TYPE_MAP),
        CategoryMapper(FORTINET_CATEGORY_MAP),
        MetadataEnricher("fortinet"),
    ],
    "netskope": [
        ActionMapper(NETSKOPE_ACTION_MAP),
        PatternNormalizer(),
        TypeMapper(NETSKOPE_TYPE_MAP),
        CategoryMapper(NETSKOPE_CATEGORY_MAP),
        MetadataEnricher("netskope"),
    ],
    "zscaler": [
        ActionMapper(ZSCALER_ACTION_MAP),
        PatternNormalizer(),
        TypeMapper(ZSCALER_TYPE_MAP),
        CategoryMapper(ZSCALER_CATEGORY_MAP),
        MetadataEnricher("zscaler"),
    ],
    "prisma": [
        ActionMapper(PRISMA_ACTION_MAP),
        PatternNormalizer(),
        TypeMapper(PRISMA_TYPE_MAP),
        CategoryMapper(PRISMA_CATEGORY_MAP),
        MetadataEnricher("prisma"),
    ],
}

UNIVERSAL_TO_VENDOR_PIPELINES = {
    "fortinet": [
        ActionMapper({v: k for k, v in FORTINET_ACTION_MAP.items()}),
        PatternNormalizer(),
        TypeMapper({v: k for k, v in FORTINET_TYPE_MAP.items()}),
        CategoryMapper({v: k for k, v in FORTINET_CATEGORY_MAP.items()}),
        MetadataEnricher("fortinet"),
    ],
    "netskope": [
        ActionMapper({v: k for k, v in NETSKOPE_ACTION_MAP.items()}),
        PatternNormalizer(),
        TypeMapper({v: k for k, v in NETSKOPE_TYPE_MAP.items()}),
        CategoryMapper({v: k for k, v in NETSKOPE_CATEGORY_MAP.items()}),
        MetadataEnricher("netskope"),
    ],
    "zscaler": [
        ActionMapper({v: k for k, v in ZSCALER_ACTION_MAP.items()}),
        PatternNormalizer(),
        TypeMapper({v: k for k, v in ZSCALER_TYPE_MAP.items()}),
        CategoryMapper({v: k for k, v in ZSCALER_CATEGORY_MAP.items()}),
        MetadataEnricher("zscaler"),
    ],
    "prisma": [
        ActionMapper({v: k for k, v in PRISMA_ACTION_MAP.items()}),
        PatternNormalizer(),
        TypeMapper({v: k for k, v in PRISMA_TYPE_MAP.items()}),
        CategoryMapper({v: k for k, v in PRISMA_CATEGORY_MAP.items()}),
        MetadataEnricher("prisma"),
    ],
}
