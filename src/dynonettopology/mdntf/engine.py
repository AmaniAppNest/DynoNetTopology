"""MDNTF orchestration engine."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .complexes import clique_complex
from .filtration import create_filtration
from .persistence import PersistenceResult, compute_persistence
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

        filtration = create_filtration(
            adjacency,
            self.thresholds,
        )

        persistence_results: list[
            PersistenceResult
        ] = []

        tracker = FeatureTracker()

        for level, filtered_adjacency in zip(
            filtration.levels,
            filtration.all_levels(),
        ):
            complex_ = clique_complex(
                filtered_adjacency,
                max_dimension=self.max_dimension,
            )

            simplex_filtration = []

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
                            time=float(time),
                            dimension=dimension,
                            birth=birth,
                            death=death,
                        )
                    )

        return MDNTFResult(
            persistence=persistence_results,
            tracker=tracker,
        )
