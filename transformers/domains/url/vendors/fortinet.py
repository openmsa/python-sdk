"""
Fortinet URL Domain Integration.

This module implements the transformer, mapper, and exporter for Fortinet,
converting between Fortinet-specific configurations and the Unified Data
Model (UDM).
"""

from datetime import datetime
from typing import Any
from typing import List
from typing import Optional

import jmespath

from transformers.domains.url.models import URL_UDM
from transformers.domains.url.models import Category
from transformers.domains.url.models import Metadata
from transformers.framework.udm_transformers.category_mapper import \
    CategoryMapper
from transformers.framework.udm_transformers.metadata_enricher import \
    MetadataEnricher
from transformers.framework.udm_transformers.pattern_normalizer import \
    PatternNormalizer
from transformers.framework.udm_transformers.type_mapper import TypeMapper

FORTINET_ACTION_MAP = {
    "allow": "allow",
    "block": "block",
    "monitor": "monitor",
    "exempt": "allow",
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
}

JMESPATH_FLATTEN_URLS = """
*.urls.*.{
    pattern: url,
    action: action,
    status: status,
    type: type,
    url_id: url_id
}
"""


def flatten_fortinet_jmespath(raw_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Flatten nested Fortinet URL data into normalized records."""
    flat = []

    for _, url_list in raw_data.items():
        list_id = url_list["object_id"]
        list_name = url_list["filter_name"]

        for _, item in url_list["urls"].items():
            flat.append(
                {
                    "pattern": item["url"],
                    "action": item["action"],
                    "status": item["status"],
                    "type": item["type"],
                    "url_id": item["url_id"],
                    "list_id": list_id,
                    "list_name": list_name,
                    "category_id": "Uncategorized",
                }
            )

    return flat


class FortinetMapper:
    """Map transformed dictionaries into URL_UDM instances."""

    def to_udm(self, item: Dict[str, Any]) -> URL_UDM:
        """Convert a transformed dictionary into a validated URL_UDM."""
        cat_id = item.get("category_id", "uncategorized")
        categories = [
            Category(
                id=cat_id,
                name=cat_id.capitalize(),
                type="standard",
            )
        ]

        meta = Metadata(
            processed_at=datetime.fromisoformat(
                item["metadata"]["processed_at"]
            ),
            source=item["metadata"].get("source"),
        )

        return URL_UDM(
            pattern=item["pattern"],
            type=item["type"],
            action=item["action"],
            status="enable",
            url_list_id=str(item["list_id"]),
            url_list_name=item["list_name"],
            categories=categories,
            vendor=item["vendor"],
            metadata=meta,
            notes=item.get("notes"),
        )


class FortinetExporter:
    """Export URL_UDM records into Fortinet format."""

    def transform(self, udm: URL_UDM) -> Dict[str, Any]:
        """Reconstruct Fortinet-specific pattern and type syntax."""
        reverse_type_map = {
            value: key for key, value in FORTINET_TYPE_MAP.items()
        }

        return {
            "url": udm.pattern,
            "type": reverse_type_map.get(udm.type, "simple"),
        }


def run_universal_to_fortinet_pipeline(
    records: List[URL_UDM],
) -> List[Dict[str, Any]]:
    """Transform universal records into Fortinet export records."""
    output = []

    for record in records:
        output.append(
            {
                "pattern": record.pattern,
                "type": record.type,
                "action": record.action,
                "list_id": record.url_list_id,
                "list_name": record.url_list_name,
            }
        )

    return output


def export_fortinet_json(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Convert flat Fortinet records into grouped Fortinet JSON."""
    grouped = {}
    counters = {}

    for record in records:
        key = record["list_id"]

        if key not in grouped:
            grouped[key] = {
                "object_id": record["list_id"],
                "filter_name": record["list_name"],
                "urls": {},
            }
            counters[key] = 0

        idx = str(counters[key])
        counters[key] += 1

        grouped[key]["urls"][idx] = {
            "url_id": str(counters[key]),
            "url": record["pattern"],
            "type": record["type"],
            "action": record["action"],
            "status": "enable",
        }

    return grouped


def run_fortinet_to_universal_pipeline(
    raw_data: Dict[str, Any],
) -> List[URL_UDM]:
    """Run the full Fortinet-to-universal transformation pipeline."""
    flat_data = flatten_fortinet_jmespath(raw_data)

    steps = [
        ActionMapper(FORTINET_ACTION_MAP),
        PatternNormalizer(),
        TypeMapper(FORTINET_TYPE_MAP),
        CategoryMapper(FORTINET_CATEGORY_MAP),
        MetadataEnricher("fortinet"),
    ]

    mapper = FortinetMapper()
    udm_records = []

    for record in flat_data:
        for step in steps:
            record = step.transform(record)

        udm_records.append(mapper.to_udm(record))

    return udm_records


VENDOR_TO_UNIVERSAL_PIPELINES = {
    "fortinet": run_fortinet_to_universal_pipeline,
}
