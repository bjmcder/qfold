"""Unit tests for color mapping utilities."""

from qfold.app.display.colors import CHAR_COLORS, get_char_color_map


def test_char_colors_is_list() -> None:
    """
    Test that CHAR_COLORS is a list.

    CHAR_COLORS should be a list of color names.
    """
    assert isinstance(CHAR_COLORS, list)
    assert len(CHAR_COLORS) > 0


def test_char_colors_contains_strings() -> None:
    """
    Test that CHAR_COLORS contains string values.

    All elements should be strings representing color names.
    """
    assert all(isinstance(color, str) for color in CHAR_COLORS)


def test_get_char_color_map_single_char() -> None:
    """
    Test color mapping for a single character.

    Single character should get first color.
    """
    color_map = get_char_color_map({"A"})
    assert color_map == {"A": CHAR_COLORS[0]}


def test_get_char_color_map_multiple_chars() -> None:
    """
    Test color mapping for multiple characters.

    Each character should get a different color.
    """
    color_map = get_char_color_map({"A", "B", "C"})
    assert len(color_map) == 3
    assert color_map["A"] == CHAR_COLORS[0]
    assert color_map["B"] == CHAR_COLORS[1]
    assert color_map["C"] == CHAR_COLORS[2]


def test_get_char_color_map_sorted_order() -> None:
    """
    Test that color mapping uses sorted character order.

    Characters should be assigned colors in sorted order.
    """
    color_map = get_char_color_map({"Z", "A", "M"})
    # Should be sorted: A, M, Z
    assert color_map["A"] == CHAR_COLORS[0]
    assert color_map["M"] == CHAR_COLORS[1]
    assert color_map["Z"] == CHAR_COLORS[2]


def test_get_char_color_map_wraps_around() -> None:
    """
    Test that color mapping wraps around for many characters.

    When there are more characters than colors, it should cycle.
    """
    many_chars = {chr(ord("A") + i) for i in range(len(CHAR_COLORS) + 5)}
    color_map = get_char_color_map(many_chars)

    # First character should get first color
    sorted_chars = sorted(many_chars)
    assert color_map[sorted_chars[0]] == CHAR_COLORS[0]
    # Character at index len(CHAR_COLORS) should wrap
    assert color_map[sorted_chars[len(CHAR_COLORS)]] == CHAR_COLORS[0]


def test_get_char_color_map_consistent() -> None:
    """
    Test that color mapping is consistent across calls.

    Same character set should always get same colors.
    """
    chars = {"H", "P"}
    color_map1 = get_char_color_map(chars)
    color_map2 = get_char_color_map(chars)
    assert color_map1 == color_map2


def test_get_char_color_map_empty_set() -> None:
    """
    Test color mapping for empty character set.

    Empty set should return empty dictionary.
    """
    color_map = get_char_color_map(set())
    assert color_map == {}


def test_get_char_color_map_all_unique_colors() -> None:
    """
    Test that all characters get unique colors when possible.

    When there are fewer characters than colors, each should be unique.
    """
    chars = {chr(ord("A") + i) for i in range(len(CHAR_COLORS))}
    color_map = get_char_color_map(chars)
    # All colors should be unique
    assert len(set(color_map.values())) == len(chars)

