"""
Alphabets are used to represent a mapping from the valid values for amino acids
or coarse-grained units in a protein sequence to a set of integers.

This module provides a base class for alphabets and a set of concrete
implementations.
"""

import abc
from typing import Dict, Optional, Set


class Alphabet(abc.ABC):
    """Base class for protein sequence alphabets."""

    @abc.abstractmethod
    def chars(self) -> Set[str]:
        """
        Get the set of valid characters for this alphabet.

        Returns:
            Set of valid characters.
        """
        pass

    @abc.abstractmethod
    def mapping(self) -> Dict[str, int]:
        """
        Get the mapping from characters to unsigned integers.

        Returns:
            Dictionary mapping characters to integers.
        """
        pass


class HPAlphabet(Alphabet):
    """
    Hydrophobic-Polar alphabet for coarse-grained protein models.

    This alphabet is immutable - modifications are not allowed.
    """

    def __init__(self) -> None:
        """Initialize HP alphabet with H (hydrophobic) and P (polar)."""
        self._chars: Set[str] = {"H", "P"}
        self._mapping: Dict[str, int] = {"H": 1, "P": 0}

    def chars(self) -> Set[str]:
        """
        Get the set of valid characters for HP alphabet.

        Returns:
            Copy of set containing 'H' and 'P'.
        """
        return self._chars.copy()

    def mapping(self) -> Dict[str, int]:
        """
        Get the mapping from characters to integers for HP alphabet.

        Returns:
            Copy of dictionary mapping 'H' to 1 and 'P' to 0.
        """
        return self._mapping.copy()


class CustomAlphabet(Alphabet):
    """
    User-defined alphabet with custom character set and mapping.

    This alphabet supports explicit modifications through transaction methods.
    """

    def __init__(
        self, chars: Set[str], mapping: Optional[Dict[str, int]] = None
    ) -> None:
        """
        Initialize a custom alphabet.

        Args:
            chars: Set of valid characters for the alphabet.
            mapping: Optional dictionary mapping characters to integers.
                    If not provided, mapping will be generated automatically
                    in the order characters are provided.

        Raises:
            ValueError: If mapping is provided but doesn't match the
                       character set.
        """
        self._chars = chars.copy()

        if mapping is not None:
            # Validate that mapping covers all characters
            if set(mapping.keys()) != self._chars:
                raise ValueError(
                    "Mapping keys must match the character set exactly."
                )
            self._mapping = mapping.copy()
        else:
            # Generate mapping automatically in order
            sorted_chars = sorted(self._chars)
            self._mapping = {char: idx for idx, char in enumerate(sorted_chars)}

    def chars(self) -> Set[str]:
        """
        Get the set of valid characters for this alphabet.

        Returns:
            Set of valid characters (direct reference - modifications allowed
            through explicit transaction methods).
        """
        return self._chars

    def mapping(self) -> Dict[str, int]:
        """
        Get the mapping from characters to integers.

        Returns:
            Dictionary mapping characters to integers (direct reference -
            modifications allowed through explicit transaction methods).
        """
        return self._mapping

    def add_char(self, char: str, value: Optional[int] = None) -> None:
        """
        Add a character to the alphabet.

        Args:
            char: Character to add.
            value: Optional integer value for the character. If not provided,
                  the next available integer will be used.

        Raises:
            ValueError: If character already exists or value conflicts with
                       existing mapping.
        """
        if char in self._chars:
            raise ValueError(f"Character '{char}' already exists in alphabet.")

        if value is not None:
            if value in self._mapping.values():
                raise ValueError(
                    f"Value {value} is already mapped to another character."
                )
            self._mapping[char] = value
        else:
            # Use next available integer
            max_value = max(self._mapping.values()) if self._mapping else -1
            self._mapping[char] = max_value + 1

        self._chars.add(char)

    def remove_char(self, char: str) -> None:
        """
        Remove a character from the alphabet.

        Args:
            char: Character to remove.

        Raises:
            KeyError: If character does not exist in alphabet.
        """
        if char not in self._chars:
            raise KeyError(f"Character '{char}' not found in alphabet.")

        self._chars.remove(char)
        del self._mapping[char]

    def update_mapping(self, char: str, value: int) -> None:
        """
        Update the integer mapping for an existing character.

        Args:
            char: Character to update.
            value: New integer value for the character.

        Raises:
            KeyError: If character does not exist in alphabet.
            ValueError: If value conflicts with existing mapping.
        """
        if char not in self._chars:
            raise KeyError(f"Character '{char}' not found in alphabet.")

        if value in self._mapping.values() and self._mapping[char] != value:
            raise ValueError(
                f"Value {value} is already mapped to another character."
            )

        self._mapping[char] = value

    def set_mapping(self, mapping: Dict[str, int]) -> None:
        """
        Set the entire mapping dictionary.

        Args:
            mapping: Dictionary mapping characters to integers.

        Raises:
            ValueError: If mapping keys don't match the character set or
                       if values conflict.
        """
        if set(mapping.keys()) != self._chars:
            raise ValueError(
                "Mapping keys must match the character set exactly."
            )

        # Check for duplicate values
        if len(mapping.values()) != len(set(mapping.values())):
            raise ValueError("Mapping contains duplicate values.")

        self._mapping = mapping.copy()
