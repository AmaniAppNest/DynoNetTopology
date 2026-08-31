"""NV-center sensor abstraction."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class NVSensor:
    """Representation of a single NV-center sensor.

    Parameters
    ----------
    position:
        Sensor position in Cartesian coordinates ``(x, y, z)``.

    orientation:
        NV quantization-axis orientation as a three-dimensional vector.
    """

    position: np.ndarray
    orientation: np.ndarray

    def __post_init__(self) -> None:
        """Validate sensor geometry."""

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

        norm = np.linalg.norm(self.orientation)

        if norm == 0:
            raise ValueError(
                "orientation must be a non-zero vector."
            )

        self.orientation = (
            self.orientation / norm
        )

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
