"""Metrics for Digital Map analysis."""

from __future__ import annotations

import numpy as np


def network_density(
    adjacency: np.ndarray,
) -> float:
    """Calculate weighted network density."""

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

    n_nodes = adjacency.shape[0]

    if n_nodes < 2:
        return 0.0

    upper_triangle = np.triu(
        adjacency,
        k=1,
    )

    return float(
        np.count_nonzero(upper_triangle)
        / (n_nodes * (n_nodes - 1) / 2)
    )


def mean_edge_weight(
    adjacency: np.ndarray,
) -> float:
    """Calculate the mean non-zero edge weight."""

    adjacency = np.asarray(
        adjacency,
        dtype=float,
    )

    if adjacency.ndim != 2:
        raise ValueError(
            "adjacency must be two-dimensional."
        )

    upper_triangle = np.triu(
        adjacency,
        k=1,
    )

    edges = upper_triangle[
        upper_triangle > 0
    ]

    if len(edges) == 0:
        return 0.0

    return float(
        np.mean(edges)
    )
