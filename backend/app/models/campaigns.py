from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    String,
    Table,
    Text,
    Uuid,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models._common import TimestampMixin
from app.models.enums import CampaignStatus, Severity

campaign_investigations = Table(
    "campaign_investigations",
    Base.metadata,
    Column(
        "campaign_id",
        Uuid(as_uuid=True),
        ForeignKey("campaigns.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "investigation_id",
        Uuid(as_uuid=True),
        ForeignKey("investigations.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


if TYPE_CHECKING:
    from app.models.investigations import Investigation


class Campaign(Base, TimestampMixin):
    __tablename__ = "campaigns"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(200), unique=True, index=True)
    classification: Mapped[str | None] = mapped_column(String(120), nullable=True)
    status: Mapped[CampaignStatus] = mapped_column(
        Enum(CampaignStatus, native_enum=False, length=32),
        default=CampaignStatus.active,
        index=True,
    )
    severity: Mapped[Severity] = mapped_column(Enum(Severity, native_enum=False, length=16), default=Severity.medium)
    first_seen: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_seen: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    investigations: Mapped[list[Investigation]] = relationship(
        secondary=campaign_investigations, back_populates="campaigns"
    )
