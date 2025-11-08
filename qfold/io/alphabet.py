"""Alphabet selection and inference functions."""

from qfold.sequence.alphabet import Alphabet, HPAlphabet


def infer_alphabet(sequence: str) -> Alphabet:
    """
    Infer the alphabet from a sequence string.

    Args:
        sequence: Normalized sequence string.

    Returns:
        Alphabet instance inferred from the sequence.

    Note:
        Currently defaults to HPAlphabet. Full implementation to be added.
    """
    # TODO: Implement alphabet inference logic
    return HPAlphabet()


def select_alphabet(alphabet_name: str) -> Alphabet:
    """
    Get an alphabet instance by name.

    Args:
        alphabet_name: Name of the alphabet ('hp' or 'auto').

    Returns:
        Alphabet instance.

    Raises:
        ValueError: If alphabet name is not supported.
    """
    if alphabet_name == "hp":
        return HPAlphabet()
    elif alphabet_name == "auto":
        # For auto, we'll use HP as default for now
        # This can be extended to auto-detect in the future
        return HPAlphabet()
    else:
        raise ValueError(
            f"Unsupported alphabet: {alphabet_name}. "
            f"Supported: 'hp', 'auto'"
        )

