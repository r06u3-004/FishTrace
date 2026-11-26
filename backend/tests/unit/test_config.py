from pathlib import Path

import pytest
from pydantic import ValidationError

from app.core.config import PROJECT_ROOT, Settings, _reject_unknown_environment_names


def test_project_paths_are_absolute():
    settings = Settings(_env_file=None, secret_key="test-secret-key-long-enough")

    assert settings.evidence_dir == PROJECT_ROOT / Path("backend/evidence")
    assert settings.report_dir == PROJECT_ROOT / Path("reports")


def test_cors_origins_are_split_and_trimmed():
    settings = Settings(
        _env_file=None,
        secret_key="test-secret-key-long-enough",
        cors_origins="http://a, http://b ",
    )

    assert settings.cors_origin_list == ["http://a", "http://b"]


def test_cors_defaults_are_restricted():
    settings = Settings(_env_file=None, secret_key="test-secret-key-long-enough")

    assert settings.debug is False
    assert settings.cors_allow_credentials is False
    assert "*" not in settings.cors_method_list + settings.cors_header_list
    assert settings.cors_method_list == ["GET", "POST", "PATCH", "DELETE", "OPTIONS"]


def test_wildcard_cors_origin_is_rejected():
    with pytest.raises(ValidationError):
        Settings(_env_file=None, secret_key="test-secret-key-long-enough", cors_origins="*")


def test_debug_is_rejected_in_production():
    with pytest.raises(ValidationError, match="Debug must be disabled"):
        Settings(_env_file=None, secret_key="test-secret-key-long-enough", environment="production", debug=True)


def test_unknown_environment_name_is_rejected():
    with pytest.raises(ValueError, match="Unknown FISHTRACE"):
        Settings(
            _env_file=None,
            _env={"FISHTRACE_UNKNOWN_OPTION": "x"},
            secret_key="test-secret-key-long-enough",
        )


def test_reserved_environment_names_are_allowed():
    _reject_unknown_environment_names({"FISHTRACE_PGPORT": "55432"})
    _reject_unknown_environment_names({"FISHTRACE_ALLOW_TEST_DB_RESET": "1"})


def test_missing_secret_key_is_rejected(monkeypatch):
    monkeypatch.delenv("FISHTRACE_SECRET_KEY", raising=False)

    with pytest.raises(ValueError, match="FISHTRACE_SECRET_KEY"):
        Settings(_env_file=None)


def test_secret_validation_does_not_echo_the_secret():
    secret = "s3cr3t-shrt"
    with pytest.raises(ValueError) as exc_info:
        Settings(_env_file=None, secret_key=secret)

    assert secret not in str(exc_info.value)
