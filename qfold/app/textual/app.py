"""Textual TUI application for qfold."""

from textual.app import App


class QFoldApp(App):
    """
    Main Textual application for qfold.

    This is a placeholder for the Textual app implementation.
    """

    def __init__(self) -> None:
        """Initialize the Textual application."""
        super().__init__()


def create_textual_app() -> QFoldApp:
    """
    Create a new Textual application instance.

    Returns:
        QFoldApp instance.
    """
    return QFoldApp()

