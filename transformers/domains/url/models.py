"""
URL Domain Models - Unified Data Model (UDM).

This module defines the canonical schema for URLs, URL collections.

Design Principles:

- Domain-Level Logic: Operates purely on domain concepts. 
- Vendor-Agnostic: No vendor-specific logic is contained here. 
- Strong Typing: Enforces RFC-compliant formatting and normalization. 
"""

from datetime import datetime
from typing import List
from typing import Literal
from typing import Optional

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class Metadata(BaseModel):
    """
    Extensible container for enrichment data.

    This includes timestamps, source information, and optional metadata fields.
    """

    processed_at: datetime = Field(
        ..., description="Timestamp of when the record was processed"
    )
    source: Optional[str] = Field(
        None, description="The origin system of the data"
    )
    additional_info: Optional[dict] = Field(
        None, description="Placeholder for custom metadata expansion"
    )


class URL_UDM(BaseModel):
    """
    Unified Data Model for URL entities.

    This model serves as the source of truth for processing, independent
    of any external vendor system.
    """

    model_config = ConfigDict(populate_by_name=True)

    pattern: str = Field(
        ..., description="The URL pattern (literal, wildcard, or regex)"
    )
    type: Literal["literal", "wildcard", "regex"] = Field(
        ..., description="The syntax type of the pattern"
    )
    url_list_id: str = Field(
        ..., description="Unique ID for the parent URL list"
    )
    url_list_name: str = Field(
        ..., description="Human-readable name of the URL list"
    )
    vendor: Optional[str] = Field(
        None, description="Original vendor for traceability purposes"
    )
    metadata: Optional[Metadata] = Field(
        None, description="Processing metadata and timestamps"
    )
