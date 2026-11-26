from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models._common import TimestampMixin
from app.models.enums import InvestigationStatus, Severity

if TYPE_CHECKING:
    from app.models.activity_events import ActivityEvent
    from app.models.analyst_notes import AnalystNote
    from app.models.campaigns import Campaign
    from app.models.emails import Email
    from app.models.indicator_sightings import IndicatorSighting
    from app.models.reports import Report
    from app.models.users import User


class Investigation(Base, TimestampMixin):
    __tablename__ = "investigations"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(String(200))
    status: Mapped[InvestigationStatus] = mapped_column(
        Enum(InvestigationStatus, native_enum=False, length=32),
        default=InvestigationStatus.open,
        index=True,
    )
    severity: Mapped[Severity] = mapped_column(
        Enum(Severity, native_enum=False, length=16), default=Severity.medium, index=True
    )
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    owner_id: Mapped[UUID | None] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    opened_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    owner: Mapped[User | None] = relationship(back_populates="investigations")
    emails: Mapped[list[Email]] = relationship(back_populates="investigation", cascade="all, delete-orphan")
    notes: Mapped[list[AnalystNote]] = relationship(back_populates="investigation", cascade="all, delete-orphan")
    events: Mapped[list[ActivityEvent]] = relationship(back_populates="investigation", cascade="all, delete-orphan")
    reports: Mapped[list[Report]] = relationship(back_populates="investigation", cascade="all, delete-orphan")
    campaigns: Mapped[list[Campaign]] = relationship(
        secondary="campaign_investigations", back_populates="investigations"
    )
    sightings: Mapped[list[IndicatorSighting]] = relationship(
        back_populates="investigation", cascade="all, delete-orphan"
    )
