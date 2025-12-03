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

        A
