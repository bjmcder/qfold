"""Sequence processing functions."""

from qfold.io.alphabet import infer_alphabet, select_alphabet
from qfold.sequence.sequence import Sequence


def process_sequence(sequence: str, alphabet_name: str) -> Sequence:
    """
    Process a sequence string with the specified alphabet.

    Args:
        sequence: Input sequence string.
        alphabet_name: Name of the alphabet ('hp' or 'auto').

    Returns:
        Sequence object.

    Raises:
        ValueError: If alphabet name is not supported or sequence is invalid.
    """
    # Get alphabet instance
    if alphabet_name == "auto":
        # Normalize sequence first for inference
        normalized = Sequence.normalize(sequence)
        alphabet_obj = infer_alphabet(normalized)
    else:
        alphabet_obj = select_alphabet(alphabet_name)

    # Construct Sequence object
    return Sequence(sequence, alphabet_obj)

