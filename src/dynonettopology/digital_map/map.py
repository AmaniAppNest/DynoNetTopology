"""Digital Map representation of an evolving system."""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np


@dataclass
class DigitalMapSnapshot:
    """System representation at one point in time."""

    time: float
    physical_state: np.ndarray | None = None
    adjacency: np.ndarray | None = None
    betti_numbers: dict[int, int] = field(
        default_factory=dict
    )

    def __post_init__(self) -> None:
        """Validate snapshot data."""

        self.time = float(self.time)

        if self.physical_state is not None:
            self.physical_state = np.asarray(
                self.physical_state,
                dtype=float,
            )

        if self.adjacency is not None:
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


@dataclass
class DigitalMap:
    """Time-dependent Digital Map of the system."""

    snapshots: list[DigitalMapSnapshot] = field(
        default_factory=list
    )

    def add_snapshot(
        self,
        snapshot: DigitalMapSnapshot,
    ) -> None:
        """Add a snapshot while preserving time order."""

        if self.snapshots:
            if snapshot.time < self.snapshots[-1].time:
                raise ValueError(
                    "Snapshots must be added in temporal order."
                )

        self.snapshots.append(
            snapshot
        )

    @property
    def times(self) -> np.ndarray:
        """Return snapshot times."""

        return np.asarray(
            [
                snapshot.time
                for snapshot in self.snapshots
            ],
            dtype=float,
        )

    @property
    def n_snapshots(self) -> int:
        """Return the number of snapshots."""

        return len(self.snapshots)

    def latest(
        self,
    ) -> DigitalMapSnapshot:
        """Return the latest snapshot."""

        if not self.snapshots:
            raise ValueError(
                "Digital Map contains no snapshots."
            )

        return self.snapshots[-1]
