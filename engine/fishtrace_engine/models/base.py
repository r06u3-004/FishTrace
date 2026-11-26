"""Shared validation and serialization helpers for forensic contracts."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import fields, is_dataclass
from datetime import UTC, datetime
from enum import Enum
from string import hexdigits
from typing import Any
from uuid import UUID

from fishtrace_engine.exceptions import ContractValidationError


def utc_now() -> datetime:
    return datetime.now(UTC)


def new_id() -> UUID:
    from uuid import uuid4

    return uuid4()


def require_timezone_aware(value: datetime, field_name: str) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ContractValidationError(f"{field_name} must be timezone-aware")
    return value


def require_nonempty(value: str, field_name: str) -> str:
    if not value.strip():
        raise ContractValidationError(f"{field_name} must not be empty")
    return value


def require_confidence(value: float, field_name: str = "confidence") -> float:
    if not 0.0 <= value <= 1.0:
        raise ContractValidationError(f"{field_name} must be between 0.0 and 1.0")
    return value


def require_non_negative(value: int, field_name: str) -> int:
    if value < 0:
        raise ContractValidationError(f"{field_name} must not be negative")
    return value


def require_sha256(value: str | None, field_name: str = "sha256") -> str | None:
    if value is None:
        return None
    if len(value) != 64 or any(char not in hexdigits for char in value):
        raise ContractValidationError(f"{field_name} must be a 64-character hexadecimal SHA-256 value")
    return value.lower()


def _serialize(value: Any) -> Any:
    if is_dataclass(value) and not isinstance(value, type):
        return {field.name: _serialize(getattr(value, field.name)) for field in fields(value)}
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, UUID):
        return str(value)
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, Mapping):
        return {str(key): _serialize(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set, frozenset)):
        return [_serialize(item) for item in value]
    return value


class SerializableModel:
    """Mixin that converts nested contracts into JSON-compatible primitives."""

    def to_dict(self) -> dict[str, Any]:
        return _serialize(self)
