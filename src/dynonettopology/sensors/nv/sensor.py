"""NV-center sensor model."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .hamiltonian import NVHamiltonian


@dataclass
class NVSensor:
    """Representation of a single NV-center sensor."""

    position: np.ndarray
    orientation: np.ndarray
    hamiltonian: NVHamiltonian | None = None

    def __post_init__(self) -> None:
        """Validate sensor geometry and configure the Hamiltonian."""

        self.position = np.asarray(
            self.position,
            dtype=float,
        )

        self.orientation = np.asarray(
            self.orientation,
            dtype=float,
        )

        if self.position.shape != (3,):
            raise ValueError(
                "position must have shape (3,)."
            )

        if self.orientation.shape != (3,):
            raise ValueError(
                "orientation must have shape (3,)."
            )

        norm = np.linalg.norm(
            self.orientation
        )

        if norm == 0:
            raise ValueError(
                "orientation must be a non-zero vector."
            )

        self.orientation = (
            self.orientation / norm
        )

        if self.hamiltonian is None:
            self.hamiltonian = NVHamiltonian()

    def project_field(
        self,
        magnetic_field: np.ndarray,
    ) -> float:
        """Project a magnetic field onto the NV axis."""

        magnetic_field = np.asarray(
            magnetic_field,
            dtype=float,
        )

        if magnetic_field.shape != (3,):
            raise ValueError(
                "magnetic_field must have shape (3,)."
            )

        return float(
            np.dot(
                magnetic_field,
                self.orientation,
            )
        )

    def energy_levels(
        self,
        magnetic_field: np.ndarray,
    ) -> np.ndarray:
        """Calculate field-dependent NV energy levels."""

        if self.hamiltonian is None:
            raise RuntimeError(
                "NV Hamiltonian is not configured."
            )

        return self.hamiltonian.eigenvalues(
            magnetic_field
        )

    def measure(
        self,
        magnetic_field: np.ndarray,
    ) -> float:
        """Return a simplified quantum-sensitive measurement.

        The current measurement is the field projection along
        the NV axis. The Hamiltonian is evaluated as part of
        the quantum-sensing model and is available through
        ``energy_levels``.
        """

        return self.project_field(
            magnetic_field
        )
