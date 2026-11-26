from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import Boolean, Enum, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models._common import TimestampMixin
from app.models.enums import UserRole

if TYPE_CHECKING:
    from app.models.analyst_notes import AnalystNote
    from app.models.investigations import Investigation


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    username: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(Text)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, native_enum=False, length=32), default=UserRole.analyst, index=True
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    investigations: Mapped[list[Investigation]] = relationship(back_populates="owner")
    notes: Mapped[list[AnalystNote]] = relationship(back_populates="author")
