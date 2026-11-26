from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Enum, ForeignKey, Uuid, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import AuthStatus

if TYPE_CHECKING:
    from app.models.emails import Email


class AuthResult(Base):
    __tablename__ = "auth_results"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    email_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("emails.id", ondelete="CASCADE"), index=True)
    spf_status: Mapped[AuthStatus] = mapped_column(
        Enum(AuthStatus, native_enum=False, length=24), default=AuthStatus.unavailable
    )
    dkim_status: Mapped[AuthStatus] = mapped_column(
        Enum(AuthStatus, native_enum=False, length=24), default=AuthStatus.unavailable
    )
    dmarc_status: Mapped[AuthStatus] = mapped_column(
        Enum(AuthStatus, native_enum=False, length=24), default=AuthStatus.unavailable
    )
    spf_alignment: Mapped[AuthStatus] = mapped_column(
        Enum(AuthStatus, native_enum=False, length=24), default=AuthStatus.unavailable
    )
    dkim_alignment: Mapped[AuthStatus] = mapped_column(
        Enum(AuthStatus, native_enum=False, length=24), default=AuthStatus.unavailable
    )
    raw_json: Mapped[dict[str, object] | None] = mapped_column(JSONB, nullable=True)
    evaluated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    email: Mapped[Email] = relationship(back_populates="auth_results")
