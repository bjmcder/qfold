"""Unit tests for sequence processing."""

import pytest

from qfold.io.sequence import process_sequence
from qfold.sequence.sequence import Sequence


def test_process_sequence_with_hp_alphabet() -> None:
    """
    Test processing sequence with 'hp' alphabet.

    process_sequence should return a valid Sequence object.
    """
    seq = process_sequence("HPPH", "hp")
    assert isinstance(seq, Sequence)
    assert str(seq) == "HPPH"


def test_process_sequence_with_auto_alphabet() -> None:
    """
    Test processing sequence with 'auto' alphabet.

    process_sequence should infer alphabet and return Sequence.
    """
    seq = process_sequence("HPPH", "auto")
    assert isinstance(seq, Sequence)
    assert str(seq) == "HPPH"


def test_process_sequence_normalizes_input() -> None:
    """
    Test that process_sequence normalizes input.

    Input should be trimmed and converted to uppercase.
    """
    seq = process_sequence("  hpph  ", "hp")
    assert str(seq) == "HPPH"


def test_process_sequence_invalid_alphabet_raises_error() -> None:
    """
    Test that invalid alphabet name raises ValueError.

    Unsupported alphabet names should raise ValueError.
    """
    with pytest.raises(ValueError, match="Unsupported alphabet"):
        process_sequence("HPPH", "invalid")


def test_process_sequence_invalid_sequence_raises_error() -> None:
    """
    Test that invalid sequence raises ValueError.

    Sequences with invalid characters should raise ValueError.
    """
    with pytest.raises(ValueError, match="Invalid characters"):
        process_sequence("HPAX", "hp")


def test_process_sequence_empty_sequence() -> None:
    """
    Test processing empty sequence.

    Empty sequences should be valid.
    """
    seq = process_sequence("", "hp")
    assert isinstance(seq, Sequence)
    assert str(seq) == ""


def test_process_sequence_single_character() -> None:
    """
    Test processing single character sequence.

    Single character sequences should work.
    """
    seq = process_sequence("H", "hp")
    assert isinstance(seq, Sequence)
    assert str(seq) == "H"
    assert seq.encoded() == [1]


def test_process_sequence_uses_correct_alphabet() -> None:
    """
    Test that process_sequence uses correct alphabet.

    The returned sequence should use the specified alphabet.
    """
    seq = process_sequence("HPPH", "hp")
    # Verify encoding matches HP alphabet (H=1, P=0)
    assert seq.encoded() == [1, 0, 0, 1]


def test_process_sequence_auto_normalizes_before_inference() -> None:
    """
    Test that auto alphabet normalizes before inference.

    Sequence should be normalized before alphabet inference.
    """
    # This should work even with lowercase/whitespace
    seq = process_sequence("  hpph  ", "auto")
    assert str(seq) == "HPPH"


def test_process_sequence_whitespace_handling() -> None:
    """
    Test that process_sequence handles whitespace correctly.

    Leading and trailing whitespace should be trimmed.
    """
    seq1 = process_sequence("HPPH", "hp")
    seq2 = process_sequence("  HPPH  ", "hp")
    seq3 = process_sequence("\tHPPH\n", "hp")
    assert str(seq1) == str(seq2) == str(seq3)

