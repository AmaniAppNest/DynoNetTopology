"""Synthetic magnetic-field models."""

from __future__ import annotations

import numpy as np

from .base import MagneticFieldModel


class SyntheticMagneticField(MagneticFieldModel):
    """Simple magnetic field used for pipeline development.

    The field is aligned with the z-axis and its amplitude
    depends on the mean system state and the distance from
    the origin.
    """

    def __init__(self, coupling: float = 1.0) -> None:
        if coupling < 0:
            raise ValueError("coupling must be non-negative.")

        self.coupling = coupling

    def evaluate(
        self,
        positions: np.ndarray,
        state: np.ndarray,
        time: float,
    ) -> np.ndarray:
        """Evaluate the synthetic magnetic field."""

        positions = np.asarray(positions, dtype=float)
        state = np.asarray(state, dtype=float)

        if positions.ndim != 2 or positions.shape[1] != 3:
            raise ValueError(
                "positions must have shape (n_sensors, 3)."
            )

        if state.ndim != 1:
            raise ValueError(
                "state must be a one-dimensional array."
            )

        if not np.isfinite(time):
            raise ValueError("time must be finite.")

        distance_squared = np.sum(
            positions**2,
            axis=1,
        )

        amplitude = (
            self.coupling
            * np.mean(state)
            * np.exp(-distance_squared)
        )

        field = np.zeros(
            (len(positions), 3),
            dtype=float,
        )

        field[:, 2] = amplitude

        return field
