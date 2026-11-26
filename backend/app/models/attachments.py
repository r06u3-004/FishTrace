from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, Integer, String, Text, Uuid
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.emails import Email


class Attachment(Base):
    __tablename__ = "attachments"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    email_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("emails.id", ondelete="CASCADE"), index=True)
    filename: Mapped[str | None] = mapped_column(Text, nullable=True)
    mime_type: Mapped[str | None] = mapped_column(String(255), nullable=True)
    size: Mapped[int] = mapped_column(Integer, default=0)
    md5: Mapped[str] = mapped_column(String(32), index=True)
    sha1: Mapped[str] = mapped_column(String(40), index=True)
    sha256: Mapped[str] = mapped_column(String(64), index=True)
    flags_json: Mapped[dict[str, object] | None] = mapped_column(JSONB, nullable=True)
    disposition: Mapped[str | None] = mapped_column(String(64), nullable=True)

    email: Mapped[Email] = relationship(back_populates="attachments")
