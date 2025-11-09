"""Unit tests for the Conformation class."""

import pytest

from qfold.conformation.conformation import Conformation
from qfold.conformation.lattice import (
    HexagonalLattice,
    Lattice,
    SquareLattice,
    TriangularLattice,
)
from qfold.conformation.path import Path


@pytest.fixture(scope="function")
def square_lattice() -> SquareLattice:
    """
    Fixture providing a SquareLattice instance.

    Returns:
        SquareLattice instance for testing.
    """
    return SquareLattice()


@pytest.fixture(scope="function")
def triangular_lattice() -> TriangularLattice:
    """
    Fixture providing a TriangularLattice instance.

    Returns:
        TriangularLattice instance for testing.
    """
    return TriangularLattice()


@pytest.fixture(scope="function")
def hexagonal_lattice() -> HexagonalLattice:
    """
    Fixture providing a HexagonalLattice instance.

    Returns:
        HexagonalLattice instance for testing.
    """
    return HexagonalLattice()


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


@pytest.fixture(scope="function")
def square_conformation(
    simple_path: Path, square_lattice: SquareLattice
) -> Conformation:
    """
    Fixture providing a Conformation with square lattice.

    Returns:
        Conformation instance for testing.
    """
    return Conformation(path=simple_path, lattice=square_lattice)


def test_conformation_initialization_valid(
    simple_path: Path, square_lattice: SquareLattice
) -> None:
    """
    Test that Conformation can be initialized with valid path and lattice.

    A conformation with valid path and lattice should be created
    successfully.
    """
    conformation = Conformation(path=simple_path, lattice=square_lattice)
    assert conformation is not None
    assert conformation.path == simple_path
    assert conformation.lattice is square_lattice


def test_conformation_initialization_empty_path(
    empty_path: Path, square_lattice: SquareLattice
) -> None:
    """
    Test that Conformation can be initialized with empty path.

    An empty path should be valid.
    """
    conformation = Conformation(path=empty_path, lattice=square_lattice)
    assert conformation is not None
    assert conformation.path == empty_path
    assert len(conformation.path.moves) == 0


def test_conformation_initialization_square_lattice(
    simple_path: Path, square_lattice: SquareLattice
) -> None:
    """
    Test Conformation with SquareLattice.

    Square lattice should work correctly with conformations.
    """
    conformation = Conformation(path=simple_path, lattice=square_lattice)
    assert isinstance(conformation.lattice, SquareLattice)
    assert isinstance(conformation.lattice, Lattice)


def test_conformation_initialization_triangular_lattice(
    simple_path: Path, triangular_lattice: TriangularLattice
) -> None:
    """
    Test Conformation with TriangularLattice.

    Triangular lattice should work correctly with conformations.
    """
    conformation = Conformation(path=simple_path, lattice=triangular_lattice)
    assert isinstance(conformation.lattice, TriangularLattice)
    assert isinstance(conformation.lattice, Lattice)


def test_conformation_initialization_hexagonal_lattice(
    simple_path: Path, hexagonal_lattice: HexagonalLattice
) -> None:
    """
    Test Conformation with HexagonalLattice.

    Hexagonal lattice should work correctly with conformations.
    """
    conformation = Conformation(path=simple_path, lattice=hexagonal_lattice)
    assert isinstance(conformation.lattice, HexagonalLattice)
    assert isinstance(conformation.lattice, Lattice)


def test_conformation_initialization_non_path_raises_type_error(
    square_lattice: SquareLattice
) -> None:
    """
    Test that Conformation raises TypeError for non-Path input.

    A conformation with non-Path should raise TypeError.
    """
    with pytest.raises(TypeError, match="path must be a Path instance"):
        Conformation(path=[0, 1, 2], lattice=square_lattice)  # type: ignore

    with pytest.raises(TypeError, match="path must be a Path instance"):
        Conformation(path="invalid", lattice=square_lattice)  # type: ignore

    with pytest.raises(TypeError, match="path must be a Path instance"):
        Conformation(path=None, lattice=square_lattice)  # type: ignore


def test_conformation_initialization_non_lattice_raises_type_error(
    simple_path: Path
) -> None:
    """
    Test that Conformation raises TypeError for non-Lattice input.

    A conformation with non-Lattice should raise TypeError.
    """
    with pytest.raises(TypeError, match="lattice must be a Lattice instance"):
        Conformation(path=simple_path, lattice="invalid")  # type: ignore

    with pytest.raises(TypeError, match="lattice must be a Lattice instance"):
        Conformation(path=simple_path, lattice=[1, 2, 3])  # type: ignore

    with pytest.raises(TypeError, match="lattice must be a Lattice instance"):
        Conformation(path=simple_path, lattice=None)  # type: ignore


def test_conformation_path_attribute(
    simple_path: Path, square_lattice: SquareLattice
) -> None:
    """
    Test that Conformation path attribute is accessible.

    The path attribute should be accessible and correct.
    """
    conformation = Conformation(path=simple_path, lattice=square_lattice)
    assert conformation.path == simple_path
    assert conformation.path.moves == [0, 1, 2, 3]


def test_conformation_lattice_attribute(
    simple_path: Path, square_lattice: SquareLattice
) -> None:
    """
    Test that Conformation lattice attribute is accessible.

    The lattice attribute should be accessible and correct.
    """
    conformation = Conformation(path=simple_path, lattice=square_lattice)
    assert conformation.lattice is square_lattice
    assert isinstance(conformation.lattice, SquareLattice)


def test_conformation_equality_same_path_and_lattice(
    simple_path: Path, square_lattice: SquareLattice
) -> None:
    """
    Test that Conformation instances with same path and lattice are equal.

    Two conformations with identical path and lattice should be equal.
    """
    conf1 = Conformation(path=simple_path, lattice=square_lattice)
    conf2 = Conformation(path=simple_path, lattice=square_lattice)
    assert conf1 == conf2


def test_conformation_equality_different_path(
    square_lattice: SquareLattice
) -> None:
    """
    Test that Conformation instances with different paths are not equal.

    Two conformations with different paths should not be equal.
    """
    path1 = Path(moves=[0, 1, 2, 3])
    path2 = Path(moves=[0, 1, 2])
    conf1 = Conformation(path=path1, lattice=square_lattice)
    conf2 = Conformation(path=path2, lattice=square_lattice)
    assert conf1 != conf2


def test_conformation_equality_different_lattice(
    simple_path: Path, square_lattice: SquareLattice
) -> None:
    """
    Test that Conformation instances with different lattices are not equal.

    Two conformations with different lattices should not be equal.
    """
    triangular_lattice = TriangularLattice()
    conf1 = Conformation(path=simple_path, lattice=square_lattice)
    conf2 = Conformation(path=simple_path, lattice=triangular_lattice)
    assert conf1 != conf2


def test_conformation_equality_different_type() -> None:
    """
    Test that Conformation is not equal to non-Conformation objects.

    A conformation should not be equal to other types.
    """
    path = Path(moves=[0, 1, 2])
    lattice = SquareLattice()
    conformation = Conformation(path=path, lattice=lattice)

    assert conformation != path
    assert conformation != lattice
    assert conformation != "not a conformation"
    assert conformation != [0, 1, 2]
    assert conformation != None  # noqa: E711


def test_conformation_repr_contains_path_and_lattice(
    simple_path: Path, square_lattice: SquareLattice
) -> None:
    """
    Test that Conformation __repr__ contains path and lattice information.

    The string representation should include path and lattice information.
    """
    conformation = Conformation(path=simple_path, lattice=square_lattice)
    repr_str = repr(conformation)
    assert "Conformation" in repr_str
    assert "path" in repr_str
    assert "lattice" in repr_str
    assert "SquareLattice" in repr_str


def test_conformation_repr_different_lattices() -> None:
    """
    Test that Conformation __repr__ shows correct lattice type names.

    Different lattice types should show in the representation.
    """
    path = Path(moves=[0, 1, 2])

    square_conf = Conformation(path=path, lattice=SquareLattice())
    assert "SquareLattice" in repr(square_conf)

    triangular_conf = Conformation(path=path, lattice=TriangularLattice())
    assert "TriangularLattice" in repr(triangular_conf)

    hexagonal_conf = Conformation(path=path, lattice=HexagonalLattice())
    assert "HexagonalLattice" in repr(hexagonal_conf)


def test_conformation_path_mutable(
    simple_path: Path, square_lattice: SquareLattice
) -> None:
    """
    Test that Conformation path attribute can be modified.

    The path moves can be modified through the conformation.
    """
    conformation = Conformation(path=simple_path, lattice=square_lattice)
    assert conformation.path.moves == [0, 1, 2, 3]

    # Modify the path through the conformation
    conformation.path.moves.append(0)
    assert conformation.path.moves == [0, 1, 2, 3, 0]


def test_conformation_multiple_instances_independent() -> None:
    """
    Test that multiple Conformation instances are independent.

    Creating multiple instances should not affect each other.
    """
    path1 = Path(moves=[0, 1, 2])
    path2 = Path(moves=[3, 4, 5])
    lattice1 = SquareLattice()
    lattice2 = TriangularLattice()

    conf1 = Conformation(path=path1, lattice=lattice1)
    conf2 = Conformation(path=path2, lattice=lattice2)

    assert conf1.path == path1
    assert conf2.path == path2
    assert conf1.lattice is lattice1
    assert conf2.lattice is lattice2
    assert conf1 != conf2


def test_conformation_square_lattice_path() -> None:
    """
    Test Conformation with square lattice and appropriate path.

    Square lattice has 4 neighbors (indices 0-3).
    """
    path = Path(moves=[0, 1, 2, 3, 0])
    lattice = SquareLattice()
    conformation = Conformation(path=path, lattice=lattice)

    assert conformation.path.moves == [0, 1, 2, 3, 0]
    assert isinstance(conformation.lattice, SquareLattice)


def test_conformation_triangular_lattice_path() -> None:
    """
    Test Conformation with triangular lattice and appropriate path.

    Triangular lattice has 6 neighbors (indices 0-5).
    """
    path = Path(moves=[0, 1, 2, 3, 4, 5])
    lattice = TriangularLattice()
    conformation = Conformation(path=path, lattice=lattice)

    assert conformation.path.moves == [0, 1, 2, 3, 4, 5]
    assert isinstance(conformation.lattice, TriangularLattice)


def test_conformation_hexagonal_lattice_path() -> None:
    """
    Test Conformation with hexagonal lattice and appropriate path.

    Hexagonal lattice has 3 neighbors (indices 0-2).
    """
    path = Path(moves=[0, 1, 2, 0, 1, 2])
    lattice = HexagonalLattice()
    conformation = Conformation(path=path, lattice=lattice)

    assert conformation.path.moves == [0, 1, 2, 0, 1, 2]
    assert isinstance(conformation.lattice, HexagonalLattice)


def test_conformation_empty_path_with_lattice(
    empty_path: Path, square_lattice: SquareLattice
) -> None:
    """
    Test Conformation with empty path and lattice.

    An empty path should be valid with any lattice.
    """
    conformation = Conformation(path=empty_path, lattice=square_lattice)
    assert conformation.path.moves == []
    assert conformation.lattice is square_lattice


def test_conformation_single_move_path() -> None:
    """
    Test Conformation with single move path.

    A path with one move should work correctly.
    """
    path = Path(moves=[0])
    lattice = SquareLattice()
    conformation = Conformation(path=path, lattice=lattice)

    assert conformation.path.moves == [0]
    assert len(conformation.path.moves) == 1

