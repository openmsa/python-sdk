# Absolute imports
import jsonata
from transformers.base_transformer import BaseTransformer
from transformers.pattern_normalizer import PatternNormalizer
from transformers.action_mapper import ActionMapper
from transformers.type_mapper import TypeMapper
from transformers.category_mapper import CategoryMapper
from transformers.metadata_enricher import MetadataEnricher

# ---------------- FORTINET MAPPINGS ----------------
FORTINET_ACTION_MAP = {"block": "block", "allow": "allow", "monitor": "monitor"}
FORTINET_CATEGORY_MAP = {"3": "malware", "4": "phishing", "5": "gambling", "default": "uncategorized"}
FORTINET_TYPE_MAP = {"simple": "literal", "wildcard": "wildcard", "regex": "regex", "substring": "substring"}

# ---------------- FORTINET PIPELINES ----------------
VENDOR_TO_UNIVERSAL_PIPELINES = [
    ActionMapper(FORTINET_ACTION_MAP),
    PatternNormalizer(),
    TypeMapper(FORTINET_TYPE_MAP),
    CategoryMapper(FORTINET_CATEGORY_MAP),
    MetadataEnricher("fortinet"),
]

UNIVERSAL_TO_VENDOR_PIPELINES = [
    ActionMapper({v: k for k, v in FORTINET_ACTION_MAP.items()}),
    PatternNormalizer(),
    TypeMapper({v: k for k, v in FORTINET_TYPE_MAP.items()}),
    CategoryMapper({v: k for k, v in FORTINET_CATEGORY_MAP.items()}),
    MetadataEnricher("fortinet"),
]
