"""Fortinet transformation pipelines.

This module defines action, category, and type mappings for Fortinet
URL filtering configurations, as well as transformation pipelines
to convert between Fortinet-specific and universal data models.
"""

import jmespath

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

JMESPATH_FLATTEN_URLS = """
*[?modify_type!='Deleted'].*.data_urls.*.{
    pattern: url,
    action: `allow`,
    category_id: 'Uncategorized',
    list_name: @.name,
    list_id: @.object_id,
    type: @.data_type
}
"""

def flatten_fortinet_jmespath(url_lists: dict) -> list[dict]:
    """
    Flatten Fortinet JSON using JMESPath.

    Args:
        url_lists: Nested Fortinet JSON URL list.

    Returns:
        Flat list of URL entries suitable for transformer input.
    """
    result = jmespath.search(JMESPATH_FLATTEN_URLS, url_lists)
    # jmespath returns a nested list, flatten if needed
    flat_result = [item for sublist in result for item in sublist] if result else []
    return flat_result
