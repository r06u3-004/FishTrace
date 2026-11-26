from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models._common import TimestampMixin

if TYPE_CHECKING:
    from app.models.investigations import Investigation
    from app.models.users import User


class AnalystNote(Base, TimestampMixin):
    __tablename__ = "analyst_notes"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    investigation_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("investigations.id", ondelete="CASCADE"), index=True
    )
    author_id: Mapped[UUID | None] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    body: Mapped[str] = mapped_column(Text)

    investigation: Mapped[Investigation] = relationship(back_populates="notes")
    author: Mapped[User | None] = relationship(back_populates="notes")
