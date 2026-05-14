"""Tests for the typer CLI."""

from __future__ import annotations

from unittest.mock import patch

from typer.testing import CliRunner

from websum.cli import app

runner = CliRunner()


def test_cli_version() -> None:
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "websum" in result.stdout


def test_cli_help() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "summarize" in result.stdout
    assert "translate" in result.stdout


def test_cli_summarize_invokes_summarizer() -> None:
    with patch("websum.cli.Summarizer") as mock_cls:
        mock_cls.return_value.summarize.return_value = "RESULT"
        result = runner.invoke(app, ["summarize", "https://example.com"])
    assert result.exit_code == 0
    assert "RESULT" in result.stdout


def test_cli_summarize_unknown_backend_fails() -> None:
    result = runner.invoke(app, ["summarize", "https://example.com", "--backend", "bogus"])
    assert result.exit_code != 0
