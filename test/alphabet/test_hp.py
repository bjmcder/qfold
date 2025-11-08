"""Unit tests for the HPAlphabet class."""

import pytest
from typing import Dict, Set

from qfold.sequence.alphabet import HPAlphabet


@pytest.fixture(scope="function")
def hp_alphabet() -> HPAlphabet:
    """
    Fixture providing an HPAlphabet instance.

    Returns:
        HPAlphabet instance for testing.
    """
    return HPAlphabet()


def test_hp_alphabet_initialization() -> None:
    """
    Test that HPAlphabet can be instantiated.

    HPAlphabet should be instantiable without arguments.
    """
    alphabet = HPAlphabet()
    assert alphabet is not None
    assert isinstance(alphabet, HPAlphabet)


def test_hp_alphabet_chars(hp_alphabet: HPAlphabet) -> None:
    """
    Test that chars() returns the correct character set.

    HP alphabet should contain exactly 'H' and 'P'.
    """
    chars = hp_alphabet.chars()
    assert chars == {"H", "P"}
    assert isinstance(chars, set)
    assert len(chars) == 2


def test_hp_alphabet_chars_returns_copy(hp_alphabet: HPAlphabet) -> None:
    """
    Test that chars() returns a copy, preventing modification.

    Modifying the returned set should not affect the alphabet.
    """
    chars = hp_alphabet.chars()
    chars.add("X")
    # Original alphabet should be unchanged
    assert hp_alphabet.chars() == {"H", "P"}


def test_hp_alphabet_mapping(hp_alphabet: HPAlphabet) -> None:
    """
    Test that mapping() returns the correct character mapping.

    H should map to 1 and P should map to 0.
    """
    mapping = hp_alphabet.mapping()
    assert mapping == {"H": 1, "P": 0}
    assert isinstance(mapping, dict)
    assert mapping["H"] == 1
    assert mapping["P"] == 0


def test_hp_alphabet_mapping_returns_copy(hp_alphabet: HPAlphabet) -> None:
    """
    Test that mapping() returns a copy, preventing modification.

    Modifying the returned dictionary should not affect the alphabet.
    """
    mapping = hp_alphabet.mapping()
    mapping["X"] = 99
    # Original alphabet should be unchanged
    assert hp_alphabet.mapping() == {"H": 1, "P": 0}


def test_hp_alphabet_mapping_values_are_integers(
    hp_alphabet: HPAlphabet
) -> None:
    """
    Test that mapping values are integers.

    All values in the mapping should be of type int.
    """
    mapping = hp_alphabet.mapping()
    assert all(isinstance(v, int) for v in mapping.values())


def test_hp_alphabet_immutability(hp_alphabet: HPAlphabet) -> None:
    """
    Test that HPAlphabet is immutable.

    Multiple calls to chars() and mapping() should return
    consistent results.
    """
    chars1 = hp_alphabet.chars()
    chars2 = hp_alphabet.chars()
    mapping1 = hp_alphabet.mapping()
    mapping2 = hp_alphabet.mapping()

    assert chars1 == chars2
    assert mapping1 == mapping2


def test_hp_alphabet_multiple_instances() -> None:
    """
    Test that multiple HPAlphabet instances are independent.

    Each instance should have its own internal state.
    """
    alphabet1 = HPAlphabet()
    alphabet2 = HPAlphabet()

    chars1 = alphabet1.chars()
    chars2 = alphabet2.chars()

    # Modify one copy
    chars1.add("X")

    # Other instance should be unaffected
    assert alphabet2.chars() == {"H", "P"}
    # First instance should also be unaffected (copy was modified)
    assert alphabet1.chars() == {"H", "P"}


def test_hp_alphabet_contains_h_and_p(hp_alphabet: HPAlphabet) -> None:
    """
    Test that HP alphabet contains exactly H and P characters.

    The character set should contain 'H' and 'P' and no others.
    """
    chars = hp_alphabet.chars()
    assert "H" in chars
    assert "P" in chars
    assert "A" not in chars
    assert "X" not in chars


def test_hp_alphabet_mapping_completeness(hp_alphabet: HPAlphabet) -> None:
    """
    Test that mapping covers all characters in the alphabet.

    Every character in chars() should have a corresponding
    entry in mapping().
    """
    chars = hp_alphabet.chars()
    mapping = hp_alphabet.mapping()

    assert set(mapping.keys()) == chars
    assert len(mapping) == len(chars)

