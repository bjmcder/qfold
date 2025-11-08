"""Unit tests for CLI commands module."""

from unittest.mock import MagicMock, patch

import pytest
import typer

from qfold.app.cli.commands import create_cli_app


@pytest.fixture(scope="function")
def cli_app() -> typer.Typer:
    """
    Fixture providing a CLI app instance.

    Returns:
        Typer application instance.
    """
    return create_cli_app()


def test_create_cli_app_returns_typer() -> None:
    """
    Test that create_cli_app returns a Typer instance.

    The function should return a configured Typer application.
    """
    app = create_cli_app()
    assert isinstance(app, typer.Typer)


def test_cli_app_has_callback(cli_app: typer.Typer) -> None:
    """
    Test that the CLI app has a callback registered.

    The app should have a callback function configured.
    """
    assert cli_app.registered_callback is not None


@patch("qfold.app.cli.commands.process_sequence")
@patch("qfold.app.cli.commands.display_sequence")
def test_cli_callback_with_sequence(
    mock_display: MagicMock,
    mock_process: MagicMock,
    cli_app: typer.Typer,
) -> None:
    """
    Test that CLI callback processes sequence when provided.

    When a sequence is provided, it should be processed and displayed.
    """
    from qfold.sequence.alphabet import HPAlphabet
    from qfold.sequence.sequence import Sequence

    # Create a mock sequence
    mock_seq = Sequence("HPPH", HPAlphabet())
    mock_process.return_value = mock_seq

    # Create a mock context
    ctx = MagicMock()
    ctx.invoked_subcommand = None

    # Get the callback
    callback = cli_app.registered_callback.callback

    # Call the callback
    callback(ctx, sequence="HPPH", alphabet="hp")

    # Verify process_sequence was called
    mock_process.assert_called_once_with("HPPH", "hp")
    # Verify display_sequence was called
    mock_display.assert_called_once_with(mock_seq)


@patch("rich.console.Console")
def test_cli_callback_without_sequence(
    mock_console_class: MagicMock, cli_app: typer.Typer
) -> None:
    """
    Test that CLI callback shows usage when no sequence provided.

    When no sequence is provided, it should display usage message.
    """
    mock_console = MagicMock()
    mock_console_class.return_value = mock_console

    # Create a mock context
    ctx = MagicMock()
    ctx.invoked_subcommand = None

    # Get the callback
    callback = cli_app.registered_callback.callback

    # Call the callback
    callback(ctx, sequence=None, alphabet="auto")

    # Verify console.print was called
    assert mock_console.print.call_count >= 2


@patch("qfold.app.cli.commands.process_sequence")
@patch("rich.console.Console")
def test_cli_callback_handles_value_error(
    mock_console_class: MagicMock,
    mock_process: MagicMock,
    cli_app: typer.Typer,
) -> None:
    """
    Test that CLI callback handles ValueError exceptions.

    When process_sequence raises ValueError, it should be caught
    and displayed, then exit with code 1.
    """
    mock_console = MagicMock()
    mock_console_class.return_value = mock_console
    mock_process.side_effect = ValueError("Invalid sequence")

    # Create a mock context
    ctx = MagicMock()
    ctx.invoked_subcommand = None

    # Get the callback
    callback = cli_app.registered_callback.callback

    # Call the callback and expect typer.Exit
    with pytest.raises(typer.Exit) as exc_info:
        callback(ctx, sequence="INVALID", alphabet="hp")

    # Verify exit code is 1
    assert exc_info.value.exit_code == 1
    # Verify error was displayed
    mock_console.print.assert_called()


def test_cli_callback_with_different_alphabets(cli_app: typer.Typer) -> None:
    """
    Test that CLI callback accepts different alphabet options.

    The callback should accept 'hp' and 'auto' alphabet options.
    """
    from unittest.mock import MagicMock, patch

    with patch("qfold.app.cli.commands.process_sequence") as mock_process:
        from qfold.sequence.alphabet import HPAlphabet
        from qfold.sequence.sequence import Sequence

        mock_seq = Sequence("HPPH", HPAlphabet())
        mock_process.return_value = mock_seq

        ctx = MagicMock()
        ctx.invoked_subcommand = None
        callback = cli_app.registered_callback.callback

        # Test with 'hp'
        callback(ctx, sequence="HPPH", alphabet="hp")
        mock_process.assert_called_with("HPPH", "hp")

        # Test with 'auto'
        callback(ctx, sequence="HPPH", alphabet="auto")
        mock_process.assert_called_with("HPPH", "auto")

