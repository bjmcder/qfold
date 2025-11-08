"""Unit tests for the CustomAlphabet class."""


import pytest

from qfold.sequence.alphabet import CustomAlphabet


@pytest.fixture(scope="function")
def custom_alphabet() -> CustomAlphabet:
    """
    Fixture providing a CustomAlphabet instance.

    Returns:
        CustomAlphabet instance with chars {'A', 'B', 'C'} and
        mapping {'A': 0, 'B': 1, 'C': 2}.
    """
    return CustomAlphabet({"A", "B", "C"}, {"A": 0, "B": 1, "C": 2})


def test_custom_alphabet_initialization_with_mapping() -> None:
    """
    Test that CustomAlphabet can be initialized with a mapping.

    When a mapping is provided, it should be used as-is.
    """
    alphabet = CustomAlphabet({"X", "Y"}, {"X": 10, "Y": 20})
    assert alphabet.chars() == {"X", "Y"}
    assert alphabet.mapping() == {"X": 10, "Y": 20}


def test_custom_alphabet_initialization_without_mapping() -> None:
    """
    Test that CustomAlphabet auto-generates mapping when not provided.

    When no mapping is provided, it should be generated in sorted order.
    """
    alphabet = CustomAlphabet({"Z", "A", "M"})
    chars = alphabet.chars()
    mapping = alphabet.mapping()

    assert chars == {"Z", "A", "M"}
    # Mapping should be in sorted order: A=0, M=1, Z=2
    assert mapping == {"A": 0, "M": 1, "Z": 2}


def test_custom_alphabet_initialization_mapping_mismatch() -> None:
    """
    Test that initialization raises ValueError when mapping doesn't match.

    If mapping keys don't match the character set, ValueError should
    be raised.
    """
    with pytest.raises(ValueError, match="Mapping keys must match"):
        CustomAlphabet({"A", "B"}, {"A": 0, "B": 1, "C": 2})


def test_custom_alphabet_initialization_duplicate_values() -> None:
    """
    Test that initialization raises ValueError for duplicate values.

    If mapping contains duplicate integer values, ValueError should
    be raised.
    """
    with pytest.raises(ValueError, match="duplicate values"):
        CustomAlphabet({"A", "B", "C"}, {"A": 0, "B": 0, "C": 1})


def test_custom_alphabet_chars_returns_reference(
    custom_alphabet: CustomAlphabet
) -> None:
    """
    Test that chars() returns a direct reference.

    Modifications to the returned set should affect the alphabet.
    """
    chars = custom_alphabet.chars()
    chars.add("D")
    # Alphabet should be modified
    assert "D" in custom_alphabet.chars()


def test_custom_alphabet_mapping_returns_reference(
    custom_alphabet: CustomAlphabet
) -> None:
    """
    Test that mapping() returns a direct reference.

    Modifications to the returned dict should affect the alphabet.
    """
    mapping = custom_alphabet.mapping()
    mapping["D"] = 99
    # Alphabet should be modified
    assert "D" in custom_alphabet.mapping()


def test_custom_alphabet_add_char_with_value(
    custom_alphabet: CustomAlphabet
) -> None:
    """
    Test adding a character with a specific value.

    add_char() should add the character with the specified value.
    """
    custom_alphabet.add_char("D", 5)
    assert "D" in custom_alphabet.chars()
    assert custom_alphabet.mapping()["D"] == 5


def test_custom_alphabet_add_char_without_value(
    custom_alphabet: CustomAlphabet
) -> None:
    """
    Test adding a character without specifying a value.

    add_char() should auto-assign the next available integer.
    """
    custom_alphabet.add_char("D")
    assert "D" in custom_alphabet.chars()
    # Max value is 2, so D should be 3
    assert custom_alphabet.mapping()["D"] == 3


def test_custom_alphabet_add_char_auto_increment_empty() -> None:
    """
    Test auto-increment when adding to empty alphabet.

    First character should get value 0.
    """
    alphabet = CustomAlphabet(set())
    alphabet.add_char("A")
    assert alphabet.mapping()["A"] == 0


def test_custom_alphabet_add_char_duplicate_raises_error(
    custom_alphabet: CustomAlphabet
) -> None:
    """
    Test that adding a duplicate character raises ValueError.

    Attempting to add a character that already exists should fail.
    """
    with pytest.raises(ValueError, match="already exists"):
        custom_alphabet.add_char("A")


def test_custom_alphabet_add_char_duplicate_value_raises_error(
    custom_alphabet: CustomAlphabet
) -> None:
    """
    Test that adding a character with duplicate value raises ValueError.

    Attempting to use a value already mapped to another character
    should fail.
    """
    with pytest.raises(ValueError, match="already mapped"):
        custom_alphabet.add_char("D", 1)


def test_custom_alphabet_remove_char(
    custom_alphabet: CustomAlphabet
) -> None:
    """
    Test removing a character from the alphabet.

    remove_char() should remove both the character and its mapping.
    """
    custom_alphabet.remove_char("B")
    assert "B" not in custom_alphabet.chars()
    assert "B" not in custom_alphabet.mapping()


def test_custom_alphabet_remove_char_not_found_raises_error(
    custom_alphabet: CustomAlphabet
) -> None:
    """
    Test that removing a non-existent character raises KeyError.

    Attempting to remove a character not in the alphabet should fail.
    """
    with pytest.raises(KeyError, match="not found"):
        custom_alphabet.remove_char("Z")


def test_custom_alphabet_update_mapping(
    custom_alphabet: CustomAlphabet
) -> None:
    """
    Test updating the mapping for an existing character.

    update_mapping() should change the value for the character.
    """
    custom_alphabet.update_mapping("A", 99)
    assert custom_alphabet.mapping()["A"] == 99


def test_custom_alphabet_update_mapping_same_value(
    custom_alphabet: CustomAlphabet
) -> None:
    """
    Test updating mapping to the same value.

    Updating to the current value should be allowed.
    """
    original_value = custom_alphabet.mapping()["A"]
    custom_alphabet.update_mapping("A", original_value)
    assert custom_alphabet.mapping()["A"] == original_value


def test_custom_alphabet_update_mapping_char_not_found_raises_error(
    custom_alphabet: CustomAlphabet
) -> None:
    """
    Test that updating mapping for non-existent char raises KeyError.

    Attempting to update a character not in the alphabet should fail.
    """
    with pytest.raises(KeyError, match="not found"):
        custom_alphabet.update_mapping("Z", 5)


def test_custom_alphabet_update_mapping_duplicate_value_raises_error(
    custom_alphabet: CustomAlphabet
) -> None:
    """
    Test that updating to a duplicate value raises ValueError.

    Attempting to use a value already mapped to another character
    should fail.
    """
    with pytest.raises(ValueError, match="already mapped"):
        custom_alphabet.update_mapping("A", 1)


def test_custom_alphabet_set_mapping(
    custom_alphabet: CustomAlphabet
) -> None:
    """
    Test setting the entire mapping dictionary.

    set_mapping() should replace the entire mapping.
    """
    new_mapping = {"A": 10, "B": 20, "C": 30}
    custom_alphabet.set_mapping(new_mapping)
    assert custom_alphabet.mapping() == new_mapping


def test_custom_alphabet_set_mapping_keys_mismatch_raises_error(
    custom_alphabet: CustomAlphabet
) -> None:
    """
    Test that set_mapping with mismatched keys raises ValueError.

    If mapping keys don't match the character set, ValueError should
    be raised.
    """
    with pytest.raises(ValueError, match="must match the character set"):
        custom_alphabet.set_mapping({"A": 0, "B": 1, "D": 2})


def test_custom_alphabet_set_mapping_duplicate_values_raises_error(
    custom_alphabet: CustomAlphabet
) -> None:
    """
    Test that set_mapping with duplicate values raises ValueError.

    If mapping contains duplicate values, ValueError should be raised.
    """
    with pytest.raises(ValueError, match="duplicate values"):
        custom_alphabet.set_mapping({"A": 0, "B": 0, "C": 1})


def test_custom_alphabet_transaction_sequence(
    custom_alphabet: CustomAlphabet
) -> None:
    """
    Test a sequence of transactions on a custom alphabet.

    Multiple operations should work correctly in sequence.
    """
    # Add a character
    custom_alphabet.add_char("D", 5)
    assert "D" in custom_alphabet.chars()

    # Update a mapping
    custom_alphabet.update_mapping("B", 10)
    assert custom_alphabet.mapping()["B"] == 10

    # Remove a character
    custom_alphabet.remove_char("A")
    assert "A" not in custom_alphabet.chars()

    # Set new mapping
    custom_alphabet.set_mapping({"B": 1, "C": 2, "D": 3})
    assert custom_alphabet.mapping() == {"B": 1, "C": 2, "D": 3}


def test_custom_alphabet_empty_initialization() -> None:
    """
    Test initializing CustomAlphabet with empty character set.

    Empty alphabet should be valid and allow adding characters.
    """
    alphabet = CustomAlphabet(set())
    assert alphabet.chars() == set()
    assert alphabet.mapping() == {}

    alphabet.add_char("A")
    assert alphabet.chars() == {"A"}
    assert alphabet.mapping() == {"A": 0}


def test_custom_alphabet_single_character() -> None:
    """
    Test CustomAlphabet with a single character.

    Single character alphabet should work correctly.
    """
    alphabet = CustomAlphabet({"X"}, {"X": 42})
    assert alphabet.chars() == {"X"}
    assert alphabet.mapping() == {"X": 42}


def test_custom_alphabet_auto_mapping_preserves_order() -> None:
    """
    Test that auto-generated mapping uses sorted order.

    Characters should be mapped in alphabetical order.
    """
    alphabet = CustomAlphabet({"Z", "A", "M", "B"})
    mapping = alphabet.mapping()
    # Should be sorted: A=0, B=1, M=2, Z=3
    assert mapping["A"] == 0
    assert mapping["B"] == 1
    assert mapping["M"] == 2
    assert mapping["Z"] == 3

