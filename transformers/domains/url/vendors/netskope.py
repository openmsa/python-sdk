"""
Netskope URL Domain Integration

This module implements the Transformer, Mapper, and Exporter for Netskope,
converting between Netskope-specific configurations and the Pydantic
Unified Data Model (UDM).
"""

import re
import jmespath
from datetime import datetime
from typing import Any, Dict, List, Optional

# Framework imports - Absolute paths
from transformers.framework.udm_transformers.action_mapper import ActionMapper
from transformers.framework.udm_transformers.category_mapper import CategoryMapper
from transformers.framework.udm_transformers.metadata_enricher import MetadataEnricher
from transformers.framework.udm_transformers.pattern_normalizer import PatternNormalizer
from transformers.framework.udm_transformers.type_mapper import TypeMapper
from transformers.framework.udm_transformers.base_transformer import BaseTransformer

# Domain Model imports
from transformers.domains.url.models import URL_UDM
from transformers.domains.url.models import Category
from transformers.domains.url.models import Metadata

# ---------------- NETSKOPE MAPPINGS ----------------

NETSKOPE_ACTION_MAP = {
    "block": "deny",
    "allow": "allow",
    "monitor": "allow",
}

NETSKOPE_CATEGORY_MAP = {
    "malware": "malware",
    "phishing": "phishing",
    "gambling": "gambling",
    "uncategorized": "uncategorized",
}

NETSKOPE_TO_UNIVERSAL_TYPE_MAP = {
    "exact": "literal",
    "regex": "regex",
}

# ---------------- EXTRACTION LAYER ----------------

JMESPATH_NETSKOPE = """
values(@)[?modify_type!='Deleted'].{
  list_name: name,
  list_id: object_id,
  type: data_type,
  urls: values(data_urls)
}
"""

def flatten_netskope_jmespath(url_lists: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Flatten the structure using jmespath. """
    extracted = jmespath.search(JMESPATH_NETSKOPE, url_lists) or []
    flat = []

    for lst in extracted:
        for entry in lst.get("urls", []):
            url = entry.get("url")
            if not url:
                continue
            flat.append({
                "pattern": url,
                "action": "allow",
                "category_id": "Uncategorized",
                "list_name": lst["list_name"],
                "list_id": str(lst["list_id"]),
                "type": lst["type"]
            })
    return flat

# ---------------- TRANSFORMERS ----------------

class NetskopePatternNormalizer(BaseTransformer):
    """Normalize Netskope URL patterns for vendor compatibility."""

    def wildcard_to_regex(self, pattern: str) -> str:
        """Convert a wildcard domain pattern to a regex."""
        if pattern.startswith("*."):
            domain = pattern[2:].replace(".", r"\.")
            return rf"^([^.]+\.)*{domain}$"
        return pattern

    def transform(self, item: Dict[str, Any]) -> Dict[str, Any]:
        raw_pattern = item.get("pattern", "")
        universal_type = item.get("type", "literal")

        if universal_type in ("literal", "exact"):
            item["pattern"] = raw_pattern
            item["netskope_type"] = "exact"
        elif universal_type in ("wildcard", "regex"):
            item["pattern"] = self.wildcard_to_regex(raw_pattern)
            item["netskope_type"] = "regex"
        else:
            item["pattern"] = raw_pattern
            item["netskope_type"] = "exact"
        return item

class NetskopePatternDenormalizer(BaseTransformer):
    """Convert Netskope patterns back to universal model patterns."""

    def regex_to_wildcard(self, pattern: str) -> Optional[str]:
        wildcard_regex = r"^\^\(\[\^\.\]\+\\\.\)\*(.+)\\\.([a-zA-Z0-9\-]+)\$$"
        match = re.match(wildcard_regex, pattern)
        if match:
            domain = f"{match.group(1)}.{match.group(2)}"
            return f"*.{domain}"
        return None

    def is_regex(self, pattern: str) -> bool:
        regex_markers = ("^", "$", "(", ")", "[", "]", "+", "?", "|", "{", "}")
        return any(marker in pattern for marker in regex_markers)

    def transform(self, item: Dict[str, Any]) -> Dict[str, Any]:
        pattern = item.get("pattern", "").replace("\\\\", "\\")
        if pattern.startswith("*.") and pattern.count("*") == 1:
            item["type"] = "wildcard"
        elif "*" in pattern:
            item["type"] = "regex"
        elif self.is_regex(pattern):
            wildcard = self.regex_to_wildcard(pattern)
            if wildcard:
                item["type"] = "wildcard"
                pattern = wildcard
            else:
                item["type"] = "regex"
        else:
            item["type"] = "exact"
        item["pattern"] = pattern
        item.pop("netskope_type", None)
        return item

# ---------------- MAPPER & EXPORTER ----------------

class NetskopeMapper:
    """Handles semantic alignment and Pydantic UDM instantiation."""

    def to_udm(self, item: Dict[str, Any]) -> URL_UDM:
        """Converts transformed dictionary into validated URL_UDM instance. """
        cat_id = item.get("category_id", "uncategorized")
        categories = [Category(id=cat_id, name=cat_id.capitalize(), type="standard")]

        meta = Metadata(
            processed_at=datetime.fromisoformat(item["metadata"]["processed_at"]),
            source="netskope"
        )

        return URL_UDM(
            pattern=item["pattern"],
            type=item["type"],
            action=item["action"],
            status="enable",
            url_list_id=item["list_id"],
            url_list_name=item["list_name"],
            categories=categories,
            vendor=item["vendor"],
            metadata=meta,
            notes=item.get("notes")
        )

class NetskopeExporter:
    """Universal Model -> Netskope Format. """

    def transform(self, udm: URL_UDM) -> Dict[str, Any]:
        # Implementation would use NetskopePatternNormalizer logic here
        pass

# ---------------- EXECUTION PIPELINE ----------------

def run_netskope_to_universal_pipeline(raw_data: Dict[str, Any]) -> List[URL_UDM]:
    """Orchestrates the flow from raw Netskope data to UDM objects. """
    # 1. Extraction
    flat_data = flatten_netskope_jmespath(raw_data)

    # 2. Transformation Pipeline
    steps = [
        ActionMapper(NETSKOPE_ACTION_MAP),
        TypeMapper(NETSKOPE_TO_UNIVERSAL_TYPE_MAP),
        NetskopePatternDenormalizer(),
        CategoryMapper(NETSKOPE_CATEGORY_MAP),
        MetadataEnricher("netskope")
    ]

    mapper = NetskopeMapper()
    udm_records = []

    for record in flat_data:
        for step in steps:
            record = step.transform(record)
        udm_records.append(mapper.to_udm(record))

    return udm_records

