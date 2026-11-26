import os
from collections.abc import Mapping
from functools import lru_cache
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from dotenv import dotenv_values
from pydantic import Field, SecretStr, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[3]

_RESERVED_ENV_NAMES = frozenset(
    {
        "FISHTRACE_ALLOW_TEST_DB_RESET",
        "FISHTRACE_PGPORT",
    }
)


def _candidate_environment_keys(extra_env: Mapping[str, object] | None) -> set[str]:
    keys = set(os.environ)
    env_file = PROJECT_ROOT / ".env"
    if env_file.is_file():
        keys.update(dotenv_values(env_file))
    if extra_env is not None:
        keys.update(extra_env)
    return {key for key in keys if isinstance(key, str) and key.startswith("FISHTRACE_")}


def _reject_unknown_environment_names(extra_env: Mapping[str, object] | None) -> None:
    known = {f"FISHTRACE_{field.upper()}" for field in Settings.model_fields} | _RESERVED_ENV_NAMES
    unknown = sorted(_candidate_environment_keys(extra_env) - known)
    if unknown:
        raise ValueError("Unknown FISHTRACE_* configuration names: " + ", ".join(unknown))


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_prefix="FISHTRACE_",
        extra="forbid",
    )

    environment: str = "development"
    debug: bool = False
    secret_key: SecretStr = Field(default_factory=lambda: SecretStr(os.environ.get("FISHTRACE_SECRET_KEY", "")))
    database_url: str = "postgresql+psycopg://fishtrace@127.0.0.1:55432/fishtrace"
    cors_origins: str = "http://127.0.0.1:5173"
    cors_allow_credentials: bool = False
    cors_allow_methods: str = "GET,POST,PATCH,DELETE,OPTIONS"
    cors_allow_headers: str = "Authorization,Content-Type,Accept"
    upload_max_bytes: int = 26_214_400
    evidence_dir: Path = Path("./backend/evidence")
    report_dir: Path = Path("./reports")
    access_token_ttl_minutes: int = 480

    def __init__(self, **values: Any) -> None:
        extra_env = values.get("_env")
        _reject_unknown_environment_names(extra_env if isinstance(extra_env, Mapping) else None)
        super().__init__(**values)
        if len(self.secret_key.get_secret_value()) < 16:
            raise ValueError("FISHTRACE_SECRET_KEY must be set and contain at least 16 characters")

    @field_validator("evidence_dir", "report_dir", mode="before")
    @classmethod
    def resolve_project_path(cls, value: str | Path) -> Path:
        path = Path(value)
        return path if path.is_absolute() else PROJECT_ROOT / path

    @field_validator("cors_origins")
    @classmethod
    def validate_cors_origins(cls, value: str) -> str:
        origins = [origin.strip() for origin in value.split(",") if origin.strip()]
        if not origins:
            raise ValueError("At least one trusted CORS origin must be configured")
        if any(origin == "*" for origin in origins):
            raise ValueError("Wildcard CORS origins are not allowed")
        for origin in origins:
            parsed = urlparse(origin)
            if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                raise ValueError("CORS origins must be absolute http(s) URLs")
        return value

    @field_validator("cors_allow_methods", "cors_allow_headers")
    @classmethod
    def validate_cors_csv(cls, value: str) -> str:
        items = [item.strip() for item in value.split(",") if item.strip()]
        if not items:
            raise ValueError("CORS methods and headers must not be empty")
        if any(item == "*" for item in items):
            raise ValueError("Wildcard CORS methods and headers are not allowed")
        return value

    @model_validator(mode="after")
    def check_debug_in_production(self) -> "Settings":
        if self.environment.strip().lower() in {"prod", "production"} and self.debug:
            raise ValueError("Debug must be disabled in production environments")
        return self

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    @property
    def cors_method_list(self) -> list[str]:
        return [method.strip().upper() for method in self.cors_allow_methods.split(",") if method.strip()]

    @property
    def cors_header_list(self) -> list[str]:
        return [header.strip() for header in self.cors_allow_headers.split(",") if header.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
