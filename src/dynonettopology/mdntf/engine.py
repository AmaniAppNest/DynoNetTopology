"""MDNTF orchestration engine."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .complexes import clique_complex
from .filtration import create_filtration
from .persistence import (
    PersistenceResult,
    compute_persistence,
)
from .tracker import (
    FeatureTracker,
    TopologicalFeature,
)


@dataclass
class MDNTFResult:
    """Result of an MDNTF analysis."""

    persistence: list[PersistenceResult]
    tracker: FeatureTracker


class MDNTFEngine:
    """Coordinate multiscale topological analysis."""

    def __init__(
        self,
        thresholds: list[float] | np.ndarray,
        max_dimension: int = 2,
    ) -> None:
        self.thresholds = np.asarray(
            thresholds,
            dtype=float,
        )

        if self.thresholds.ndim != 1:
            raise ValueError(
                "thresholds must be one-dimensional."
            )

        if len(self.thresholds) == 0:
            raise ValueError(
                "At least one threshold is required."
            )

        if not np.all(
            np.isfinite(self.thresholds)
        ):
            raise ValueError(
                "thresholds must contain finite values."
            )

        if np.any(self.thresholds < 0):
            raise ValueError(
                "thresholds must be non-negative."
            )

        self.thresholds = np.sort(
            self.thresholds
        )

        self.max_dimension = int(
            max_dimension
        )

        if self.max_dimension < 0:
            raise ValueError(
                "max_dimension must be non-negative."
            )

    def analyze_adjacency(
        self,
        adjacency: np.ndarray,
        time: float,
    ) -> MDNTFResult:
        """Analyze one network state across filtration scales."""

        adjacency = np.asarray(
            adjacency,
            dtype=float,
        )

        if adjacency.ndim != 2:
            raise ValueError(
                "adjacency must be two-dimensional."
            )

        if (
            adjacency.shape[0]
            != adjacency.shape[1]
        ):
            raise ValueError(
                "adjacency must be square."
            )

        if not np.all(
            np.isfinite(adjacency)
        ):
            raise ValueError(
                "adjacency must contain finite values."
            )

        time = float(time)

        if not np.isfinite(time):
            raise ValueError(
                "time must be finite."
            )

        filtration = create_filtration(
            adjacency,
            self.thresholds,
        )

        persistence_results: list[
            PersistenceResult
        ] = []

        tracker = FeatureTracker()

        for level in filtration.levels:
            filtered_adjacency = filtration.apply(
                level
            )

            complex_ = clique_complex(
                filtered_adjacency,
                max_dimension=self.max_dimension,
            )

            simplex_filtration: list[
                tuple[tuple[int, ...], float]
            ] = []

            for dimension, simplices in (
                complex_.simplices.items()
            ):
                for simplex in simplices:
                    simplex_filtration.append(
                        (
                            simplex,
                            level.threshold,
                        )
                    )

            if not simplex_filtration:
                continue

            persistence_result = compute_persistence(
                simplex_filtration
            )

            persistence_results.append(
                persistence_result
            )

            for dimension, intervals in (
                persistence_result.intervals.items()
            ):
                for birth, death in intervals:
                    tracker.create_trajectory(
                        TopologicalFeature(
                            time=time,
                            dimension=dimension,
                            birth=birth,
                            death=death,
                        )
                    )

        return MDNTFResult(
            persistence=persistence_results,
            tracker=tracker,
        )
