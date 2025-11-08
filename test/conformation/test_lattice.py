"""Unit tests for the Lattice base class."""

from typing import Dict

import numpy as np
import pytest

from qfold.conformation.lattice import Lattice


class CompleteLattice(Lattice):
    """Complete lattice implementation for testing."""

    def __init__(
        self, dimension: int, basis_vectors: np.ndarray
    ) -> None:
        """Initialize test lattice."""
        super().__init__(dimension, basis_vectors)

    def index_to_basis(self) -> Dict[int, np.ndarray]:
        """Return index to basis mapping."""
        return {
            0: np.array([1.0, 0.0], dtype=float),
            1: np.array([0.0, 1.0], dtype=float),
        }


class IncompleteLattice(Lattice):
    """Lattice missing index_to_basis() implementation."""

    def __init__(
        self, dimension: int, basis_vectors: np.ndarray
    ) -> None:
        """Initialize incomplete lattice."""
        super().__init__(dimension, basis_vectors)


def test_lattice_is_abstract() -> None:
    """
    Test that Lattice cannot be instantiated directly.

    Since Lattice is an abstract base class, attempting to
    instantiate it should raise a TypeError.
    """
    basis_vectors = np.array([[1.0, 0.0], [0.0, 1.0]], dtype=float)
    with pytest.raises(TypeError):
        Lattice(2, basis_vectors)  # type: ignore


def test_concrete_lattice_must_implement_index_to_basis() -> None:
    """
    Test that concrete classes must implement index_to_basis() method.

    A class that inherits from Lattice but doesn't implement
    index_to_basis() should raise TypeError when instantiated.
    """
    basis_vectors = np.array([[1.0, 0.0], [0.0, 1.0]], dtype=float)
    with pytest.raises(TypeError):
        IncompleteLattice(2, basis_vectors)


def test_complete_concrete_lattice_can_be_instantiated() -> None:
    """
    Test that a complete concrete implementation can be instantiated.

    A class that implements index_to_basis() should be instantiable.
    """
    basis_vectors = np.array([[1.0, 0.0], [0.0, 1.0]], dtype=float)
    lattice = CompleteLattice(2, basis_vectors)
    assert lattice is not None
    assert isinstance(lattice, Lattice)


def test_lattice_stores_dimension() -> None:
    """
    Test that Lattice stores the dimension correctly.

    The dimension attribute should match the value passed to __init__.
    """
    basis_vectors = np.array([[1.0, 0.0], [0.0, 1.0]], dtype=float)
    lattice = CompleteLattice(2, basis_vectors)
    assert lattice.dimension == 2

    basis_vectors_3d = np.array(
        [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]], dtype=float
    )
    lattice_3d = CompleteLattice(3, basis_vectors_3d)
    assert lattice_3d.dimension == 3


def test_lattice_stores_basis_vectors() -> None:
    """
    Test that Lattice stores the basis vectors correctly.

    The basis_vectors property should return the vectors passed to __init__.
    """
    basis_vectors = np.array([[1.0, 0.0], [0.0, 1.0]], dtype=float)
    lattice = CompleteLattice(2, basis_vectors)
    stored_vectors = lattice.basis_vectors
    assert np.array_equal(stored_vectors, basis_vectors)
    assert stored_vectors.shape == (2, 2)


def test_lattice_basis_vectors_property() -> None:
    """
    Test that basis_vectors property returns correct values.

    The property should return the stored basis vectors.
    """
    basis_vectors = np.array([[2.0, 0.0], [0.0, 2.0]], dtype=float)
    lattice = CompleteLattice(2, basis_vectors)
    result = lattice.basis_vectors
    assert np.array_equal(result, basis_vectors)
    assert result.dtype == float
