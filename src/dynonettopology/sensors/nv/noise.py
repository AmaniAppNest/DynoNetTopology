"""Noise models for NV-center measurements."""

from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np


class NoiseModel(ABC):
    """Abstract interface for sensor noise."""

    @abstractmethod
    def apply(
        self,
        signal: np.ndarray,
    ) -> np.ndarray:
        """Apply noise to an ideal signal."""
        raise NotImplementedError


class GaussianNoise(NoiseModel):
    """Additive Gaussian measurement noise."""

    def __init__(
        self,
        standard_deviation: float = 0.0,
        seed: int | None = 42,
    ) -> None:
        if standard_deviation < 0:
            raise ValueError(
                "standard_deviation must be non-negative."
            )

        self.standard_deviation = float(
            standard_deviation
        )

        self.rng = np.random.default_rng(seed)

    def apply(
        self,
        signal: np.ndarray,
    ) -> np.ndarray:
        """Return the signal with Gaussian noise added."""

        signal = np.asarray(
            signal,
            dtype=float,
        )

        if self.standard_deviation == 0:
            return signal.copy()

        noise = self.rng.normal(
            loc=0.0,
            scale=self.standard_deviation,
            size=signal.shape,
        )

        return signal + noise
