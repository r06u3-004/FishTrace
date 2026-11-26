"""Authentication result contracts with explicit non-failure states."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum, auto

from fishtrace_engine.exceptions import ContractValidationError
from fishtrace_engine.models.base import SerializableModel, require_timezone_aware


class AuthStatus(StrEnum):
    PASS = auto()
    FAIL = auto()
    SOFTFAIL = auto()
    NEUTRAL = auto()
    NONE = auto()
    TEMPERROR = auto()
    PERMERROR = auto()
    NOT_CHECKED = auto()
    INDETERMINATE = auto()


def _coerce_status(value: AuthStatus | str, field_name: str) -> AuthStatus:
    if isinstance(value, AuthStatus):
        return value
    if isinstance(value, str):
        candidate = value.strip()
        for normalized in (candidate.upper(), candidate.lower()):
            try:
                return AuthStatus(normalized)
            except ValueError:
                continue
        raise ContractValidationError(f"{field_name} is not a supported authentication status")
    raise ContractValidationError(f"{field_name} must be an AuthStatus value")


@dataclass(frozen=True, slots=True)
class AuthenticationResult(SerializableModel):
    """SPF, DKIM and DMARC outcomes; missing data stays NOT_CHECKED or NONE."""

    spf: AuthStatus | str = AuthStatus.NOT_CHECKED
    dkim: AuthStatus | str = AuthStatus.NOT_CHECKED
    dmarc: AuthStatus | str = AuthStatus.NOT_CHECKED
    spf_alignment: AuthStatus | str = AuthStatus.NOT_CHECKED
    dkim_alignment: AuthStatus | str = AuthStatus.NOT_CHECKED
    details: dict[str, str] = field(default_factory=dict)
    evaluated_at: datetime | None = None

    def __post_init__(self) -> None:
        for field_name in ("spf", "dkim", "dmarc", "spf_alignment", "dkim_alignment"):
            object.__setattr__(self, field_name, _coerce_status(getattr(self, field_name), field_name))
        if self.evaluated_at is not None:
            require_timezone_aware(self.evaluated_at, "evaluated_at")
