"""Multiscale filtration for dynamic weighted networks."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class FiltrationLevel:
    """A single network filtration level."""

    threshold: float

    def __post_init__(self) -> None:
        """Validate the filtration threshold."""

        if not np.isfinite(self.threshold):
            raise ValueError(
                "threshold must be finite."
            )

        if self.threshold < 0:
            raise ValueError(
                "threshold must be non-negative."
            )


@dataclass
class NetworkFiltration:
    """Apply multiple thresholds to a weighted adjacency matrix."""

    adjacency: np.ndarray
    levels: list[FiltrationLevel]

    def __post_init__(self) -> None:
        """Validate the adjacency matrix and filtration levels."""

        self.adjacency = np.asarray(
            self.adjacency,
            dtype=float,
        )

        if self.adjacency.ndim != 2:
            raise ValueError(
                "adjacency must be two-dimensional."
            )

        if (
            self.adjacency.shape[0]
            != self.adjacency.shape[1]
        ):
            raise ValueError(
                "adjacency must be square."
            )

        if not np.all(
            np.isfinite(self.adjacency)
        ):
            raise ValueError(
                "adjacency must contain finite values."
            )

        if not self.levels:
            raise ValueError(
                "At least one filtration level is required."
            )

    def apply(
        self,
        level: FiltrationLevel,
    ) -> np.ndarray:
        """Return the thresholded adjacency matrix."""

        result = self.adjacency.copy()

        result[
            result < level.threshold
        ] = 0.0

        np.fill_diagonal(
            result,
            0.0,
        )

        return result

    def all_levels(
        self,
    ) -> list[np.ndarray]:
        """Return the filtered network at every scale."""

        return [
            self.apply(level)
            for level in self.levels
        ]


def create_filtration(
    adjacency: np.ndarray,
    thresholds: np.ndarray | list[float],
) -> NetworkFiltration:
    """Create a multiscale network filtration."""

    thresholds = np.asarray(
        thresholds,
        dtype=float,
    )

    if thresholds.ndim != 1:
        raise ValueError(
            "thresholds must be one-dimensional."
        )

    if len(thresholds) == 0:
        raise ValueError(
            "At least one threshold is required."
        )

    levels = [
        FiltrationLevel(
            threshold=float(threshold)
        )
        for threshold in thresholds
    ]

    levels.sort(
        key=lambda level: level.threshold
    )

    return NetworkFiltration(
        adjacency=adjacency,
        levels=levels,
    )
