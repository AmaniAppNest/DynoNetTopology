"""Construction of interaction networks from sensor measurements."""

from __future__ import annotations

import numpy as np


def correlation_adjacency(
    measurements: np.ndarray,
    absolute: bool = True,
) -> np.ndarray:
    """Construct an adjacency matrix from sensor time series.

    Parameters
    ----------
    measurements:
        Sensor measurements with shape
        ``(n_time_points, n_nodes)``.

    absolute:
        If True, use the absolute value of the correlation.
        If False, preserve positive and negative correlations.

    Returns
    -------
    numpy.ndarray
        Symmetric adjacency matrix with shape
        ``(n_nodes, n_nodes)``.
    """

    measurements = np.asarray(
        measurements,
        dtype=float,
    )

    if measurements.ndim != 2:
        raise ValueError(
            "measurements must be a two-dimensional array."
        )

    n_time_points, n_nodes = measurements.shape

    if n_time_points < 2:
        raise ValueError(
            "At least two time points are required."
        )

    if n_nodes < 2:
        raise ValueError(
            "At least two nodes are required."
        )

    if not np.all(
        np.isfinite(measurements)
    ):
        raise ValueError(
            "measurements must contain finite values."
        )

    adjacency = np.corrcoef(
        measurements,
        rowvar=False,
    )

    if absolute:
        adjacency = np.abs(adjacency)

    np.fill_diagonal(
        adjacency,
        0.0,
    )

    return adjacency


def threshold_adjacency(
    adjacency: np.ndarray,
    threshold: float,
) -> np.ndarray:
    """Remove edges below a chosen interaction threshold."""

    adjacency = np.asarray(
        adjacency,
        dtype=float,
    )

    if adjacency.ndim != 2:
        raise ValueError(
            "adjacency must be a two-dimensional array."
        )

    if (
        adjacency.shape[0]
        != adjacency.shape[1]
    ):
        raise ValueError(
            "adjacency must be square."
        )

    if threshold < 0:
        raise ValueError(
            "threshold must be non-negative."
        )

    result = adjacency.copy()

    result[result < threshold] = 0.0

    np.fill_diagonal(
        result,
        0.0,
    )

    return result
