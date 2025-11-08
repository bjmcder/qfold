"""Rendering functions for displaying sequences."""

from rich.console import Console
from rich.text import Text

from qfold.app.display.colors import get_char_color_map
from qfold.sequence.sequence import Sequence

console = Console()


def display_sequence(seq_obj: Sequence) -> None:
    """
    Display a sequence with colored characters and mapping.

    Args:
        seq_obj: Sequence object to display.
    """
    # Get color mapping for characters
    unique_chars = set(str(seq_obj))
    char_colors = get_char_color_map(unique_chars)

    # Display colored sequence
    seq_text = Text("Sequence: ", style="bold")
    for char in str(seq_obj):
        seq_text.append(char, style=char_colors[char])
    console.print(seq_text)

    # Display colored mapping
    mapping = seq_obj.encoded()
    seq_str = str(seq_obj)
    # Create mapping from position to character for coloring
    mapping_text = Text("Mapping:  [", style="bold")
    for idx, value in enumerate(mapping):
        if idx > 0:
            mapping_text.append(", ", style="default")
        # Use character at same position for color
        char = seq_str[idx]
        mapping_text.append(str(value), style=char_colors[char])
    mapping_text.append("]", style="bold")
    console.print(mapping_text)

