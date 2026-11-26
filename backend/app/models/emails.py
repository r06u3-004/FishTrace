from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, String, Text, Uuid
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models._common import TimestampMixin

if TYPE_CHECKING:
    from app.models.analysis_results import AnalysisResult
    from app.models.attachments import Attachment
    from app.models.auth_results import AuthResult
    from app.models.investigations import Investigation


class Email(Base, TimestampMixin):
    __tablename__ = "emails"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    investigation_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("investigations.id", ondelete="CASCADE"),
        index=True,
    )
    subject: Mapped[str | None] = mapped_column(String(512), nullable=True)
    sender: Mapped[str | None] = mapped_column(String(512), nullable=True)
    recipients: Mapped[list[object] | None] = mapped_column(JSONB, nullable=True)
    date_headers: Mapped[list[object] | None] = mapped_column(JSONB, nullable=True)
    parsed_json: Mapped[dict[str, object] | None] = mapped_column(JSONB, nullable=True)
    raw_evidence_sha256: Mapped[str] = mapped_column(String(64), index=True)
    raw_evidence_path: Mapped[str] = mapped_column(Text)
    received_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    investigation: Mapped[Investigation] = relationship(back_populates="emails")
    attachments: Mapped[list[Attachment]] = relationship(back_populates="email", cascade="all, delete-orphan")
    analysis_results: Mapped[list[AnalysisResult]] = relationship(back_populates="email", cascade="all, delete-orphan")
    auth_results: Mapped[list[AuthResult]] = relationship(back_populates="email", cascade="all, delete-orphan")
