"""Explainable risk assessment contracts without embedded scoring rules."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from uuid import UUID

from fishtrace_engine.exceptions import ContractValidationError
from fishtrace_engine.models.base import SerializableModel, require_confidence


class RiskLevel(StrEnum):
    UNDETERMINED = "undetermined"
    INFORMATIONAL = "informational"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(frozen=True, slots=True)
class RiskAssessment(SerializableModel):
    """Explanation of risk; scoring logic is intentionally not implemented here."""

    level: RiskLevel = RiskLevel.UNDETERMINED
    confidence: float = 0.0
    contributing_finding_ids: tuple[UUID, ...] = field(default_factory=tuple)
    reasons: tuple[str, ...] = field(default_factory=tuple)
    recommendations: tuple[str, ...] = field(default_factory=tuple)
    score: float | None = None
    score_model: str | None = None

    def __post_init__(self) -> None:
        require_confidence(self.confidence)
        if self.score is not None and not 0.0 <= self.score <= 100.0:
            raise ContractValidationError("score must be between 0.0 and 100.0")
        if self.score is not None and self.score_model is None:
            raise ContractValidationError("score_model is required when score is provided")
