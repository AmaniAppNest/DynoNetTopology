"""Persistent-homology analysis for simplicial complexes."""

from __future__ import annotations

from dataclasses import dataclass

import gudhi


@dataclass
class PersistenceResult:
    """Persistent-homology result."""

    intervals: dict[int, list[tuple[float, float]]]

    def intervals_for(
        self,
        dimension: int,
    ) -> list[tuple[float, float]]:
        """Return persistence intervals for one dimension."""

        return self.intervals.get(
            dimension,
            [],
        )

    def count(
        self,
        dimension: int,
    ) -> int:
        """Return the number of persistence intervals."""

        return len(
            self.intervals_for(dimension)
        )


def compute_persistence(
    simplex_filtration: list[tuple[tuple[int, ...], float]],
) -> PersistenceResult:
    """Compute persistent homology from a filtered simplicial complex.

    Parameters
    ----------
    simplex_filtration:
        List containing pairs of:

        ``(simplex, filtration_value)``

        where ``simplex`` is a tuple of vertex indices.

    Returns
    -------
    PersistenceResult
        Persistence intervals grouped by homological dimension.
    """

    if not simplex_filtration:
        raise ValueError(
            "simplex_filtration cannot be empty."
        )

    complex_ = gudhi.SimplexTree()

    for simplex, filtration_value in simplex_filtration:
        if not simplex:
            raise ValueError(
                "A simplex cannot be empty."
            )

        if filtration_value < 0:
            raise ValueError(
                "filtration values must be non-negative."
            )

        complex_.insert(
            simplex,
            filtration=filtration_value,
        )

    complex_.make_filtration_non_decreasing()

    persistence = complex_.persistence()

    intervals: dict[
        int,
        list[tuple[float, float]]
    ] = {}

    for dimension, pair in persistence:
        birth, death = pair

        intervals.setdefault(
            dimension,
            [],
        ).append(
            (
                float(birth),
                float(death),
            )
        )

    return PersistenceResult(
        intervals=intervals
    )
