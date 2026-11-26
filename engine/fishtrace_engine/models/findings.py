"""Finding contracts for detected observations and anomalies."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from uuid import UUID

from fishtrace_engine.models.base import (
    SerializableModel,
    require_confidence,
    require_nonempty,
    require_timezone_aware,
)


class FindingCategory(StrEnum):
    AUTHENTICATION = "authentication"
    HEADER = "header"
    CONTENT = "content"
    INDICATOR = "indicator"
    ATTACHMENT = "attachment"
    STRUCTURAL = "structural"
    RISK = "risk"
    OTHER = "other"


class FindingSeverity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(frozen=True, slots=True)
class Finding(SerializableModel):
    """A detected observation, independent of its confidence score."""

    id: UUID
    category: FindingCategory
    title: str
    description: str
    severity: FindingSeverity
    confidence: float
    evidence_ids: tuple[UUID, ...]
    detection_source: str
    observed_at: datetime | None = None

    def __post_init__(self) -> None:
        require_nonempty(self.title, "title")
        require_nonempty(self.description, "description")
        require_nonempty(self.detection_source, "detection_source")
        require_confidence(self.confidence)
        if self.observed_at is not None:
            require_timezone_aware(self.observed_at, "observed_at")
