from contextlib import nullcontext

import pytest
from database_guard import (
    DESTRUCTIVE_RESET_ENV,
    assert_safe_test_database,
    derive_test_database_url,
    destructive_reset_enabled,
    reset_test_schema,
)
from sqlalchemy.engine import make_url


class RecordingConnection:
    def __init__(self) -> None:
        self.statements: list[str] = []

    def execute(self, statement: object) -> None:
        self.statements.append(str(statement))


class RecordingEngine:
    def __init__(self) -> None:
        self.connection = RecordingConnection()

    def begin(self):
        return nullcontext(self.connection)


def _url(database: str):
    return make_url(f"postgresql+psycopg://user:example-password@127.0.0.1:55432/{database}")


def test_derive_test_database_url_adds_expected_suffix() -> None:
    assert derive_test_database_url(_url("fishtrace")).database == "fishtrace_test"


def test_derive_test_database_url_keeps_existing_test_database() -> None:
    assert derive_test_database_url(_url("fishtrace_test")).database == "fishtrace_test"


@pytest.mark.parametrize(
    "database",
    ["fishtrace", "postgres", "prod", "production_test", "development_test", "FishTrace_test", "db_test_prod"],
)
def test_unsafe_database_names_are_rejected(database: str) -> None:
    with pytest.raises(ValueError, match="non-test database"):
        assert_safe_test_database(_url(database))


def test_destructive_reset_requires_explicit_truthy_value(monkeypatch) -> None:
    monkeypatch.delenv(DESTRUCTIVE_RESET_ENV, raising=False)
    assert destructive_reset_enabled() is False

    monkeypatch.setenv(DESTRUCTIVE_RESET_ENV, "yes")
    assert destructive_reset_enabled() is True

    monkeypatch.setenv(DESTRUCTIVE_RESET_ENV, "maybe")
    assert destructive_reset_enabled() is False


def test_reset_skips_without_explicit_guard(monkeypatch) -> None:
    monkeypatch.delenv(DESTRUCTIVE_RESET_ENV, raising=False)
    engine = RecordingEngine()

    reset_test_schema(engine, _url("fishtrace_test"))

    assert engine.connection.statements == []


def test_reset_executes_for_safe_test_database_when_enabled(monkeypatch) -> None:
    monkeypatch.setenv(DESTRUCTIVE_RESET_ENV, "1")
    engine = RecordingEngine()

    reset_test_schema(engine, _url("fishtrace_test"))

    assert len(engine.connection.statements) == 2
    assert "DROP SCHEMA" in engine.connection.statements[0]
    assert "CREATE SCHEMA" in engine.connection.statements[1]


def test_reset_refuses_unsafe_database_even_when_enabled(monkeypatch) -> None:
    monkeypatch.setenv(DESTRUCTIVE_RESET_ENV, "1")
    engine = RecordingEngine()

    with pytest.raises(ValueError, match="non-test database"):
        reset_test_schema(engine, _url("fishtrace"))

    assert engine.connection.statements == []
