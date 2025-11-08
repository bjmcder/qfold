"""Unit tests for alphabet selection and inference."""

import pytest

from qfold.io.alphabet import infer_alphabet, select_alphabet
from qfold.sequence.alphabet import HPAlphabet


def test_select_alphabet_hp() -> None:
    """
    Test selecting HP alphabet by name.

    select_alphabet('hp') should return HPAlphabet instance.
    """
    alphabet = select_alphabet("hp")
    assert isinstance(alphabet, HPAlphabet)


def test_select_alphabet_auto() -> None:
    """
    Test selecting auto alphabet.

    select_alphabet('auto') should return HPAlphabet (default).
    """
    alphabet = select_alphabet("auto")
    assert isinstance(alphabet, HPAlphabet)


def test_select_alphabet_invalid_raises_error() -> None:
    """
    Test that invalid alphabet name raises ValueError.

    Unsupported alphabet names should raise ValueError.
    """
    with pytest.raises(ValueError, match="Unsupported alphabet"):
        select_alphabet("invalid")


def test_select_alphabet_error_message() -> None:
    """
    Test that error message includes supported options.

    Error message should mention 'hp' and 'auto'.
    """
    with pytest.raises(ValueError) as exc_info:
        select_alphabet("xyz")
    error_msg = str(exc_info.value)
    assert "hp" in error_msg or "auto" in error_msg


def test_infer_alphabet_returns_alphabet() -> None:
    """
    Test that infer_alphabet returns an Alphabet instance.

    infer_alphabet should return an Alphabet (currently HPAlphabet).
    """
    alphabet = infer_alphabet("HPPH")
    assert isinstance(alphabet, HPAlphabet)


def test_infer_alphabet_with_different_sequences() -> None:
    """
    Test infer_alphabet with different sequences.

    Currently all sequences return HPAlphabet (placeholder).
    """
    alphabet1 = infer_alphabet("HPPH")
    alphabet2 = infer_alphabet("ABC")
    # Currently both return HPAlphabet
    assert isinstance(alphabet1, HPAlphabet)
    assert isinstance(alphabet2, HPAlphabet)


def test_infer_alphabet_normalized_sequence() -> None:
    """
    Test that infer_alphabet accepts normalized sequences.

    Function should work with uppercase sequences.
    """
    alphabet = infer_alphabet("HPPH")
    assert alphabet is not None


def test_select_alphabet_case_sensitive() -> None:
    """
    Test that select_alphabet is case sensitive.

    Alphabet names should match exactly.
    """
    with pytest.raises(ValueError):
        select_alphabet("HP")  # Should be lowercase 'hp'

    with pytest.raises(ValueError):
        select_alphabet("AUTO")  # Should be lowercase 'auto'

