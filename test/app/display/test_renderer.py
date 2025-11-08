"""Unit tests for rendering functions."""

from unittest.mock import MagicMock, patch

import pytest

from qfold.app.display.renderer import display_sequence
from qfold.sequence.alphabet import HPAlphabet
from qfold.sequence.sequence import Sequence


@pytest.fixture(scope="function")
def hp_sequence() -> Sequence:
    """
    Fixture providing an HP sequence instance.

    Returns:
        Sequence instance with "HPPH" for testing.
    """
    return Sequence("HPPH", HPAlphabet())


@patch("qfold.app.display.renderer.console")
def test_display_sequence_calls_console_print(
    mock_console: MagicMock, hp_sequence: Sequence
) -> None:
    """
    Test that display_sequence calls console.print.

    The function should output to console.
    """
    display_sequence(hp_sequence)
    # Should be called at least twice (sequence and mapping)
    assert mock_console.print.call_count >= 2


@patch("qfold.app.display.renderer.get_char_color_map")
@patch("qfold.app.display.renderer.console")
def test_display_sequence_uses_color_map(
    mock_console: MagicMock,
    mock_color_map: MagicMock,
    hp_sequence: Sequence,
) -> None:
    """
    Test that display_sequence uses color mapping.

    The function should get color mapping for characters.
    """
    mock_color_map.return_value = {"H": "red", "P": "blue"}
    display_sequence(hp_sequence)
    # Verify color map was called with unique chars
    mock_color_map.assert_called_once()
    call_args = mock_color_map.call_args[0][0]
    assert "H" in call_args
    assert "P" in call_args


@patch("qfold.app.display.renderer.console")
def test_display_sequence_shows_sequence_string(
    mock_console: MagicMock, hp_sequence: Sequence
) -> None:
    """
    Test that display_sequence displays the sequence string.

    The sequence should be displayed with "Sequence: " prefix.
    """
    display_sequence(hp_sequence)
    # Check that first print call contains sequence
    first_call = mock_console.print.call_args_list[0]
    assert "Sequence:" in str(first_call)


@patch("qfold.app.display.renderer.console")
def test_display_sequence_shows_mapping(
    mock_console: MagicMock, hp_sequence: Sequence
) -> None:
    """
    Test that display_sequence displays the encoded mapping.

    The mapping should be displayed with "Mapping:" prefix.
    """
    display_sequence(hp_sequence)
    # Check that second print call contains mapping
    calls = [str(call) for call in mock_console.print.call_args_list]
    mapping_call = [c for c in calls if "Mapping" in c]
    assert len(mapping_call) > 0


@patch("qfold.app.display.renderer.console")
def test_display_sequence_with_different_sequence(
    mock_console: MagicMock,
) -> None:
    """
    Test display_sequence with different sequence.

    Function should work with various sequences.
    """
    seq = Sequence("H", HPAlphabet())
    display_sequence(seq)
    assert mock_console.print.call_count >= 2


@patch("qfold.app.display.renderer.console")
def test_display_sequence_empty_sequence(mock_console: MagicMock) -> None:
    """
    Test display_sequence with empty sequence.

    Function should handle empty sequences gracefully.
    """
    seq = Sequence("", HPAlphabet())
    display_sequence(seq)
    # Should still print (empty sequence and empty mapping)
    assert mock_console.print.call_count >= 2

