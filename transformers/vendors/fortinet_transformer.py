"""Fortinet transformation pipelines.

This module defines action, category, and type mappings for Fortinet
URL filtering configurations, as well as transformation pipelines
to convert between Fortinet-specific and universal data models.
"""

from transformers.action_mapper import ActionMapper
from transformers.base_transformer import BaseTransformer
from transformers.category_mapper import CategoryMapper
from transformers.metadata_enricher import MetadataEnricher
from transformers.pattern_normalizer import PatternNormalizer
from transformers.type_mapper import TypeMapper

# ---------------- FORTINET MAPPINGS ----------------

FORTINET_ACTION_MAP = {
    "block": "block",
    "allow": "allow",
    "monitor": "monitor",
}

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


# ---------------- FORTINET PIPELINES ----------------

VENDOR_TO_UNIVERSAL_PIPELINES = [
    ActionMapper(FORTINET_ACTION_MAP),
    PatternNormalizer(),
    TypeMapper(FORTINET_TYPE_MAP),
    CategoryMapper(FORTINET_CATEGORY_MAP),
    MetadataEnricher("fortinet"),
]

UNIVERSAL_TO_VENDOR_PIPELINES = [
    ActionMapper({value: key for key, value in FORTINET_ACTION_MAP.items()}),
    PatternNormalizer(),
    TypeMapper({value: key for key, value in FORTINET_TYPE_MAP.items()}),
    CategoryMapper({value: key for key, value in FORTINET_CATEGORY_MAP.items()}),
    MetadataEnricher("fortinet"),
]
