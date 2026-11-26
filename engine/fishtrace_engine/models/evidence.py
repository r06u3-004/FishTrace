"""Evidence contracts for preserved forensic material."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from uuid import UUID

from fishtrace_engine.models.base import (
    SerializableModel,
    require_non_negative,
    require_nonempty,
    require_sha256,
    require_timezone_aware,
)


class EvidenceType(StrEnum):
    RAW_EMAIL = "raw_email"
    HEADER = "header"
    BODY = "body"
    ATTACHMENT = "attachment"
    DNS_RECORD = "dns_record"
    URL = "url"
    FILE = "file"
    OTHER = "other"


@dataclass(frozen=True, slots=True)
class Evidence(SerializableModel):
    """A single piece of evidence with source and integrity metadata."""

    id: UUID
    type: EvidenceType
    value: str
    source_location: str
    collected_at: datetime
    sha256: str | None = None
    size_bytes: int | None = None
    is_safe_representation: bool = False
    related_finding_ids: tuple[UUID, ...] = ()

    def __post_init__(self) -> None:
        require_nonempty(self.value, "value")
        require_nonempty(self.source_location, "source_location")
        require_timezone_aware(self.collected_at, "collected_at")
        if self.size_bytes is not None:
            require_non_negative(self.size_bytes, "size_bytes")
        object.__setattr__(self, "sha256", require_sha256(self.sha256))
