from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, String, Text, Uuid, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.investigations import Investigation


class ActivityEvent(Base):
    __tablename__ = "activity_events"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    investigation_id: Mapped[UUID | None] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("investigations.id", ondelete="CASCADE"), nullable=True, index=True
    )
    actor: Mapped[str] = mapped_column(String(128))
    event_type: Mapped[str] = mapped_column(String(64), index=True)
    description: Mapped[str] = mapped_column(Text)
    payload_json: Mapped[dict[str, object] | None] = mapped_column(JSONB, nullable=True)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)

    investigation: Mapped[Investigation | None] = relationship(back_populates="events")
