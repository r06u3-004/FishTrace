from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, String, Text, UniqueConstraint, Uuid, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.indicators import Indicator


class IntelResult(Base):
    __tablename__ = "intel_results"
    __table_args__ = (
        UniqueConstraint(
            "indicator_id",
            "provider",
            "queried_at",
            name="uq_intel_results_indicator_provider_queried",
        ),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    indicator_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("indicators.id", ondelete="CASCADE"), index=True
    )
    provider: Mapped[str] = mapped_column(String(64))
    status: Mapped[str] = mapped_column(String(32))
    data_json: Mapped[dict[str, object] | None] = mapped_column(JSONB, nullable=True)
    queried_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    error: Mapped[str | None] = mapped_column(Text, nullable=True)

    indicator: Mapped[Indicator] = relationship(back_populates="intel_results")
