from dev.app import app
from typer.testing import CliRunner
from unittest import mock

runner = CliRunner()

def test_main():
    result = runner.invoke(app)

    assert result.exit_code == 0
