"""Base interfaces for dynamic physical systems."""

from abc import ABC, abstractmethod

import numpy as np


class DynamicSystem(ABC):
    """Abstract interface for a time-dependent physical system."""

    @abstractmethod
    def reset(self, state: np.ndarray | None = None) -> np.ndarray:
        """Return the initial system state."""
        raise NotImplementedError

    @abstractmethod
    def step(self, state: np.ndarray, dt: float) -> np.ndarray:
        """Advance the system state by one time step."""
        raise NotImplementedError

    @abstractmethod
    def observe(self, state: np.ndarray) -> np.ndarray:
        """Convert the internal state into observable quantities."""
        raise NotImplementedError
