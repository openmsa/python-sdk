"""
Fortinet URL Domain Integration

This module implements the Transformer, Mapper, and Exporter for Fortinet,
converting between Fortinet-specific configurations and the Pydantic
Unified Data Model (UDM).
"""

import jmespath
from datetime import datetime
from typing import Any, Dict, List, Optional

# Framework imports - Absolute paths [cite: 66-67]
from transformers.framework.udm_transformers.action_mapper import ActionMapper
from transformers.framework.udm_transformers.category_mapper import CategoryMapper
from transformers.framework.udm_transformers.metadata_enricher import MetadataEnricher
from transformers.framework.udm_transformers.pattern_normalizer import PatternNormalizer
from transformers.framework.udm_transformers.type_mapper import TypeMapper

# Domain Model imports [cite: 81, 212]
from transformers.domains.url.models import URL_UDM
from transformers.domains.url.models import Category
from transformers.domains.url.models import Metadata

# ---------------- FORTINET MAPPINGS ----------------

FORTINET_TYPE_MAP = {
    "simple": "literal",
    "wildcard": "wildcard",
    "regex": "regex",
}

# ---------------- EXTRACTION LAYER ----------------


JMESPATH_FLATTEN_URLS = """
*.urls.*.{
    pattern: url,
    type: type,
    url_id: url_id
}
"""

def flatten_fortinet_jmespath(raw_data):
    flat = []

    for _, url_list in raw_data.items():
        list_id = url_list["object_id"]
        list_name = url_list["filter_name"]

        for _, item in url_list["urls"].items():
            flat.append({
                "pattern": item["url"],
                "type": item["type"],
                "url_id": item["url_id"],
                "list_id": list_id,
                "list_name": list_name,
            })

    return flat

# ---------------- MAPPER & EXPORTER ----------------

class FortinetMapper:
    """
    Handles semantic alignment and Pydantic UDM instantiation.
    """

    def to_udm(self, item: Dict[str, Any]) -> URL_UDM:
        """
        Converts a transformed dictionary into a validated URL_UDM instance.
        """
        # Construct the Metadata model
        # MetadataEnricher provides the ISO timestamp string
        meta = Metadata(
            processed_at=datetime.fromisoformat(item["metadata"]["processed_at"]),
        )

        return URL_UDM(
            pattern=item["pattern"],
            type=item["type"],
            url_list_id=str(item["list_id"]),
            url_list_name=item["list_name"],
            vendor=item["vendor"],
            metadata=meta,
        )

class FortinetExporter:
    """
    Universal Model -> Fortinet Format.
    """
    def transform(self, udm: URL_UDM) -> Dict[str, Any]:
        """
        Reconstructs Fortinet-specific pattern and type syntax.
        """
        # Reverse mapping for Type [cite: 347]
        reverse_type_map = {v: k for k, v in FORTINET_TYPE_MAP.items()}

        return {
            "url": udm.pattern,
            "type": reverse_type_map.get(udm.type, "simple")
        }

def run_universal_to_fortinet_pipeline(records: List[URL_UDM]) -> List[dict]:
    output = []

    for r in records:
        output.append({
            "pattern": r.pattern,
            "type": r.type,
            "list_id": r.url_list_id,
            "list_name": r.url_list_name
        })

    return output


def export_fortinet_json(records: List[dict]) -> dict:
    grouped = {}
    counters = {}

    for r in records:
        key = r["list_id"]

        if key not in grouped:
            grouped[key] = {
                "object_id": r["list_id"],
                "filter_name": r["list_name"],
                "urls": {}
            }
            counters[key] = 0

        idx = str(counters[key])
        counters[key] += 1

        grouped[key]["urls"][idx] = {
            "url_id": str(counters[key]),
            "url": r["pattern"],
            "type": r["type"],
        }

    return grouped

# ---------------- EXECUTION PIPELINE ----------------

def run_fortinet_to_universal_pipeline(raw_data: Dict[str, Any]) -> List[URL_UDM]:
    """
    Orchestrates the deterministic flow from raw Fortinet data to UDM objects.
    """
    # 1. Extraction [cite: 264]
    flat_data = flatten_fortinet_jmespath(raw_data)

    # 2. Transformation Pipeline [cite: 338-343]
    steps = [
        PatternNormalizer(),
        TypeMapper(FORTINET_TYPE_MAP),
        MetadataEnricher("fortinet")
    ]

    mapper = FortinetMapper()
    udm_records = []

    for record in flat_data:
        # Apply each modular transformation unit
        for step in steps:
            record = step.transform(record)

        # 3. Validation & Pydantic Conversion
        udm_records.append(mapper.to_udm(record))

    return udm_records

# ---------------- REGISTRATION ----------------

# This is what debugPythonScript.py is looking for
VENDOR_TO_UNIVERSAL_PIPELINES = {
    "fortinet": run_fortinet_to_universal_pipeline
}
