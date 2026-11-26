"""Indicator contracts that preserve original values and normalization separately."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from uuid import UUID

from fishtrace_engine.models.base import (
    SerializableModel,
    require_nonempty,
    require_timezone_aware,
    utc_now,
)


class IndicatorType(StrEnum):
    IPV4 = "ipv4"
    IPV6 = "ipv6"
    DOMAIN = "domain"
    URL = "url"
    EMAIL = "email"
    MD5 = "md5"
    SHA1 = "sha1"
    SHA256 = "sha256"


@dataclass(frozen=True, slots=True)
class Indicator(SerializableModel):
    """An extracted IOC; normalization never replaces the original value."""

    id: UUID
    type: IndicatorType
    original_value: str
    normalized_value: str
    source_location: str
    context: str | None = None
    evidence_ids: tuple[UUID, ...] = field(default_factory=tuple)
    extracted_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        require_nonempty(self.original_value, "original_value")
        require_nonempty(self.normalized_value, "normalized_value")
        require_nonempty(self.source_location, "source_location")
        require_timezone_aware(self.extracted_at, "extracted_at")
