import fishtrace_cli
import fishtrace_engine
from fishtrace_cli.main import app
from typer.testing import CliRunner

runner = CliRunner()


def test_packages_expose_versions():
    assert fishtrace_engine.__version__ == "0.1.0"
    assert fishtrace_cli.__version__ == "0.1.0"


def test_cli_version_command():
    result = runner.invoke(app, ["version"])

    assert result.exit_code == 0
    assert "FishTrace CLI 0.1.0 (engine 0.1.0)" in result.output
