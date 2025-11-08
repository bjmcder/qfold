"""Color mapping utilities for sequence display."""

from typing import Dict, Set

# Color palette for characters
CHAR_COLORS = [
    "bright_red",
    "bright_blue",
    "bright_green",
    "bright_yellow",
    "bright_magenta",
    "bright_cyan",
    "red",
    "blue",
    "green",
    "yellow",
    "magenta",
    "cyan",
]


def get_char_color_map(chars: Set[str]) -> Dict[str, str]:
    """
    Create a color mapping for characters.

    Args:
        chars: Set of unique characters to assign colors to.

    Returns:
        Dictionary mapping characters to color names.
    """
    sorted_chars = sorted(chars)
    color_map = {}
    for idx, char in enumerate(sorted_chars):
        color_map[char] = CHAR_COLORS[idx % len(CHAR_COLORS)]
    return color_map

