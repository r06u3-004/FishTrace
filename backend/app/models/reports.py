from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import Enum, ForeignKey, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models._common import TimestampMixin
from app.models.enums import ReportFormat

if TYPE_CHECKING:
    from app.models.investigations import Investigation


class Report(Base, TimestampMixin):
    __tablename__ = "reports"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    investigation_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("investigations.id", ondelete="CASCADE"), index=True
    )
    format: Mapped[ReportFormat] = mapped_column(
        Enum(ReportFormat, native_enum=False, length=16), default=ReportFormat.html
    )
    path: Mapped[str] = mapped_column(Text)
    sha256: Mapped[str] = mapped_column(String(64), index=True)
    generated_by: Mapped[str] = mapped_column(String(128))

    investigation: Mapped[Investigation] = relationship(back_populates="reports")
