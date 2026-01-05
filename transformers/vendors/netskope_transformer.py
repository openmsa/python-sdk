from typing import Dict, Any

# Absolute imports
from transformers.base_transformer import BaseTransformer
from transformers.pattern_normalizer import PatternNormalizer
from transformers.action_mapper import ActionMapper
from transformers.type_mapper import TypeMapper
from transformers.category_mapper import CategoryMapper
from transformers.metadata_enricher import MetadataEnricher


class NetskopePatternNormalizer(BaseTransformer):
    """
    Normalize Netskope URL patterns and convert wildcards to regex formats.

    - 'literal' or 'exact': left as-is for exact lists.
    - 'wildcard': converted to regex for regex lists.
    - 'regex': passed as regex (wildcards converted to proper regex if needed).
    """

    def wildcard_to_regex(self, pattern: str) -> str:
        """
        Convert Netskope wildcard patterns into regex.
        '*.example.com' -> '^([^.]+\.)*example\.com$'
        """
        if pattern.startswith("*."):
            domain = pattern[2:]
            domain = domain.replace(".", r"\.")  # Escape dots
            return rf"^([^.]+\.)*{domain}$"
        else:
            # Leave non-wildcards as-is for regex lists
            return pattern

    def transform(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform a single URL item into Netskope-compatible pattern.
        """
        raw_pattern = item.get("pattern", "")
        utype = item.get("type", "literal")  # universal type

        # Determine netskope_type
        if utype in ("literal", "exact"):
            # Exact list → leave pattern as literal
            final_pattern = raw_pattern
            item["netskope_type"] = "exact"

        elif utype in ("wildcard", "regex"):
            # Regex list → convert wildcard to proper regex
            final_pattern = self.wildcard_to_regex(raw_pattern)
            item["netskope_type"] = "regex"

        else:
            # Fallback
            final_pattern = raw_pattern
            item["netskope_type"] = "exact"

        # **Important:** do NOT double-escape backslashes
        # Only regex patterns need normal backslashes
        item["pattern"] = final_pattern

        return item

    def transform_list(self, items: list[Dict[str, Any]]) -> list[Dict[str, Any]]:
        """
        Transform a list of URL items.
        """
        return [self.transform(item) for item in items]


class NetskopePatternDenormalizer(BaseTransformer):
    """
    Convert Netskope Data Model patterns back into universal-compatible
    patterns and types.
    """

    def regex_to_wildcard(self, pattern: str) -> str | None:
        """
        Convert a known Netskope-style regex back to wildcard format.
        Example:
            ^([^.]+\.)*example\.com$  ->  *.example.com
        """
        wildcard_regex = r'^\^\(\[\^\.\]\+\\\.\)\*(.+)\\\.([a-zA-Z0-9\-]+)\$$'
        match = re.match(wildcard_regex, pattern)

        if match:
            domain = f"{match.group(1)}.{match.group(2)}"
            return f"*.{domain}"

        return None

    def is_regex(self, pattern: str) -> bool:
        regex_markers = (
            "^", "$", "(", ")", "[", "]", "+", "?", "|", "{", "}"
        )
        return any(m in pattern for m in regex_markers)

    def transform(self, item: Dict[str, Any]) -> Dict[str, Any]:
        pattern = item.get("pattern", "").replace("\\\\", "\\")

        # 1. Valid Netskope wildcard ONLY
        if pattern.startswith("*.") and pattern.count("*") == 1:
            item["type"] = "wildcard"
            item["pattern"] = pattern

        # 2. Any other '*' means regex
        elif "*" in pattern:
            item["type"] = "regex"
            item["pattern"] = pattern

        # 3. Regex syntax without '*'
        elif self.is_regex(pattern):
            wildcard = self.regex_to_wildcard(pattern)
            if wildcard:
                item["type"] = "wildcard"
                item["pattern"] = wildcard
            else:
                item["type"] = "regex"
                item["pattern"] = pattern

        # 4. Literal
        else:
            item["type"] = "exact"
            item["pattern"] = pattern

        item.pop("netskope_type", None)
        return item



# ---------------- NETSKOPE MAPPINGS ----------------
NETSKOPE_ACTION_MAP = {"block": "deny", "allow": "allow", "monitor": "allow"}
NETSKOPE_CATEGORY_MAP = {"malware": "malware", "phishing": "phishing", "gambling": "gambling", "uncategorized": "uncategorized"}
NETSKOPE_TO_UNIVERSAL_TYPE_MAP = {"exact": "literal", "regex": "regex"}
UNIVERSAL_TO_NETSKOPE_TYPE_MAP = {"literal": "exact", "regex": "regex", "wildcard": "regex", "substring": "regex"}

# ---------------- NETSKOPE PIPELINES ----------------

VENDOR_TO_UNIVERSAL_PIPELINES = [
    ActionMapper(NETSKOPE_ACTION_MAP),
    TypeMapper(NETSKOPE_TO_UNIVERSAL_TYPE_MAP),
    NetskopePatternDenormalizer(),
    CategoryMapper(NETSKOPE_CATEGORY_MAP),
    MetadataEnricher("netskope"),
]

UNIVERSAL_TO_VENDOR_PIPELINES = [
    ActionMapper({v: k for k, v in NETSKOPE_ACTION_MAP.items()}),
    TypeMapper(UNIVERSAL_TO_NETSKOPE_TYPE_MAP),
    NetskopePatternNormalizer(),
    CategoryMapper({v: k for k, v in NETSKOPE_CATEGORY_MAP.items()}),
    MetadataEnricher("netskope"),
]
