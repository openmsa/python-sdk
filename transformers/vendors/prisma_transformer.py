# Absolute imports
from transformers.base_transformer import BaseTransformer
from transformers.pattern_normalizer import PatternNormalizer
from transformers.action_mapper import ActionMapper
from transformers.type_mapper import TypeMapper
from transformers.category_mapper import CategoryMapper
from transformers.metadata_enricher import MetadataEnricher

# ---------------- PRISMA MAPPINGS ----------------
PRISMA_ACTION_MAP = {"block": "deny", "allow": "allow", "monitor": "alert"}
PRISMA_CATEGORY_MAP = {"malware": "malware", "phishing": "phishing", "gambling": "gambling", "uncategorized": "uncategorized"}
PRISMA_TYPE_MAP = {"simple": "literal", "wildcard": "wildcard", "regex": "regex", "substring": "substring"}

# ---------------- PRISMA PIPELINES ----------------
VENDOR_TO_UNIVERSAL_PIPELINES = [
    ActionMapper(PRISMA_ACTION_MAP),
    PatternNormalizer(),
    TypeMapper(PRISMA_TYPE_MAP),
    CategoryMapper(PRISMA_CATEGORY_MAP),
    MetadataEnricher("prisma"),
]

UNIVERSAL_TO_VENDOR_PIPELINES = [
    ActionMapper({v: k for k, v in PRISMA_ACTION_MAP.items()}),
    PatternNormalizer(),
    TypeMapper({v: k for k, v in PRISMA_TYPE_MAP.items()}),
    CategoryMapper({v: k for k, v in PRISMA_CATEGORY_MAP.items()}),
    MetadataEnricher("prisma"),
]
