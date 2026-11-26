"""Top-level forensic result contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from uuid import UUID

from fishtrace_engine.models.attachments import AttachmentAnalysis
from fishtrace_engine.models.authentication import AuthenticationResult
from fishtrace_engine.models.base import (
    SerializableModel,
    new_id,
    require_nonempty,
    require_timezone_aware,
    utc_now,
)
from fishtrace_engine.models.evidence import Evidence
from fishtrace_engine.models.findings import Finding
from fishtrace_engine.models.indicators import Indicator
from fishtrace_engine.models.risk import RiskAssessment


class AnalysisStatus(StrEnum):
    NOT_RUN = "not_run"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    PARTIAL = "partial"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class EmailMetadata(SerializableModel):
    """Parsed email header values attached to an analysis result."""

    subject: str | None = None
    sender: str | None = None
    recipients: tuple[str, ...] = field(default_factory=tuple)
    message_id: str | None = None
    sent_at: datetime | None = None
    raw_date_header: str | None = None

    def __post_init__(self) -> None:
        for recipient in self.recipients:
            require_nonempty(recipient, "recipient")
        if self.sent_at is not None:
            require_timezone_aware(self.sent_at, "sent_at")


@dataclass(frozen=True, slots=True)
class EmailAnalysisResult(SerializableModel):
    """Complete, serializable output of one email analysis."""

    original_filename: str
    engine_version: str
    analysis_id: UUID = field(default_factory=new_id)
    analyzed_at: datetime = field(default_factory=utc_now)
    status: AnalysisStatus = AnalysisStatus.NOT_RUN
    metadata: EmailMetadata = field(default_factory=EmailMetadata)
    authentication: AuthenticationResult = field(default_factory=AuthenticationResult)
    header_findings: tuple[Finding, ...] = field(default_factory=tuple)
    indicators: tuple[Indicator, ...] = field(default_factory=tuple)
    attachments: tuple[AttachmentAnalysis, ...] = field(default_factory=tuple)
    risk: RiskAssessment = field(default_factory=RiskAssessment)
    findings: tuple[Finding, ...] = field(default_factory=tuple)
    evidence: tuple[Evidence, ...] = field(default_factory=tuple)
    limitations: tuple[str, ...] = field(default_factory=tuple)
    warnings: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        require_nonempty(self.original_filename, "original_filename")
        require_nonempty(self.engine_version, "engine_version")
        require_timezone_aware(self.analyzed_at, "analyzed_at")
