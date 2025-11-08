"""Sequence class for protein sequences."""

from typing import List

from qfold.sequence.alphabet import Alphabet


class Sequence:
    """Represents a protein sequence validated against an alphabet."""

    def __init__(self, sequence: str, alphabet: Alphabet) -> None:
        """
        Initialize a sequence from a string and alphabet.

        Args:
            sequence: Input sequence string.
            alphabet: Alphabet object to validate against.

        Raises:
            ValueError: If sequence contains invalid characters for the
                       alphabet.
        """
        self._alphabet = alphabet
        self._normalized = self.normalize(sequence)
        self.validate(self._normalized)
        self._finalized = True

    @staticmethod
    def normalize(sequence: str) -> str:
        """
        Normalize a sequence string.

        Trims whitespace and converts to uppercase.

        Args:
            sequence: Input sequence string.

        Returns:
            Normalized sequence string.
        """
        return sequence.strip().upper()

    def validate(self, sequence: str) -> None:
        """
        Validate a sequence against the alphabet.

        Args:
            sequence: Sequence string to validate.

        Raises:
            ValueError: If sequence contains characters not in the alphabet.
        """
        valid_chars = self._alphabet.chars()
        invalid_chars = set()

        for char in sequence:
            if char not in valid_chars:
                invalid_chars.add(char)

        if invalid_chars:
            alphabet_name = getattr(self._alphabet, "name", "alphabet")
            raise ValueError(
                f"Invalid characters for {alphabet_name} alphabet: "
                f"{sorted(invalid_chars)}"
            )

    def __str__(self) -> str:
        """
        Return string representation of the sequence.

        Returns:
            Normalized sequence string.
        """
        return self._normalized

    def __repr__(self) -> str:
        """
        Return representation of the sequence.

        Returns:
            String representation showing class and sequence.
        """
        return f"Sequence('{self._normalized}')"

    def encoded(self) -> List[int]:
        """
        Return the encoded mapping of the sequence.

        Returns:
            List of integers representing the sequence according to the
            alphabet mapping.
        """
        mapping = self._alphabet.mapping()
        return [mapping[char] for char in self._normalized]

