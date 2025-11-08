"""Textual TUI application for qfold."""

from qfold.app.textual.app import create_textual_app


def launch_textual_app() -> None:
    """
    Launch the Textual TUI application.

    This is a placeholder for the Textual app implementation.
    """
    textual_app = create_textual_app()
    textual_app.run()

__all__ = ["launch_textual_app"]
