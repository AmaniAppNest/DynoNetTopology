"""Base interface for magnetic-field models."""

from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np


class MagneticFieldModel(ABC):
    """Abstract interface for time-dependent magnetic fields."""

    @abstractmethod
    def evaluate(
        self,
        positions: np.ndarray,
        state: np.ndarray,
        time: float,
    ) -> np.ndarray:
        """Evaluate the magnetic field at sensor positions.

        Parameters
        ----------
        positions:
            Sensor positions with shape ``(n_sensors, 3)``.

        state:
            Current physical-system state.

        time:
            Current simulation time.

        Returns
        -------
        numpy.ndarray
            Magnetic-field vectors with shape
            ``(n_sensors, 3)``.
        """
        raise NotImplementedError
