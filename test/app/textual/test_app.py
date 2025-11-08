"""Unit tests for Textual application."""

import pytest
from textual.app import App

from qfold.app.textual.app import QFoldApp, create_textual_app


def test_qfold_app_is_textual_app() -> None:
    """
    Test that QFoldApp is a subclass of App.

    QFoldApp should inherit from textual.app.App.
    """
    assert issubclass(QFoldApp, App)


def test_create_textual_app_returns_qfold_app() -> None:
    """
    Test that create_textual_app returns QFoldApp instance.

    The function should return a QFoldApp instance.
    """
    app = create_textual_app()
    assert isinstance(app, QFoldApp)


def test_qfold_app_can_be_instantiated() -> None:
    """
    Test that QFoldApp can be instantiated directly.

    QFoldApp should be instantiable.
    """
    app = QFoldApp()
    assert app is not None
    assert isinstance(app, QFoldApp)


def test_qfold_app_inherits_from_app() -> None:
    """
    Test that QFoldApp properly inherits from App.

    QFoldApp should have App's functionality.
    """
    app = QFoldApp()
    # Check that it has App attributes
    assert hasattr(app, "run")

