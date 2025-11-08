"""Unit tests for the TriangularLattice class."""

import numpy as np
import pytest

from qfold.conformation.lattice import Lattice, TriangularLattice


@pytest.fixture(scope="function")
def triangular_lattice() -> TriangularLattice:
    """
    Fixture providing a TriangularLattice instance with default parameters.

    Returns:
        TriangularLattice instance for testing.
    """
    return TriangularLattice()


@pytest.fixture(scope="function")
def triangular_lattice_custom() -> TriangularLattice:
    """
    Fixture providing a TriangularLattice instance with custom lattice constant.

    Returns:
        TriangularLattice instance with a=2.0 for testing.
    """
    return TriangularLattice(a=2.0)


def test_triangular_lattice_initialization_default(
    triangular_lattice: TriangularLattice
) -> None:
    """
    Test that TriangularLattice can be initialized with default parameters.

    Default lattice constant should be 1.0.
    """
    assert triangular_lattice is not None
    assert isinstance(triangular_lattice, Lattice)
    assert isinstance(triangular_lattice, TriangularLattice)
    assert triangular_lattice.dimension == 2


def test_triangular_lattice_initialization_custom(
    triangular_lattice_custom: TriangularLattice
) -> None:
    """
    Test that TriangularLattice can be initialized with custom lattice constant.

    Custom lattice constant should be stored and used in basis vectors.
    """
    assert triangular_lattice_custom is not None
    assert triangular_lattice_custom.dimension == 2
    sqrt3_half = np.sqrt(3) / 2.0
    expected_vectors = np.array(
        [[2.0, 0.0], [1.0, 2.0 * sqrt3_half]], dtype=float
    )
    assert np.array_equal(
        triangular_lattice_custom.basis_vectors, expected_vectors
    )


def test_triangular_lattice_basis_vectors_default(
    triangular_lattice: TriangularLattice
) -> None:
    """
    Test that TriangularLattice has correct basis vectors with default a.

    Default basis vectors should be [[1.0, 0.0], [0.5, sqrt(3)/2]].
    """
    sqrt3_half = np.sqrt(3) / 2.0
    expected_vectors = np.array(
        [[1.0, 0.0], [0.5, sqrt3_half]], dtype=float
    )
    assert np.array_equal(triangular_lattice.basis_vectors, expected_vectors)


def test_triangular_lattice_index_to_basis_returns_dict(
    triangular_lattice: TriangularLattice
) -> None:
    """
    Test that index_to_basis() returns a dictionary.

    The return value should be a dictionary mapping int to np.ndarray.
    """
    mapping = triangular_lattice.index_to_basis()
    assert isinstance(mapping, dict)
    assert all(isinstance(k, int) for k in mapping.keys())
    assert all(isinstance(v, np.ndarray) for v in mapping.values())


def test_triangular_lattice_index_to_basis_canonical_order(
    triangular_lattice: TriangularLattice
) -> None:
    """
    Test that index_to_basis() returns canonical indexing.

    Canonical indexing should start at theta=0 ([1, 0]) and proceed
    counterclockwise with 6 neighbors: [1, 0] -> 0, [0.5, sqrt(3)/2] -> 1,
    [-0.5, sqrt(3)/2] -> 2, [-1, 0] -> 3, [-0.5, -sqrt(3)/2] -> 4,
    [0.5, -sqrt(3)/2] -> 5.
    """
    mapping = triangular_lattice.index_to_basis()
    assert len(mapping) == 6
    sqrt3_half = np.sqrt(3) / 2.0

    # Index 0: [1, 0] (right, theta=0)
    assert np.array_equal(mapping[0], np.array([1.0, 0.0], dtype=float))

    # Index 1: [0.5, sqrt(3)/2] (60° counterclockwise)
    assert np.array_equal(
        mapping[1], np.array([0.5, sqrt3_half], dtype=float)
    )

    # Index 2: [-0.5, sqrt(3)/2] (120° counterclockwise)
    assert np.array_equal(
        mapping[2], np.array([-0.5, sqrt3_half], dtype=float)
    )

    # Index 3: [-1, 0] (180° counterclockwise)
    assert np.array_equal(mapping[3], np.array([-1.0, 0.0], dtype=float))

    # Index 4: [-0.5, -sqrt(3)/2] (240° counterclockwise)
    assert np.array_equal(
        mapping[4], np.array([-0.5, -sqrt3_half], dtype=float)
    )

    # Index 5: [0.5, -sqrt(3)/2] (300° counterclockwise)
    assert np.array_equal(
        mapping[5], np.array([0.5, -sqrt3_half], dtype=float)
    )


def test_triangular_lattice_index_to_basis_indices_sequential(
    triangular_lattice: TriangularLattice
) -> None:
    """
    Test that index_to_basis() uses sequential indices starting at 0.

    The dictionary keys should be 0, 1, 2, 3, 4, 5.
    """
    mapping = triangular_lattice.index_to_basis()
    assert set(mapping.keys()) == {0, 1, 2, 3, 4, 5}


def test_triangular_lattice_index_to_basis_vectors_normalized(
    triangular_lattice: TriangularLattice
) -> None:
    """
    Test that index_to_basis() returns normalized unit vectors.

    All basis vectors should be unit vectors (magnitude 1.0).
    """
    mapping = triangular_lattice.index_to_basis()
    for vec in mapping.values():
        magnitude = np.linalg.norm(vec)
        assert abs(magnitude - 1.0) < 1e-10


def test_triangular_lattice_index_to_basis_vectors_dtype(
    triangular_lattice: TriangularLattice
) -> None:
    """
    Test that index_to_basis() returns float dtype arrays.

    All basis vectors should be numpy arrays with float dtype.
    """
    mapping = triangular_lattice.index_to_basis()
    for vec in mapping.values():
        assert vec.dtype == float


def test_triangular_lattice_custom_lattice_constant() -> None:
    """
    Test TriangularLattice with various lattice constants.

    The lattice constant should affect basis vectors but not the
    index_to_basis mapping (which uses unit vectors).
    """
    for a in [0.5, 1.0, 2.0, 5.0]:
        lattice = TriangularLattice(a=a)
        assert lattice.dimension == 2
        sqrt3_half = np.sqrt(3) / 2.0
        expected_vectors = np.array(
            [[a, 0.0], [a / 2.0, a * sqrt3_half]], dtype=float
        )
        assert np.array_equal(lattice.basis_vectors, expected_vectors)

        # index_to_basis should always return unit vectors
        mapping = lattice.index_to_basis()
        assert np.array_equal(mapping[0], np.array([1.0, 0.0], dtype=float))


def test_triangular_lattice_inherits_from_lattpy() -> None:
    """
    Test that TriangularLattice properly inherits from lattpy.Lattice.

    TriangularLattice should be an instance of both Lattice and
    lattpy.Lattice.
    """
    from lattpy import Lattice as LattpyLattice

    triangular_lattice = TriangularLattice()
    assert isinstance(triangular_lattice, LattpyLattice)
    assert isinstance(triangular_lattice, Lattice)


def test_triangular_lattice_multiple_instances_independent() -> None:
    """
    Test that multiple TriangularLattice instances are independent.

    Creating multiple instances should not affect each other.
    """
    lattice1 = TriangularLattice(a=1.0)
    lattice2 = TriangularLattice(a=2.0)

    assert lattice1.dimension == lattice2.dimension == 2
    assert not np.array_equal(lattice1.basis_vectors, lattice2.basis_vectors)

    mapping1 = lattice1.index_to_basis()
    mapping2 = lattice2.index_to_basis()
    # Mappings should be identical (unit vectors)
    assert np.array_equal(mapping1[0], mapping2[0])
    assert np.array_equal(mapping1[1], mapping2[1])


def test_triangular_lattice_index_to_basis_immutable() -> None:
    """
    Test that index_to_basis() returns new arrays each time.

    Modifying returned arrays should not affect subsequent calls.
    """
    lattice = TriangularLattice()
    mapping1 = lattice.index_to_basis()
    vec = mapping1[0]
    vec[0] = 999.0  # Modify the array

    mapping2 = lattice.index_to_basis()
    # Second call should return original values
    assert np.array_equal(mapping2[0], np.array([1.0, 0.0], dtype=float))


def test_triangular_lattice_angles_correct() -> None:
    """
    Test that triangular lattice neighbors are at correct angles.

    Neighbors should be at 0°, 60°, 120°, 180°, 240°, 300°.
    """
    lattice = TriangularLattice()
    mapping = lattice.index_to_basis()

    # Calculate angles using atan2
    angles = []
    for vec in mapping.values():
        angle = np.arctan2(vec[1], vec[0])
        # Convert to degrees and normalize to [0, 360)
        angle_deg = np.degrees(angle)
        if angle_deg < 0:
            angle_deg += 360
        angles.append(angle_deg)

    expected_angles = [0.0, 60.0, 120.0, 180.0, 240.0, 300.0]
    for actual, expected in zip(sorted(angles), sorted(expected_angles)):
        assert abs(actual - expected) < 1e-10

