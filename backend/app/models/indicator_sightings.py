from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Text, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.indicators import Indicator
    from app.models.investigations import Investigation


class IndicatorSighting(Base):
    __tablename__ = "indicator_sightings"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    indicator_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("indicators.id", ondelete="CASCADE"), index=True
    )
    investigation_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("investigations.id", ondelete="CASCADE"), index=True
    )
    source: Mapped[str] = mapped_column(Text)
    context: Mapped[str | None] = mapped_column(Text, nullable=True)
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    indicator: Mapped[Indicator] = relationship(back_populates="sightings")
    investigation: Mapped[Investigation] = relationship(back_populates="sightings")
