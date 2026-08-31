"""Visualization utilities for the Digital Map."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

from .map import DigitalMap
from .metrics import network_density


def plot_network_density(
    digital_map: DigitalMap,
) -> tuple[plt.Figure, plt.Axes]:
    """Plot network density through time."""

    times: list[float] = []
    densities: list[float] = []

    for snapshot in digital_map.snapshots:
        if snapshot.adjacency is None:
            continue

        times.append(snapshot.time)

        densities.append(
            network_density(
                snapshot.adjacency
            )
        )

    if not times:
        raise ValueError(
            "Digital Map contains no network data."
        )

    figure, axes = plt.subplots()

    axes.plot(
        np.asarray(times),
        np.asarray(densities),
        marker="o",
    )

    axes.set_xlabel("Time")
    axes.set_ylabel("Network density")
    axes.set_title(
        "Dynamic Network Density"
    )

    axes.grid(True)

    figure.tight_layout()

    return figure, axes
