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
from collections import defaultdict

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


NETSKOPE_TO_UNIVERSAL_TYPE_MAP = {
    "exact": "literal",
    "regex": "regex",
}

UNIVERSAL_TO_NETSKOPE_TYPE_MAP = {
    "literal": "exact",
    "regex": "regex",
    "wildcard": "regex",
    "substring": "regex",
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

    now_iso = datetime.utcnow().isoformat()

    for lst in extracted:
        for entry in lst.get("urls", []):
            url = entry.get("url")
            if not url:
                continue
            flat.append({
                "pattern": url,
                "list_name": lst["list_name"],
                "list_id": str(lst["list_id"]),
                "type": lst["type"],
                "metadata": {"processed_at": now_iso}
            })
    return flat

# ---------------- TRANSFORMERS ----------------

class NetskopePatternNormalizer(BaseTransformer):

    def wildcard_to_regex(self, pattern: str) -> str:
        if not pattern.startswith("*."):
            return pattern

        domain = re.escape(pattern[2:])
        return rf"^([^.]+\.)*{domain}$"

    def transform(self, item: Dict[str, Any]) -> Dict[str, Any]:
        item = item.copy()

        raw_pattern = item.get("pattern", "")
        universal_type = item.get("type", "literal")

        if universal_type in ("literal", "exact"):
            item["pattern"] = raw_pattern
            item["type"] = "literal"

        elif universal_type in ("wildcard", "regex"):
            item["pattern"] = self.wildcard_to_regex(raw_pattern)
            item["type"] = "regex"

        else:
            item["pattern"] = raw_pattern
            item["type"] = "literal"

        return item


class NetskopePatternDenormalizer(BaseTransformer):
    """Convert Netskope patterns back to universal model patterns."""

    def regex_to_wildcard(self, pattern: str) -> Optional[str]:
        prefix = "^([^.]+\\.)*"
        suffix = "$"

        if pattern.startswith(prefix) and pattern.endswith(suffix):
            domain = pattern[len(prefix):-len(suffix)]
            domain = domain.replace("\\.", ".")
            return f"*.{domain}"

        return None

    def is_regex(self, pattern: str) -> bool:
        regex_markers = ("^", "$", "(", ")", "[", "]", "+", "?", "|", "{", "}")
        return any(marker in pattern for marker in regex_markers)

    def transform(self, item: Dict[str, Any]) -> Dict[str, Any]:
        pattern = item.get("pattern", "").replace("\\\\", "\\")

        # already wildcard
        if pattern.startswith("*.") and pattern.count("*") == 1:
            item["type"] = "wildcard"

        # regex patterns FIRST
        elif self.is_regex(pattern):
            wildcard = self.regex_to_wildcard(pattern)

            if wildcard:
                item["type"] = "wildcard"
                pattern = wildcard
            else:
                item["type"] = "regex"

        # non-regex wildcard syntax
        elif "*" in pattern:
            item["type"] = "wildcard"

        else:
            item["type"] = "literal"

        item["pattern"] = pattern
        item.pop("netskope_type", None)

        return item

# ---------------- MAPPER & EXPORTER ----------------

class NetskopeMapper:
    """Handles semantic alignment and Pydantic UDM instantiation."""

    def to_udm(self, item: Dict[str, Any]) -> URL_UDM:
        """Converts transformed dictionary into validated URL_UDM instance. """

        meta = Metadata(
            processed_at=datetime.fromisoformat(item["metadata"]["processed_at"]),
        )

        return URL_UDM(
            pattern=item["pattern"],
            type=item["type"],
            url_list_id=item["list_id"],
            url_list_name=item["list_name"],
#            vendor=item["vendor"],
            vendor="netskope",
#            metadata=meta,
        )

class NetskopeExporter:
    """Universal Model -> Netskope Format."""

    def transform(self, item: Dict[str, Any]) -> Dict[str, Any]:
        # Netskope expects URLs nested under the list ID
        return {
            "object_id": item.get("url_list_id"),
            "name": item.get("url_list_name"),
            "data_type": item.get("type"),
            "data_urls": item.get("urls", []) # Ensure this is a list of strings
        }

# ---------------- EXECUTION PIPELINE ----------------

def run_netskope_to_universal_pipeline(raw_data: Dict[str, Any]) -> List[URL_UDM]:
    """Orchestrates the flow from raw Netskope data to UDM objects. """
    # 1. Extraction
    flat_data = flatten_netskope_jmespath(raw_data)

    # 2. Transformation Pipeline
    steps = [
        TypeMapper(NETSKOPE_TO_UNIVERSAL_TYPE_MAP),
        NetskopePatternDenormalizer(),
    ]

    mapper = NetskopeMapper()
    udm_records = []

    for record in flat_data:
        for step in steps:
            record = step.transform(record)
        udm_records.append(mapper.to_udm(record))

    return udm_records

def run_universal_to_netskope_pipeline(udm_records: List[Any]) -> List[Dict[str, Any]]:
    if not udm_records:
        return []

    steps = [
        TypeMapper(UNIVERSAL_TO_NETSKOPE_TYPE_MAP),
        NetskopePatternNormalizer(),
         MetadataEnricher("netskope")
    ]

    grouped = defaultdict(
        lambda: {
            "name": "",
            "data_type": "literal",
            "data_urls": set()
        }
    )

    for entry in udm_records:

        # Apply all transformers sequentially
        transformed = entry

        for step in steps:
            transformed = step.transform(transformed)

        # Use transformed record
        obj_id = str(transformed.get("url_list_id", "0"))
        name = transformed.get("url_list_name", "Default_List")
        url_val = transformed.get("pattern", "")
        d_type = transformed.get("type", "literal")

        if not url_val:
            continue

        group = grouped[obj_id]
        group["name"] = name
        group["data_urls"].add(url_val)

        if d_type == "wildcard" or d_type == "regex" or "*" in url_val:
            group["data_type"] = "regex"

    final_payload = []

    for oid, data in grouped.items():
        final_payload.append({
            "object_id": int(oid) if oid.isdigit() else oid,
            "name": data["name"],
            "data_type": data["data_type"],
            "data_urls": sorted(list(data["data_urls"]))
        })

    return final_payload

# Pipeline definitoion
VENDOR_TO_UNIVERSAL_PIPELINES = {
        "netskope": run_netskope_to_universal_pipeline
}

UNIVERSAL_TO_VENDOR_PIPELINES = {
    "netskope": run_universal_to_netskope_pipeline
}
