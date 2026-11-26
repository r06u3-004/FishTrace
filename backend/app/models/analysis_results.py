from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Enum, Float, ForeignKey, String, Uuid, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import Severity

if TYPE_CHECKING:
    from app.models.emails import Email


class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    email_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("emails.id", ondelete="CASCADE"), index=True)
    engine_version: Mapped[str] = mapped_column(String(32))
    findings_json: Mapped[list[object]] = mapped_column(JSONB)
    risk_score: Mapped[float] = mapped_column(Float, default=0.0)
    risk_level: Mapped[Severity] = mapped_column(Enum(Severity, native_enum=False, length=16), default=Severity.low)
    completed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    email: Mapped[Email] = relationship(back_populates="analysis_results")
