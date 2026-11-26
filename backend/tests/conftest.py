import importlib
from collections.abc import Generator

import pytest
from database_guard import derive_test_database_url, reset_test_schema
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, inspect
from sqlalchemy.engine import Engine, Inspector
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.base import Base
from app.db.session import get_db
from app.main import app

settings = get_settings()
TEST_DATABASE_URL = derive_test_database_url(settings.database_url)
importlib.import_module("app.models")


@pytest.fixture(scope="session")
def engine() -> Generator[Engine]:
    test_engine = create_engine(TEST_DATABASE_URL, pool_pre_ping=True)
    reset_test_schema(test_engine, TEST_DATABASE_URL)
    Base.metadata.create_all(test_engine)
    yield test_engine
    test_engine.dispose()


@pytest.fixture()
def db_session(engine: Engine) -> Generator[Session]:
    with Session(engine, expire_on_commit=False) as session:
        yield session
        session.rollback()


@pytest.fixture()
def client(db_session: Session) -> Generator[TestClient]:
    def override_get_db() -> Generator[Session]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture()
def schema_inspector(engine: Engine) -> Inspector:
    return inspect(engine)
