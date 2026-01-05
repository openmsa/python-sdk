"""Zscaler transformation pipelines.

This module defines action, category, and type mappings for Zscaler
URL filtering configurations, along with transformation pipelines
to convert between Zscaler-specific and universal data models.
"""

from transformers.action_mapper import ActionMapper
from transformers.base_transformer import BaseTransformer
from transformers.category_mapper import CategoryMapper
from transformers.metadata_enricher import MetadataEnricher
from transformers.pattern_normalizer import PatternNormalizer
from transformers.type_mapper import TypeMapper


# ---------------- ZSCALER MAPPINGS ----------------

ZSCALER_ACTION_MAP = {
    "block": "BLOCK",
    "allow": "ALLOW",
    "monitor": "MONITOR",
}

ZSCALER_CATEGORY_MAP = {
    "malware": "malware",
    "phishing": "phishing",
    "gambling": "gambling",
    "uncategorized": "uncategorized",
}

ZSCALER_TYPE_MAP = {
    "STRING": "literal",
    "WILDCARD": "wildcard",
    "REGEX": "regex",
}


# ---------------- ZSCALER PIPELINES ----------------

VENDOR_TO_UNIVERSAL_PIPELINES = [
    ActionMapper(ZSCALER_ACTION_MAP),
    PatternNormalizer(),
    TypeMapper(ZSCALER_TYPE_MAP),
    CategoryMapper(ZSCALER_CATEGORY_MAP),
    MetadataEnricher("zscaler"),
]

UNIVERSAL_TO_VENDOR_PIPELINES = [
    ActionMapper({value: key for key, value in ZSCALER_ACTION_MAP.items()}),
    PatternNormalizer(),
    TypeMapper({value: key for key, value in ZSCALER_TYPE_MAP.items()}),
    CategoryMapper({value: key for key, value in ZSCALER_CATEGORY_MAP.items()}),
    MetadataEnricher("zscaler"),
]

