"""CLI interface for qfold."""

from qfold.app.cli.commands import create_cli_app

app_cli = create_cli_app()

__all__ = ["app_cli"]
