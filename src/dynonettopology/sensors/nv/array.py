"""NV-center sensor arrays."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .sensor import NVSensor


@dataclass
class NVSensoryArray:
    """Collection of NV-center sensors."""

    sensors: list[NVSensor]

    def __post_init__(self) -> None:
        """Validate the sensor collection."""

        if not self.sensors:
            raise ValueError(
                "The sensor array must contain at least one sensor."
            )

    @property
    def positions(self) -> np.ndarray:
        """Return sensor positions as an array."""

        return np.asarray(
            [sensor.position for sensor in self.sensors],
            dtype=float,
        )

    @property
    def orientations(self) -> np.ndarray:
        """Return sensor orientations as an array."""

        return np.asarray(
            [sensor.orientation for sensor in self.sensors],
            dtype=float,
        )

    def measure(
        self,
        magnetic_field: np.ndarray,
    ) -> np.ndarray:
        """Project magnetic fields onto each sensor's NV axis.

        Parameters
        ----------
        magnetic_field:
            Magnetic-field vectors with shape
            ``(n_sensors, 3)``.

        Returns
        -------
        numpy.ndarray
            One scalar measurement per sensor.
        """

        magnetic_field = np.asarray(
            magnetic_field,
            dtype=float,
        )

        expected_shape = (
            len(self.sensors),
            3,
        )

        if magnetic_field.shape != expected_shape:
            raise ValueError(
                "magnetic_field must have shape "
                f"{expected_shape}, got "
                f"{magnetic_field.shape}."
            )

        return np.asarray(
            [
                sensor.project_field(field)
                for sensor, field in zip(
                    self.sensors,
                    magnetic_field,
                )
            ],
            dtype=float,
        )

    @classmethod
    def create_linear(
        cls,
        n_sensors: int = 16,
        spacing: float = 1.0,
    ) -> "NVSensoryArray":
        """Create a simple linear sensor array.

        All sensors initially point along the z-axis.
        """

        if n_sensors < 1:
            raise ValueError(
                "n_sensors must be at least 1."
            )

        if spacing <= 0:
            raise ValueError(
                "spacing must be positive."
            )

        sensors = []

        for index in range(n_sensors):
            position = np.array(
                [index * spacing, 0.0, 0.0],
                dtype=float,
            )

            orientation = np.array(
                [0.0, 0.0, 1.0],
                dtype=float,
            )

            sensors.append(
                NVSensor(
                    position=position,
                    orientation=orientation,
                )
            )

        return cls(sensors=sensors)
