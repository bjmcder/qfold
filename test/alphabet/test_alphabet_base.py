"""Unit tests for the Alphabet base class."""

from typing import Callable, Dict, Set

import pytest

from qfold.sequence.alphabet import Alphabet


class CompleteAlphabet(Alphabet):
    """Complete alphabet implementation for testing."""

    def __init__(self, chars: Set[str], mapping: Dict[str, int]) -> None:
        """Initialize test alphabet."""
        self._chars = chars
        self._mapping = mapping

    def chars(self) -> Set[str]:
        """Return character set."""
        return self._chars

    def mapping(self) -> Dict[str, int]:
        """Return character to integer mapping."""
        return self._mapping


@pytest.fixture(scope="function")
def alphabet_factory() -> Callable[[Set[str], Dict[str, int]], Alphabet]:
    """
    Fixture providing a factory function for creating complete alphabets.

    Returns:
        Factory function that creates CompleteAlphabet instances.
    """
    def _factory(chars: Set[str], mapping: Dict[str, int]) -> Alphabet:
        return CompleteAlphabet(chars, mapping)

    return _factory


def test_alphabet_is_abstract() -> None:
    """
    Test that Alphabet cannot be instantiated directly.

    Since Alphabet is an abstract base class, attempting to
    instantiate it should raise a TypeError.
    """
    with pytest.raises(TypeError):
        Alphabet()  # type: ignore


def test_concrete_alphabet_must_implement_chars() -> None:
    """
    Test that concrete classes must implement chars() method.

    A class that inherits from Alphabet but doesn't implement
    chars() should raise TypeError when instantiated.
    """

    class IncompleteAlphabet(Alphabet):
        """Alphabet missing chars() implementation."""

        def mapping(self) -> Dict[str, int]:
            """Implement mapping but not chars."""
            return {"A": 0}

    with pytest.raises(TypeError):
        IncompleteAlphabet()


def test_concrete_alphabet_must_implement_mapping() -> None:
    """
    Test that concrete classes must implement mapping() method.

    A class that inherits from Alphabet but doesn't implement
    mapping() should raise TypeError when instantiated.
    """

    class IncompleteAlphabet(Alphabet):
        """Alphabet missing mapping() implementation."""

        def chars(self) -> Set[str]:
            """Implement chars but not mapping."""
            return {"A"}

    with pytest.raises(TypeError):
        IncompleteAlphabet()


def test_complete_concrete_alphabet_can_be_instantiated(
    alphabet_factory: Callable[[Set[str], Dict[str, int]], Alphabet]
) -> None:
    """
    Test that a complete concrete implementation can be instantiated.

    A class that implements both chars() and mapping() should
    be instantiable.
    """
    alphabet = alphabet_factory({"A", "B"}, {"A": 0, "B": 1})
    assert alphabet is not None
    assert isinstance(alphabet, Alphabet)


def test_concrete_alphabet_returns_chars(
    alphabet_factory: Callable[[Set[str], Dict[str, int]], Alphabet]
) -> None:
    """
    Test that concrete alphabet returns characters via chars().

    A complete implementation should return the expected
    character set.
    """
    alphabet = alphabet_factory({"X", "Y", "Z"}, {"X": 0, "Y": 1, "Z": 2})
    chars = alphabet.chars()
    assert chars == {"X", "Y", "Z"}
    assert isinstance(chars, set)


def test_concrete_alphabet_returns_mapping(
    alphabet_factory: Callable[[Set[str], Dict[str, int]], Alphabet]
) -> None:
    """
    Test that concrete alphabet returns mapping via mapping().

    A complete implementation should return the expected
    character to integer mapping.
    """
    alphabet = alphabet_factory({"A", "B"}, {"A": 5, "B": 10})
    mapping = alphabet.mapping()
    assert mapping == {"A": 5, "B": 10}
    assert isinstance(mapping, dict)
    assert all(isinstance(v, int) for v in mapping.values())

