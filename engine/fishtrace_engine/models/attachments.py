"""Attachment metadata and analysis state contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from uuid import UUID

from fishtrace_engine.models.base import (
    SerializableModel,
    require_non_negative,
    require_nonempty,
    require_sha256,
)


class AttachmentAnalysisStatus(StrEnum):
    NOT_ANALYZED = "not_analyzed"
    ANALYZED = "analyzed"
    SKIPPED = "skipped"
    ERROR = "error"


@dataclass(frozen=True, slots=True)
class AttachmentAnalysis(SerializableModel):
    """Safe metadata for an attachment; no file content is executed."""

    filename: str
    sha256: str
    size_bytes: int
    mime_type: str | None = None
    detected_file_type: str | None = None
    suspicious_characteristics: tuple[str, ...] = field(default_factory=tuple)
    status: AttachmentAnalysisStatus = AttachmentAnalysisStatus.NOT_ANALYZED
    finding_ids: tuple[UUID, ...] = field(default_factory=tuple)
    evidence_ids: tuple[UUID, ...] = field(default_factory=tuple)
    error: str | None = None

    def __post_init__(self) -> None:
        require_nonempty(self.filename, "filename")
        object.__setattr__(self, "sha256", require_sha256(self.sha256, "sha256"))
        require_non_negative(self.size_bytes, "size_bytes")
        if self.error is not None:
            require_nonempty(self.error, "error")
