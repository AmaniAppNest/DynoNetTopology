"""Dynamic network representation."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class NetworkState:
    """Network representation at a single point in time."""

    time: float
    adjacency: np.ndarray

    def __post_init__(self) -> None:
        """Validate the network state."""

        self.time = float(self.time)

        self.adjacency = np.asarray(
            self.adjacency,
            dtype=float,
        )

        if self.adjacency.ndim != 2:
            raise ValueError(
                "adjacency must be a two-dimensional array."
            )

        if (
            self.adjacency.shape[0]
            != self.adjacency.shape[1]
        ):
            raise ValueError(
                "adjacency must be a square matrix."
            )

        if not np.all(
            np.isfinite(self.adjacency)
        ):
            raise ValueError(
                "adjacency must contain finite values."
            )

    @property
    def n_nodes(self) -> int:
        """Return the number of network nodes."""

        return self.adjacency.shape[0]

    def copy(self) -> "NetworkState":
        """Return an independent copy of the network state."""

        return NetworkState(
            time=self.time,
            adjacency=self.adjacency.copy(),
        )


@dataclass
class DynamicNetwork:
    """Time-ordered collection of network states."""

    states: list[NetworkState]

    def __post_init__(self) -> None:
        """Validate temporal ordering."""

        if not self.states:
            raise ValueError(
                "DynamicNetwork requires at least one state."
            )

        times = [
            state.time
            for state in self.states
        ]

        if times != sorted(times):
            raise ValueError(
                "Network states must be ordered by time."
            )

    @property
    def n_nodes(self) -> int:
        """Return the number of nodes."""

        return self.states[0].n_nodes

    @property
    def times(self) -> np.ndarray:
        """Return all network-state times."""

        return np.asarray(
            [state.time for state in self.states],
            dtype=float,
        )

    @property
    def adjacency_matrices(self) -> list[np.ndarray]:
        """Return adjacency matrices in temporal order."""

        return [
            state.adjacency
            for state in self.states
        ]

    def add_state(
        self,
        state: NetworkState,
    ) -> None:
        """Append a new network state."""

        if state.n_nodes != self.n_nodes:
            raise ValueError(
                "All network states must have the same "
                "number of nodes."
            )

        if state.time < self.states[-1].time:
            raise ValueError(
                "New network state cannot move backward in time."
            )

        self.states.append(state)
