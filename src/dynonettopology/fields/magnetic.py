"""Time-dependent magnetic-field models."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class MagneticField:
    """Simple analytic time-dependent magnetic field."""

    amplitude: float = 1.0
    frequency: float = 1.0
    bias: np.ndarray | None = None

    def __post_init__(self) -> None:
        """Validate and prepare field parameters."""

        self.amplitude = float(
            self.amplitude
        )

        self.frequency = float(
            self.frequency
        )

        if self.bias is None:
            self.bias = np.zeros(
                3,
                dtype=float,
            )
        else:
            self.bias = np.asarray(
                self.bias,
                dtype=float,
            )

        if self.bias.shape != (3,):
            raise ValueError(
                "bias must have shape (3,)."
            )

        if not np.all(
            np.isfinite(self.bias)
        ):
            raise ValueError(
                "bias must contain finite values."
            )

    def evaluate(
        self,
        position: np.ndarray,
        time: float,
    ) -> np.ndarray:
        """Evaluate the magnetic field at one position and time.

        The current demonstration model uses a spatially uniform
        oscillating field. More physically detailed field models
        can replace this implementation later.
        """

        position = np.asarray(
            position,
            dtype=float,
        )

        if position.shape != (3,):
            raise ValueError(
                "position must have shape (3,)."
            )

        if not np.all(
            np.isfinite(position)
        ):
            raise ValueError(
                "position must contain finite values."
            )

        time = float(time)

        field = self.bias.copy()

        field[2] += (
            self.amplitude
            * np.sin(
                2.0
                * np.pi
                * self.frequency
                * time
            )
        )

        return field

    def evaluate_array(
        self,
        positions: np.ndarray,
        time: float,
    ) -> np.ndarray:
        """Evaluate the field at multiple sensor positions."""

        positions = np.asarray(
            positions,
            dtype=float,
        )

        if positions.ndim != 2:
            raise ValueError(
                "positions must be two-dimensional."
            )

        if positions.shape[1] != 3:
            raise ValueError(
                "positions must have shape (n, 3)."
            )

        return np.asarray(
            [
                self.evaluate(
                    position,
                    time,
                )
                for position in positions
            ],
            dtype=float,
        )
