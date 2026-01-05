"""Prisma transformation pipelines.

This module defines action, category, and type mappings for Prisma
URL filtering configurations, along with transformation pipelines
to convert between Prisma-specific and universal data models.
"""

from transformers.action_mapper import ActionMapper
from transformers.base_transformer import BaseTransformer
from transformers.category_mapper import CategoryMapper
from transformers.metadata_enricher import MetadataEnricher
from transformers.pattern_normalizer import PatternNormalizer
from transformers.type_mapper import TypeMapper

# ---------------- PRISMA MAPPINGS ----------------

PRISMA_ACTION_MAP = {
    "block": "deny",
    "allow": "allow",
    "monitor": "alert",
}

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


# ---------------- PRISMA PIPELINES ----------------

VENDOR_TO_UNIVERSAL_PIPELINES = [
    ActionMapper(PRISMA_ACTION_MAP),
    PatternNormalizer(),
    TypeMapper(PRISMA_TYPE_MAP),
    CategoryMapper(PRISMA_CATEGORY_MAP),
    MetadataEnricher("prisma"),
]

UNIVERSAL_TO_VENDOR_PIPELINES = [
    ActionMapper({value: key for key, value in PRISMA_ACTION_MAP.items()}),
    PatternNormalizer(),
    TypeMapper({value: key for key, value in PRISMA_TYPE_MAP.items()}),
    CategoryMapper({value: key for key, value in PRISMA_CATEGORY_MAP.items()}),
    MetadataEnricher("prisma"),
]
