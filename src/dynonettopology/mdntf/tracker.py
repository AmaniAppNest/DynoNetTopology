"""Temporal tracking of topological features."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TopologicalFeature:
    """A topological feature observed at one time."""

    time: float
    dimension: int
    birth: float
    death: float

    @property
    def lifetime(self) -> float:
        """Return the persistence lifetime of the feature."""

        if self.death == float("inf"):
            return float("inf")

        return self.death - self.birth


@dataclass
class FeatureTrajectory:
    """Temporal trajectory of a topological feature."""

    feature_id: int
    features: list[TopologicalFeature]

    @property
    def start_time(self) -> float:
        """Return the first time of the trajectory."""

        if not self.features:
            raise ValueError(
                "Feature trajectory is empty."
            )

        return self.features[0].time

    @property
    def end_time(self) -> float:
        """Return the final time of the trajectory."""

        if not self.features:
            raise ValueError(
                "Feature trajectory is empty."
            )

        return self.features[-1].time

    @property
    def duration(self) -> float:
        """Return the temporal duration of the trajectory."""

        return self.end_time - self.start_time

    def add_feature(
        self,
        feature: TopologicalFeature,
    ) -> None:
        """Append a feature observation in time order."""

        if self.features:
            if feature.time < self.features[-1].time:
                raise ValueError(
                    "Features must be added in temporal order."
                )

        self.features.append(feature)


class FeatureTracker:
    """Manage temporal topological feature trajectories."""

    def __init__(self) -> None:
        self.trajectories: list[FeatureTrajectory] = []

    def create_trajectory(
        self,
        feature: TopologicalFeature,
    ) -> FeatureTrajectory:
        """Create a new feature trajectory."""

        trajectory = FeatureTrajectory(
            feature_id=len(self.trajectories),
            features=[feature],
        )

        self.trajectories.append(
            trajectory
        )

        return trajectory

    def add_observation(
        self,
        trajectory: FeatureTrajectory,
        feature: TopologicalFeature,
    ) -> None:
        """Add a new observation to an existing trajectory."""

        trajectory.add_feature(
            feature
        )

    def all_trajectories(
        self,
    ) -> list[FeatureTrajectory]:
        """Return all tracked feature trajectories."""

        return list(
            self.trajectories
        )
