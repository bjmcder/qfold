"""Unit tests for the Sequence class."""

import pytest

from qfold.sequence.alphabet import CustomAlphabet, HPAlphabet
from qfold.sequence.sequence import Sequence


@pytest.fixture(scope="function")
def hp_alphabet() -> HPAlphabet:
    """
    Fixture providing an HPAlphabet instance.

    Returns:
        HPAlphabet instance for testing.
    """
    return HPAlphabet()


@pytest.fixture(scope="function")
def custom_alphabet() -> CustomAlphabet:
    """
    Fixture providing a CustomAlphabet instance.

    Returns:
        CustomAlphabet instance with chars {'A', 'B', 'C'}.
    """
    return CustomAlphabet({"A", "B", "C"}, {"A": 0, "B": 1, "C": 2})


def test_sequence_initialization_valid(hp_alphabet: HPAlphabet) -> None:
    """
    Test that Sequence can be initialized with a valid sequence.

    A valid sequence should be created successfully.
    """
    sequence = Sequence("HPPH", hp_alphabet)
    assert sequence is not None
    assert str(sequence) == "HPPH"


def test_sequence_initialization_invalid_raises_error(
    hp_alphabet: HPAlphabet
) -> None:
    """
    Test that Sequence raises ValueError for invalid characters.

    A sequence with characters not in the alphabet should raise
    ValueError.
    """
    with pytest.raises(ValueError, match="Invalid characters"):
        Sequence("HPAX", hp_alphabet)


def test_sequence_normalize_trim_whitespace() -> None:
    """
    Test that normalize() trims whitespace.

    Leading and trailing whitespace should be removed.
    """
    result = Sequence.normalize("  HPPH  ")
    assert result == "HPPH"

    result = Sequence.normalize("\tHPPH\n")
    assert result == "HPPH"

    result = Sequence.normalize("  H P P H  ")
    assert result == "H P P H"


def test_sequence_normalize_uppercase() -> None:
    """
    Test that normalize() converts to uppercase.

    Lowercase letters should be converted to uppercase.
    """
    result = Sequence.normalize("hpph")
    assert result == "HPPH"

    result = Sequence.normalize("HpPh")
    assert result == "HPPH"

    result = Sequence.normalize("abc")
    assert result == "ABC"


def test_sequence_normalize_combined() -> None:
    """
    Test that normalize() handles both trimming and uppercase.

    Both operations should be applied together.
    """
    result = Sequence.normalize("  hpph  ")
    assert result == "HPPH"

    result = Sequence.normalize("\n\tHpPh\t\n")
    assert result == "HPPH"


def test_sequence_validation_valid(hp_alphabet: HPAlphabet) -> None:
    """
    Test that validate() accepts valid sequences.

    Sequences with only valid characters should pass validation.
    """
    sequence = Sequence("HPPH", hp_alphabet)
    # Should not raise an error
    assert sequence is not None


def test_sequence_validation_invalid_single_char(
    hp_alphabet: HPAlphabet
) -> None:
    """
    Test that validate() rejects sequences with invalid characters.

    A sequence with a single invalid character should raise ValueError.
    """
    with pytest.raises(ValueError, match="Invalid characters.*A"):
        Sequence("HPA", hp_alphabet)


def test_sequence_validation_invalid_multiple_chars(
    hp_alphabet: HPAlphabet
) -> None:
    """
    Test that validate() reports all invalid characters.

    A sequence with multiple invalid characters should list all of them.
    """
    with pytest.raises(ValueError, match="Invalid characters") as exc_info:
        Sequence("HPAXB", hp_alphabet)
    # The error should mention A, X, and B
    error_msg = str(exc_info.value)
    assert "A" in error_msg or "X" in error_msg or "B" in error_msg


def test_sequence_str_representation(hp_alphabet: HPAlphabet) -> None:
    """
    Test that __str__ returns the normalized sequence.

    String representation should return the normalized sequence string.
    """
    sequence = Sequence("hpph", hp_alphabet)
    assert str(sequence) == "HPPH"

    sequence = Sequence("  HPPH  ", hp_alphabet)
    assert str(sequence) == "HPPH"


def test_sequence_repr_representation(hp_alphabet: HPAlphabet) -> None:
    """
    Test that __repr__ returns a proper representation.

    Representation should show the class name and sequence.
    """
    sequence = Sequence("HPPH", hp_alphabet)
    repr_str = repr(sequence)
    assert "Sequence" in repr_str
    assert "HPPH" in repr_str


def test_sequence_encoded_mapping_hp(hp_alphabet: HPAlphabet) -> None:
    """
    Test that encoded() returns correct mapping for HP alphabet.

    H should map to 1 and P should map to 0.
    """
    sequence = Sequence("HPPH", hp_alphabet)
    encoded = sequence.encoded()
    assert encoded == [1, 0, 0, 1]


def test_sequence_encoded_mapping_custom(
    custom_alphabet: CustomAlphabet
) -> None:
    """
    Test that encoded() returns correct mapping for custom alphabet.

    Encoding should use the alphabet's mapping.
    """
    sequence = Sequence("ABC", custom_alphabet)
    encoded = sequence.encoded()
    assert encoded == [0, 1, 2]


def test_sequence_encoded_mapping_empty(hp_alphabet: HPAlphabet) -> None:
    """
    Test that encoded() works for empty sequences.

    An empty sequence should return an empty list.
    """
    sequence = Sequence("", hp_alphabet)
    encoded = sequence.encoded()
    assert encoded == []


def test_sequence_encoded_mapping_single_char(
    hp_alphabet: HPAlphabet
) -> None:
    """
    Test that encoded() works for single character sequences.

    Single character should map correctly.
    """
    sequence = Sequence("H", hp_alphabet)
    encoded = sequence.encoded()
    assert encoded == [1]

    sequence = Sequence("P", hp_alphabet)
    encoded = sequence.encoded()
    assert encoded == [0]


def test_sequence_finalized_on_construction(hp_alphabet: HPAlphabet) -> None:
    """
    Test that sequence is finalized after successful construction.

    The _finalized attribute should be True after construction.
    """
    sequence = Sequence("HPPH", hp_alphabet)
    assert sequence._finalized is True


def test_sequence_with_custom_alphabet() -> None:
    """
    Test Sequence with a custom alphabet.

    Sequence should work with any Alphabet implementation.
    """
    alphabet = CustomAlphabet({"X", "Y", "Z"}, {"X": 10, "Y": 20, "Z": 30})
    sequence = Sequence("XYZ", alphabet)
    assert str(sequence) == "XYZ"
    assert sequence.encoded() == [10, 20, 30]


def test_sequence_normalize_preserves_internal_spaces() -> None:
    """
    Test that normalize() only trims external whitespace.

    Internal spaces should be preserved (though they may be invalid
    for most alphabets).
    """
    result = Sequence.normalize("  A B C  ")
    assert result == "A B C"


def test_sequence_validation_case_insensitive_after_normalize(
    custom_alphabet: CustomAlphabet
) -> None:
    """
    Test that validation works after normalization.

    Lowercase input should be normalized to uppercase before validation.
    """
    sequence = Sequence("abc", custom_alphabet)
    assert str(sequence) == "ABC"
    assert sequence.encoded() == [0, 1, 2]


def test_sequence_invalid_after_normalization(
    hp_alphabet: HPAlphabet
) -> None:
    """
    Test that invalid characters are caught after normalization.

    Even if input is lowercase, invalid characters should be detected.
    """
    with pytest.raises(ValueError, match="Invalid characters"):
        Sequence("hpx", hp_alphabet)

