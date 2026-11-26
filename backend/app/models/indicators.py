from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Enum, Float, Index, String, Text, UniqueConstraint, Uuid
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import IndicatorType

if TYPE_CHECKING:
    from app.models.indicator_sightings import IndicatorSighting
    from app.models.intel_results import IntelResult


class Indicator(Base):
    __tablename__ = "indicators"
    __table_args__ = (
        UniqueConstraint("type", "normalized_value", name="uq_indicators_type_normalized"),
        Index("ix_indicators_type_value", "type", "normalized_value"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    type: Mapped[IndicatorType] = mapped_column(Enum(IndicatorType, native_enum=False, length=32), index=True)
    value: Mapped[str] = mapped_column(Text)
    normalized_value: Mapped[str] = mapped_column(Text)
    classification: Mapped[str | None] = mapped_column(String(64), nullable=True)
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    first_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    last_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    reputation_json: Mapped[dict[str, object] | None] = mapped_column(JSONB, nullable=True)

    sightings: Mapped[list[IndicatorSighting]] = relationship(back_populates="indicator", cascade="all, delete-orphan")
    intel_results: Mapped[list[IntelResult]] = relationship(back_populates="indicator", cascade="all, delete-orphan")
