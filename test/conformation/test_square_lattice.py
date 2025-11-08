"""Unit tests for the SquareLattice class."""

import numpy as np
import pytest

from qfold.conformation.lattice import Lattice, SquareLattice


@pytest.fixture(scope="function")
def square_lattice() -> SquareLattice:
    """
    Fixture providing a SquareLattice instance with default parameters.

    Returns:
        SquareLattice instance for testing.
    """
    return SquareLattice()


@pytest.fixture(scope="function")
def square_lattice_custom() -> SquareLattice:
    """
    Fixture providing a SquareLattice instance with custom lattice constant.

    Returns:
        SquareLattice instance with a=2.0 for testing.
    """
    return SquareLattice(a=2.0)


def test_square_lattice_initialization_default(
    square_lattice: SquareLattice
) -> None:
    """
    Test that SquareLattice can be initialized with default parameters.

    Default lattice constant should be 1.0.
    """
    assert square_lattice is not None
    assert isinstance(square_lattice, Lattice)
    assert isinstance(square_lattice, SquareLattice)
    assert square_lattice.dimension == 2


def test_square_lattice_initialization_custom(
    square_lattice_custom: SquareLattice
) -> None:
    """
    Test that SquareLattice can be initialized with custom lattice constant.

    Custom lattice constant should be stored and used in basis vectors.
    """
    assert square_lattice_custom is not None
    assert square_lattice_custom.dimension == 2
    expected_vectors = np.array([[2.0, 0.0], [0.0, 2.0]], dtype=float)
    assert np.array_equal(
        square_lattice_custom.basis_vectors, expected_vectors
    )


def test_square_lattice_basis_vectors_default(
    square_lattice: SquareLattice
) -> None:
    """
    Test that SquareLattice has correct basis vectors with default a.

    Default basis vectors should be [[1.0, 0.0], [0.0, 1.0]].
    """
    expected_vectors = np.array([[1.0, 0.0], [0.0, 1.0]], dtype=float)
    assert np.array_equal(square_lattice.basis_vectors, expected_vectors)


def test_square_lattice_index_to_basis_returns_dict(
    square_lattice: SquareLattice
) -> None:
    """
    Test that index_to_basis() returns a dictionary.

    The return value should be a dictionary mapping int to np.ndarray.
    """
    mapping = square_lattice.index_to_basis()
    assert isinstance(mapping, dict)
    assert all(isinstance(k, int) for k in mapping.keys())
    assert all(isinstance(v, np.ndarray) for v in mapping.values())


def test_square_lattice_index_to_basis_canonical_order(
    square_lattice: SquareLattice
) -> None:
    """
    Test that index_to_basis() returns canonical indexing.

    Canonical indexing should start at theta=0 ([1, 0]) and proceed
    counterclockwise: [1, 0] -> 0, [0, 1] -> 1, [-1, 0] -> 2,
    [0, -1] -> 3.
    """
    mapping = square_lattice.index_to_basis()
    assert len(mapping) == 4

    # Index 0: [1, 0] (right, theta=0)
    assert np.array_equal(mapping[0], np.array([1.0, 0.0], dtype=float))

    # Index 1: [0, 1] (up, counterclockwise from 0)
    assert np.array_equal(mapping[1], np.array([0.0, 1.0], dtype=float))

    # Index 2: [-1, 0] (left, counterclockwise from 1)
    assert np.array_equal(mapping[2], np.array([-1.0, 0.0], dtype=float))

    # Index 3: [0, -1] (down, counterclockwise from 2)
    assert np.array_equal(mapping[3], np.array([0.0, -1.0], dtype=float))


def test_square_lattice_index_to_basis_indices_sequential(
    square_lattice: SquareLattice
) -> None:
    """
    Test that index_to_basis() uses sequential indices starting at 0.

    The dictionary keys should be 0, 1, 2, 3.
    """
    mapping = square_lattice.index_to_basis()
    assert set(mapping.keys()) == {0, 1, 2, 3}


def test_square_lattice_index_to_basis_vectors_normalized(
    square_lattice: SquareLattice
) -> None:
    """
    Test that index_to_basis() returns normalized unit vectors.

    All basis vectors should be unit vectors (magnitude 1.0).
    """
    mapping = square_lattice.index_to_basis()
    for vec in mapping.values():
        magnitude = np.linalg.norm(vec)
        assert abs(magnitude - 1.0) < 1e-10


def test_square_lattice_index_to_basis_vectors_dtype(
    square_lattice: SquareLattice
) -> None:
    """
    Test that index_to_basis() returns float dtype arrays.

    All basis vectors should be numpy arrays with float dtype.
    """
    mapping = square_lattice.index_to_basis()
    for vec in mapping.values():
        assert vec.dtype == float


def test_square_lattice_custom_lattice_constant() -> None:
    """
    Test SquareLattice with various lattice constants.

    The lattice constant should affect basis vectors but not the
    index_to_basis mapping (which uses unit vectors).
    """
    for a in [0.5, 1.0, 2.0, 5.0]:
        lattice = SquareLattice(a=a)
        assert lattice.dimension == 2
        expected_vectors = np.array([[a, 0.0], [0.0, a]], dtype=float)
        assert np.array_equal(lattice.basis_vectors, expected_vectors)

        # index_to_basis should always return unit vectors
        mapping = lattice.index_to_basis()
        assert np.array_equal(mapping[0], np.array([1.0, 0.0], dtype=float))


def test_square_lattice_inherits_from_lattpy() -> None:
    """
    Test that SquareLattice properly inherits from lattpy.Lattice.

    SquareLattice should be an instance of both Lattice and
    lattpy.Lattice.
    """
    from lattpy import Lattice as LattpyLattice

    square_lattice = SquareLattice()
    assert isinstance(square_lattice, LattpyLattice)
    assert isinstance(square_lattice, Lattice)


def test_square_lattice_multiple_instances_independent() -> None:
    """
    Test that multiple SquareLattice instances are independent.

    Creating multiple instances should not affect each other.
    """
    lattice1 = SquareLattice(a=1.0)
    lattice2 = SquareLattice(a=2.0)

    assert lattice1.dimension == lattice2.dimension == 2
    assert not np.array_equal(lattice1.basis_vectors, lattice2.basis_vectors)

    mapping1 = lattice1.index_to_basis()
    mapping2 = lattice2.index_to_basis()
    # Mappings should be identical (unit vectors)
    assert np.array_equal(mapping1[0], mapping2[0])
    assert np.array_equal(mapping1[1], mapping2[1])


def test_square_lattice_index_to_basis_immutable() -> None:
    """
    Test that index_to_basis() returns new arrays each time.

    Modifying returned arrays should not affect subsequent calls.
    """
    lattice = SquareLattice()
    mapping1 = lattice.index_to_basis()
    vec = mapping1[0]
    vec[0] = 999.0  # Modify the array

    mapping2 = lattice.index_to_basis()
    # Second call should return original values
    assert np.array_equal(mapping2[0], np.array([1.0, 0.0], dtype=float))

