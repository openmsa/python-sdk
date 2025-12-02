"""
transformers.py
A single-file SDK for bidirectional URL-filter migration transformers.

Supports:
- Vendors: Fortinet, Netskope, Zscaler, Prisma Access
- Universal intermediate model
- Modular basic transformers (action, pattern, category, metadata)
- CLI and unit test support
- Built-in sample data for direct testing
"""

from typing import List, Dict, Any
from dataclasses import dataclass, field

# ---------------- UNIVERSAL DATA MODEL ----------------

@dataclass
class UniversalURLFilter:
    pattern: str
    action: str
    category: str
    type: str = "literal"  # literal, wildcard, regex, substring
    vendor: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

# ---------------- BASIC TRANSFORMERS ----------------

class BaseTransformer:
    """Abstract transformer"""
    def transform(self, item: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError

class ActionMapper(BaseTransformer):
    def __init__(self, action_map: Dict[str, str]):
        self.action_map = action_map

    def transform(self, item: Dict[str, Any]) -> Dict[str, Any]:
        item['action'] = self.action_map.get(item.get('action'), item.get('action'))
        return item

class PatternNormalizer(BaseTransformer):
    """Keep pattern as-is; do not change type"""
    def transform(self, item: Dict[str, Any]) -> Dict[str, Any]:
        item['pattern'] = item.get('pattern', '')
        return item

class TypeMapper(BaseTransformer):
    """Map vendor type -> universal type"""
    def __init__(self, type_map: Dict[str, str]):
        self.type_map = type_map

    def transform(self, item: Dict[str, Any]) -> Dict[str, Any]:
        # Always read the original 'type' from vendor config
        vendor_type = item.get('type', 'simple')
        # Normalize case for Zscaler
        vendor_type_normalized = vendor_type.upper() if vendor_type in ['STRING', 'WILDCARD', 'REGEX'] else vendor_type.lower()
        # Map to universal type
        item['type'] = self.type_map.get(vendor_type_normalized, 'literal')
        return item

class CategoryMapper(BaseTransformer):
    """Map vendor category to universal category"""
    def __init__(self, category_map: Dict[str, str]):
        self.category_map = category_map

    def transform(self, item: Dict[str, Any]) -> Dict[str, Any]:
        vendor_cat = str(item.get('category_id', 'default'))  # read from input
        item['category'] = self.category_map.get(vendor_cat, 'uncategorized')
        return item

class MetadataEnricher(BaseTransformer):
    """Add vendor metadata"""
    def __init__(self, vendor: str):
        self.vendor = vendor

    def transform(self, item: Dict[str, Any]) -> Dict[str, Any]:
        item['vendor'] = self.vendor
        return item

# ---------------- PIPELINE EXECUTOR ----------------

def apply_transformers(items: List[Dict[str, Any]], transformers: List[BaseTransformer]) -> List[Dict[str, Any]]:
    result = []
    for item in items:
        for t in transformers:
            item = t.transform(item)
        result.append(item)
    return result

# ---------------- VENDOR MAPPINGS ----------------

FORTINET_ACTION_MAP = {'block': 'block', 'allow': 'allow', 'monitor': 'monitor'}
FORTINET_CATEGORY_MAP = {'3': 'malware', '4': 'phishing', '5': 'gambling', 'default': 'uncategorized'}
FORTINET_TYPE_MAP = { "simple": "literal", "wildcard": "wildcard", "regex": "regex", "substring": "substring"}

NETSKOPE_ACTION_MAP = {'block': 'deny', 'allow': 'allow', 'monitor': 'monitor'}
NETSKOPE_CATEGORY_MAP = {'malware': 'malware', 'phishing': 'phishing', 'gambling': 'gambling', 'uncategorized': 'uncategorized'}
NETSKOPE_TYPE_MAP = { "exact": "literal", "wildcard": "wildcard", "regex": "regex", "substring": "substring"}

ZSCALER_ACTION_MAP = {'block': 'BLOCK', 'allow': 'ALLOW', 'monitor': 'MONITOR'}
ZSCALER_CATEGORY_MAP = {'malware': 'malware', 'phishing': 'phishing', 'gambling': 'gambling', 'uncategorized': 'uncategorized'}
ZSCALER_TYPE_MAP =  {"STRING": "literal", "WILDCARD": "wildcard", "REGEX": "regex"}

PRISMA_ACTION_MAP = {'block': 'deny', 'allow': 'allow', 'monitor': 'alert'}
PRISMA_CATEGORY_MAP = {'malware': 'malware', 'phishing': 'phishing', 'gambling': 'gambling', 'uncategorized': 'uncategorized'}
PRISMA_TYPE_MAP =  {"simple": "literal", "wildcard": "wildcard", "regex": "regex", "substring": "substring"}

# ---------------- PIPELINE DEFINITIONS ----------------

VENDOR_TO_UNIVERSAL_PIPELINES = {
    'fortinet': [
        ActionMapper(FORTINET_ACTION_MAP),
        PatternNormalizer(),
        TypeMapper(FORTINET_TYPE_MAP),
        CategoryMapper(FORTINET_CATEGORY_MAP),
        MetadataEnricher('fortinet')
    ],
    'netskope': [
        ActionMapper(NETSKOPE_ACTION_MAP),
        PatternNormalizer(),
        TypeMapper(NETSKOPE_TYPE_MAP),
        CategoryMapper(NETSKOPE_CATEGORY_MAP),
        MetadataEnricher('netskope')
    ],
    'zscaler': [
        ActionMapper(ZSCALER_ACTION_MAP),
        PatternNormalizer(),
        TypeMapper(ZSCALER_TYPE_MAP),
        CategoryMapper(ZSCALER_CATEGORY_MAP),
        MetadataEnricher('zscaler')
    ],
    'prisma': [
        ActionMapper(PRISMA_ACTION_MAP),
        PatternNormalizer(),
        TypeMapper(PRISMA_TYPE_MAP),
        CategoryMapper(PRISMA_CATEGORY_MAP),
        MetadataEnricher('prisma')
    ]
}

UNIVERSAL_TO_VENDOR_PIPELINES = {
    'fortinet': [
        ActionMapper({v:k for k,v in FORTINET_ACTION_MAP.items()}),
        PatternNormalizer(),
        TypeMapper({v:k for k,v in FORTINET_TYPE_MAP.items()}),
        CategoryMapper({v:k for k,v in FORTINET_CATEGORY_MAP.items()}),
        MetadataEnricher('fortinet')
    ],
    'netskope': [
        ActionMapper({v:k for k,v in NETSKOPE_ACTION_MAP.items()}),
        PatternNormalizer(),
        TypeMapper({v:k for k,v in NETSKOPE_TYPE_MAP.items()}),
        CategoryMapper({v:k for k,v in NETSKOPE_CATEGORY_MAP.items()}),
        MetadataEnricher('netskope')
    ],
    'zscaler': [
        ActionMapper({v:k for k,v in ZSCALER_ACTION_MAP.items()}),
        PatternNormalizer(),
        TypeMapper({v:k for k,v in ZSCALER_TYPE_MAP.items()}),
        CategoryMapper({v:k for k,v in ZSCALER_CATEGORY_MAP.items()}),
        MetadataEnricher('zscaler')
    ],
    'prisma': [
        ActionMapper({v:k for k,v in PRISMA_ACTION_MAP.items()}),
        PatternNormalizer(),
        TypeMapper({v:k for k,v in PRISMA_TYPE_MAP.items()}),
        CategoryMapper({v:k for k,v in PRISMA_CATEGORY_MAP.items()}),
        MetadataEnricher('prisma')
    ]
}


A
A
A
A
A
A
A
A
A
A
A
A
A
A
B
B
B
B
B
B
B
B
B
B
B
B
B
B
B
B
B
B
B
B
B
B
B
B
B
A
A
A
A
A
A
A
A
A
A
A
A
A
A
A
B
B
B
B
B
B
B
B
B
B
B
B
B
B
B
B
B
B
B
B
B
B
B
B
B
B
B
B
B
B

