from uuid import UUID, uuid4

from sqlalchemy import Boolean, LargeBinary, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models._common import TimestampMixin


class IntegrationConfig(Base, TimestampMixin):
    """Provider configuration; ``encrypted_api_key`` is reserved for future AEAD ciphertext only."""

    __tablename__ = "integration_configs"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    provider: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    encrypted_api_key: Mapped[bytes | None] = mapped_column(LargeBinary, nullable=True)
    base_url: Mapped[str | None] = mapped_column(Text, nullable=True)
