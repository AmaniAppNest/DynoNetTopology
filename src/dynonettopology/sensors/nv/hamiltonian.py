"""Spin-1 Hamiltonian model for an NV center."""

from __future__ import annotations

import numpy as np


class NVHamiltonian:
    """Simplified spin-1 NV-center Hamiltonian.

    The model includes the zero-field splitting and Zeeman
    interaction:

        H = D S_z^2 + gamma_e (B_x S_x + B_y S_y + B_z S_z)

    Parameters
    ----------
    zero_field_splitting:
        Zero-field splitting parameter D.

    gyromagnetic_ratio:
        Electron gyromagnetic ratio gamma_e.
    """

    def __init__(
        self,
        zero_field_splitting: float = 2.87e9,
        gyromagnetic_ratio: float = 28.024e9,
    ) -> None:
        self.zero_field_splitting = float(
            zero_field_splitting
        )

        self.gyromagnetic_ratio = float(
            gyromagnetic_ratio
        )

        self._spin_matrices = self._create_spin_matrices()

    @staticmethod
    def _create_spin_matrices() -> tuple[
        np.ndarray,
        np.ndarray,
        np.ndarray,
    ]:
        """Create dimensionless spin-1 operators."""

        sqrt_two = np.sqrt(2.0)

        s_x = (
            1.0 / sqrt_two
        ) * np.array(
            [
                [0.0, 1.0, 0.0],
                [1.0, 0.0, 1.0],
                [0.0, 1.0, 0.0],
            ],
            dtype=complex,
        )

        s_y = (
            1.0 / sqrt_two
        ) * np.array(
            [
                [0.0, -1.0j, 0.0],
                [1.0j, 0.0, -1.0j],
                [0.0, 1.0j, 0.0],
            ],
            dtype=complex,
        )

        s_z = np.array(
            [
                [1.0, 0.0, 0.0],
                [0.0, 0.0, 0.0],
                [0.0, 0.0, -1.0],
            ],
            dtype=complex,
        )

        return s_x, s_y, s_z

    @property
    def spin_matrices(
        self,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Return the spin-1 matrices."""

        return self._spin_matrices

    def matrix(
        self,
        magnetic_field: np.ndarray,
    ) -> np.ndarray:
        """Construct the Hamiltonian for a magnetic field.

        Parameters
        ----------
        magnetic_field:
            Magnetic-field vector ``[Bx, By, Bz]``.

        Returns
        -------
        numpy.ndarray
            Complex 3x3 Hamiltonian matrix.
        """

        magnetic_field = np.asarray(
            magnetic_field,
            dtype=float,
        )

        if magnetic_field.shape != (3,):
            raise ValueError(
                "magnetic_field must have shape (3,)."
            )

        if not np.all(
            np.isfinite(magnetic_field)
        ):
            raise ValueError(
                "magnetic_field must contain finite values."
            )

        bx, by, bz = magnetic_field

        s_x, s_y, s_z = self._spin_matrices

        h_zero_field = (
            self.zero_field_splitting
            * (s_z @ s_z)
        )

        h_zeeman = (
            self.gyromagnetic_ratio
            * (
                bx * s_x
                + by * s_y
                + bz * s_z
            )
        )

        return (
            h_zero_field
            + h_zeeman
        )

    def eigenvalues(
        self,
        magnetic_field: np.ndarray,
    ) -> np.ndarray:
        """Return sorted Hamiltonian eigenvalues."""

        hamiltonian = self.matrix(
            magnetic_field
        )

        return np.linalg.eigvalsh(
            hamiltonian
        )
