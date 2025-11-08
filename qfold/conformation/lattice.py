"""Lattice base class for protein folding conformations."""

from abc import ABC, abstractmethod
from typing import Dict

import numpy as np
from lattpy import Lattice as LattpyLattice


class Lattice(LattpyLattice, ABC):
    """
    Base class for lattice representations of protein conformations.

    Inherits from lattpy.Lattice to provide lattice structure
    functionality. Subclasses must implement canonical indexing methods.
    """

    def __init__(
        self, dimension: int, basis_vectors: np.ndarray
    ) -> None:
        """
        Initialize a lattice instance.

        Args:
            dimension: The dimensionality of the lattice (e.g., 2 for 2D,
                       3 for 3D).
            basis_vectors: The basis vectors of the unit cell as a
                          numpy array of shape (dimension, dimension).
        """
        super().__init__(basis_vectors)
        self.dimension = dimension
        self._basis_vectors = basis_vectors

    @property
    def basis_vectors(self) -> np.ndarray:
        """
        Get the basis vectors of the lattice.

        Returns:
            The basis vectors as a numpy array.
        """
        return self._basis_vectors

    @abstractmethod
    def index_to_basis(self) -> Dict[int, np.ndarray]:
        """
        Return a mapping from canonical index to basis vector.

        The canonical indexing in 2D starts at theta=0 position
        ([1, 0]) and indexes counterclockwise around the origin
        (right-hand rule).

        Returns:
            Dictionary mapping canonical index to basis vector
            numpy array.
        """
        pass


class SquareLattice(Lattice):
    """
    Concrete class for a 2D square lattice.

    Canonical indexing (starting at theta=0, counterclockwise):
        - [1, 0] -> 0 (right)
        - [0, 1] -> 1 (up)
        - [-1, 0] -> 2 (left)
        - [0, -1] -> 3 (down)
    """

    def __init__(self, a: float = 1.0) -> None:
        """
        Initialize a square lattice.

        Args:
            a: Lattice constant (default is 1.0).
        """
        basis_vectors = np.array([[a, 0.0], [0.0, a]], dtype=float)
        super().__init__(dimension=2, basis_vectors=basis_vectors)
        self._a = a

    def index_to_basis(self) -> Dict[int, np.ndarray]:
        """
        Return a mapping from canonical index to basis vector.

        Returns:
            Dictionary mapping canonical index (0-3) to basis vector
            numpy array. Indexing starts at theta=0 ([1, 0]) and
            proceeds counterclockwise.
        """
        return {
            0: np.array([1.0, 0.0], dtype=float),
            1: np.array([0.0, 1.0], dtype=float),
            2: np.array([-1.0, 0.0], dtype=float),
            3: np.array([0.0, -1.0], dtype=float),
        }


class TriangularLattice(Lattice):
    """
    Concrete class for a 2D triangular lattice.

    Each point has 6 neighbors arranged in a hexagon.
    Canonical indexing (starting at theta=0, counterclockwise):
        - [1, 0] -> 0 (right)
        - [0.5, sqrt(3)/2] -> 1 (60°)
        - [-0.5, sqrt(3)/2] -> 2 (120°)
        - [-1, 0] -> 3 (left)
        - [-0.5, -sqrt(3)/2] -> 4 (240°)
        - [0.5, -sqrt(3)/2] -> 5 (300°)
    """

    def __init__(self, a: float = 1.0) -> None:
        """
        Initialize a triangular lattice.

        Args:
            a: Lattice constant (default is 1.0).
        """
        sqrt3_half = np.sqrt(3) / 2.0
        basis_vectors = np.array(
            [[a, 0.0], [a / 2.0, a * sqrt3_half]], dtype=float
        )
        super().__init__(dimension=2, basis_vectors=basis_vectors)
        self._a = a
        self._sqrt3_half = sqrt3_half

    def index_to_basis(self) -> Dict[int, np.ndarray]:
        """
        Return a mapping from canonical index to basis vector.

        Returns:
            Dictionary mapping canonical index (0-5) to basis vector
            numpy array. Indexing starts at theta=0 ([1, 0]) and
            proceeds counterclockwise.
        """
        sqrt3_half = self._sqrt3_half
        return {
            0: np.array([1.0, 0.0], dtype=float),
            1: np.array([0.5, sqrt3_half], dtype=float),
            2: np.array([-0.5, sqrt3_half], dtype=float),
            3: np.array([-1.0, 0.0], dtype=float),
            4: np.array([-0.5, -sqrt3_half], dtype=float),
            5: np.array([0.5, -sqrt3_half], dtype=float),
        }


class HexagonalLattice(Lattice):
    """
    Concrete class for a 2D hexagonal (honeycomb) lattice.

    Each point has 3 neighbors arranged at 120° intervals.
    Canonical indexing (starting at theta=0, counterclockwise):
        - [1, 0] -> 0 (right)
        - [-0.5, sqrt(3)/2] -> 1 (120°)
        - [-0.5, -sqrt(3)/2] -> 2 (240°)
    """

    def __init__(self, a: float = 1.0) -> None:
        """
        Initialize a hexagonal lattice.

        Args:
            a: Lattice constant (default is 1.0).
        """
        sqrt3_half = np.sqrt(3) / 2.0
        basis_vectors = np.array(
            [[a, 0.0], [a / 2.0, a * sqrt3_half]], dtype=float
        )
        super().__init__(dimension=2, basis_vectors=basis_vectors)
        self._a = a
        self._sqrt3_half = sqrt3_half

    def index_to_basis(self) -> Dict[int, np.ndarray]:
        """
        Return a mapping from canonical index to basis vector.

        Returns:
            Dictionary mapping canonical index (0-2) to basis vector
            numpy array. Indexing starts at theta=0 ([1, 0]) and
            proceeds counterclockwise.
        """
        sqrt3_half = self._sqrt3_half
        return {
            0: np.array([1.0, 0.0], dtype=float),
            1: np.array([-0.5, sqrt3_half], dtype=float),
            2: np.array([-0.5, -sqrt3_half], dtype=float),
        }

