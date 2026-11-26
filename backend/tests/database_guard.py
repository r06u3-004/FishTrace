from __future__ import annotations

import os
import re
from contextlib import AbstractContextManager
from typing import Protocol

from sqlalchemy import text
from sqlalchemy.engine import URL, make_url

DESTRUCTIVE_RESET_ENV = "FISHTRACE_ALLOW_TEST_DB_RESET"
TEST_DATABASE_SUFFIX = "_test"

_TEST_DATABASE_RE = re.compile(r"^[a-z][a-z0-9_]*_test$")
_RESERVED_DATABASE_ROOTS = frozenset(
    {
        "postgres",
        "template0",
        "template1",
        "development",
        "production",
        "prod",
        "main",
    }
)
_RESERVED_DATABASE_NAMES = _RESERVED_DATABASE_ROOTS | {
    f"{root}{TEST_DATABASE_SUFFIX}" for root in _RESERVED_DATABASE_ROOTS
}
_TRUTHY_VALUES = frozenset({"1", "true", "yes", "on"})


class _Connection(Protocol):
    def execute(self, statement: object) -> object: ...


class _Engine(Protocol):
    def begin(self) -> AbstractContextManager[_Connection]: ...


def destructive_reset_enabled() -> bool:
    return os.environ.get(DESTRUCTIVE_RESET_ENV, "").strip().lower() in _TRUTHY_VALUES


def _database_name(url: str | URL) -> str:
    parsed = make_url(url) if isinstance(url, str) else url
    name = parsed.database
    if not name:
        raise ValueError("Test database name is missing")
    return name


def assert_safe_test_database(url: str | URL) -> None:
    name = _database_name(url)
    if name in _RESERVED_DATABASE_NAMES or not _TEST_DATABASE_RE.fullmatch(name):
        raise ValueError("Refusing to use a non-test database for destructive test setup")


def derive_test_database_url(database_url: str | URL) -> URL:
    parsed = make_url(database_url) if isinstance(database_url, str) else database_url
    current = parsed.database
    if not current:
        raise ValueError("Test database name could not be derived")
    candidate = current if current.endswith(TEST_DATABASE_SUFFIX) else f"{current}{TEST_DATABASE_SUFFIX}"
    result = parsed.set(database=candidate)
    assert_safe_test_database(result)
    return result


def reset_test_schema(engine: _Engine, database_url: str | URL) -> None:
    assert_safe_test_database(database_url)
    if not destructive_reset_enabled():
        return
    with engine.begin() as connection:
        connection.execute(text("DROP SCHEMA public CASCADE"))
        connection.execute(text("CREATE SCHEMA public"))
