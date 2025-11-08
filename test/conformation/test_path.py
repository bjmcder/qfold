"""Unit tests for the Path class."""

import pytest

from qfold.conformation.path import Path


@pytest.fixture(scope="function")
def simple_path() -> Path:
    """
    Fixture providing a Path instance with simple moves.

    Returns:
        Path instance with moves [0, 1, 2, 3] for testing.
    """
    return Path(moves=[0, 1, 2, 3])


@pytest.fixture(scope="function")
def empty_path() -> Path:
    """
    Fixture providing a Path instance with no moves.

    Returns:
        Path instance with empty moves list for testing.
    """
    return Path(moves=[])


def test_path_initialization_valid() -> None:
    """
    Test that Path can be initialized with valid moves.

    A path with valid integer moves should be created successfully.
    """
    path = Path(moves=[0, 1, 2, 3])
    assert path is not None
    assert path.moves == [0, 1, 2, 3]


def test_path_initialization_empty() -> None:
    """
    Test that Path can be initialized with empty moves list.

    An empty path should be valid.
    """
    path = Path(moves=[])
    assert path is not None
    assert path.moves == []
    assert len(path.moves) == 0


def test_path_initialization_single_move() -> None:
    """
    Test that Path can be initialized with a single move.

    A path with one move should be valid.
    """
    path = Path(moves=[0])
    assert path is not None
    assert path.moves == [0]
    assert len(path.moves) == 1


def test_path_initialization_repeated_moves() -> None:
    """
    Test that Path can handle repeated moves.

    A path with repeated move indices should be valid.
    """
    path = Path(moves=[0, 0, 1, 1, 2, 2])
    assert path is not None
    assert path.moves == [0, 0, 1, 1, 2, 2]


def test_path_initialization_large_indices() -> None:
    """
    Test that Path can handle large move indices.

    Large positive integers should be valid move indices.
    """
    path = Path(moves=[0, 5, 10, 100])
    assert path is not None
    assert path.moves == [0, 5, 10, 100]


def test_path_initialization_non_list_raises_type_error() -> None:
    """
    Test that Path raises TypeError for non-list input.

    A path with non-list moves should raise TypeError.
    """
    with pytest.raises(TypeError, match="moves must be a list"):
        Path(moves=(0, 1, 2))  # type: ignore

    with pytest.raises(TypeError, match="moves must be a list"):
        Path(moves="012")  # type: ignore

    with pytest.raises(TypeError, match="moves must be a list"):
        Path(moves={0, 1, 2})  # type: ignore


def test_path_initialization_non_integer_raises_type_error() -> None:
    """
    Test that Path raises TypeError for non-integer moves.

    A path with non-integer moves should raise TypeError.
    """
    with pytest.raises(TypeError, match="All moves must be integers"):
        Path(moves=[0, 1.5, 2])  # type: ignore

    with pytest.raises(TypeError, match="All moves must be integers"):
        Path(moves=[0, "1", 2])  # type: ignore

    with pytest.raises(TypeError, match="All moves must be integers"):
        Path(moves=[0, [1], 2])  # type: ignore


def test_path_initialization_negative_index_raises_value_error() -> None:
    """
    Test that Path raises ValueError for negative move indices.

    A path with negative move indices should raise ValueError.
    """
    with pytest.raises(ValueError, match="Move indices must be non-negative"):
        Path(moves=[0, -1, 2])

    with pytest.raises(ValueError, match="Move indices must be non-negative"):
        Path(moves=[-1])

    with pytest.raises(ValueError, match="Move indices must be non-negative"):
        Path(moves=[0, 1, -5, 2])


def test_path_equality_same_moves() -> None:
    """
    Test that Path instances with same moves are equal.

    Two paths with identical moves should be equal.
    """
    path1 = Path(moves=[0, 1, 2, 3])
    path2 = Path(moves=[0, 1, 2, 3])
    assert path1 == path2


def test_path_equality_different_moves() -> None:
    """
    Test that Path instances with different moves are not equal.

    Two paths with different moves should not be equal.
    """
    path1 = Path(moves=[0, 1, 2, 3])
    path2 = Path(moves=[0, 1, 2])
    assert path1 != path2

    path3 = Path(moves=[1, 2, 3, 4])
    assert path1 != path3


def test_path_equality_empty_paths() -> None:
    """
    Test that empty Path instances are equal.

    Two empty paths should be equal.
    """
    path1 = Path(moves=[])
    path2 = Path(moves=[])
    assert path1 == path2


def test_path_repr_contains_moves() -> None:
    """
    Test that Path __repr__ contains moves information.

    The string representation should include the moves.
    """
    path = Path(moves=[0, 1, 2, 3])
    repr_str = repr(path)
    assert "Path" in repr_str
    assert "moves" in repr_str or "[0, 1, 2, 3]" in repr_str


def test_path_moves_attribute_mutable() -> None:
    """
    Test that Path moves attribute can be modified.

    The moves list should be mutable after initialization.
    """
    path = Path(moves=[0, 1, 2])
    assert path.moves == [0, 1, 2]

    # Modify the moves list
    path.moves.append(3)
    assert path.moves == [0, 1, 2, 3]

    path.moves[0] = 5
    assert path.moves == [5, 1, 2, 3]


def test_path_moves_attribute_replacement() -> None:
    """
    Test that Path moves attribute can be replaced.

    Replacing moves with valid list should work.
    """
    path = Path(moves=[0, 1, 2])
    path.moves = [3, 4, 5]
    assert path.moves == [3, 4, 5]


def test_path_moves_attribute_replacement_invalid() -> None:
    """
    Test that replacing moves with invalid data is not prevented.

    Note: __post_init__ only runs during initialization, so
    replacing moves with invalid data after initialization won't
    raise an error. This documents the current behavior.
    """
    path = Path(moves=[0, 1, 2])
    # This won't raise an error because __post_init__ only runs once
    path.moves = [0, -1, 2]  # type: ignore
    # The invalid data is stored, but this is expected behavior
    assert path.moves == [0, -1, 2]


def test_path_square_lattice_moves() -> None:
    """
    Test Path with moves valid for square lattice.

    Square lattice has 4 neighbors (indices 0-3).
    """
    path = Path(moves=[0, 1, 2, 3, 0])
    assert path.moves == [0, 1, 2, 3, 0]


def test_path_triangular_lattice_moves() -> None:
    """
    Test Path with moves valid for triangular lattice.

    Triangular lattice has 6 neighbors (indices 0-5).
    """
    path = Path(moves=[0, 1, 2, 3, 4, 5])
    assert path.moves == [0, 1, 2, 3, 4, 5]


def test_path_hexagonal_lattice_moves() -> None:
    """
    Test Path with moves valid for hexagonal lattice.

    Hexagonal lattice has 3 neighbors (indices 0-2).
    """
    path = Path(moves=[0, 1, 2, 0, 1, 2])
    assert path.moves == [0, 1, 2, 0, 1, 2]


def test_path_long_sequence() -> None:
    """
    Test Path with a long sequence of moves.

    A path with many moves should work correctly.
    """
    moves = [0, 1, 2, 3] * 10
    path = Path(moves=moves)
    assert path.moves == moves
    assert len(path.moves) == 40


def test_path_zero_index() -> None:
    """
    Test that Path accepts zero as a valid move index.

    Zero should be a valid move index.
    """
    path = Path(moves=[0, 0, 0])
    assert path.moves == [0, 0, 0]


def test_path_mixed_valid_indices() -> None:
    """
    Test Path with mixed valid move indices.

    A path with various valid indices should work.
    """
    path = Path(moves=[0, 1, 0, 2, 1, 3, 0])
    assert path.moves == [0, 1, 0, 2, 1, 3, 0]

