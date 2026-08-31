"""First end-to-end DynoNetTopology demonstration."""

from __future__ import annotations

import numpy as np

from dynonettopology.fields import SyntheticMagneticField
from dynonettopology.networks import (
    DynamicNetwork,
    NetworkState,
    correlation_adjacency,
)
from dynonettopology.sensors.nv import (
    NVSensoryArray,
)
from dynonettopology.mdntf import (
    MDNTFEngine,
)
from dynonettopology.digital_map import (
    DigitalMap,
    DigitalMapSnapshot,
)


def create_sensor_array() -> NVSensoryArray:
    """Create a small linear NV sensor array."""

    return NVSensoryArray.create_linear(
        n_sensors=8,
        spacing=1.0,
    )


def generate_measurements(
    sensor_array: NVSensoryArray,
    field_model: SyntheticMagneticField,
    times: np.ndarray,
) -> np.ndarray:
    """Generate synthetic NV sensor measurements."""

    measurements = []

    state = np.ones(
        8,
        dtype=float,
    )
    for time in times:
        magnetic_field = field_model.evaluate(
            sensor_array.positions,
            state,
            float(time),
        )

        sensor_measurements = (
            sensor_array.measure(
                magnetic_field
            )
        )

        measurements.append(
            sensor_measurements
        )

    return np.asarray(
        measurements,
        dtype=float,
    )


def build_dynamic_network(
    measurements: np.ndarray,
    times: np.ndarray,
) -> DynamicNetwork:
    """Build a time-dependent interaction network."""

    states: list[NetworkState] = []

    for index, time in enumerate(times):
        start = max(
            0,
            index - 4,
        )

        window = measurements[
            start : index + 1
        ]

        if len(window) < 2:
            continue

        adjacency = correlation_adjacency(
            window,
            absolute=True,
        )

        states.append(
            NetworkState(
                time=float(time),
                adjacency=adjacency,
            )
        )

    return DynamicNetwork(
        states=states
    )


def analyze_network(
    network: DynamicNetwork,
) -> list:
    """Run MDNTF analysis over network states."""

    engine = MDNTFEngine(
        thresholds=[
            0.2,
            0.4,
            0.6,
            0.8,
        ],
        max_dimension=2,
    )

    results = []

    for state in network.states:
        result = engine.analyze_adjacency(
            state.adjacency,
            state.time,
        )

        results.append(
            result
        )

    return results


def build_digital_map(
    network: DynamicNetwork,
    mdntf_results: list,
) -> DigitalMap:
    """Combine network and topological results."""

    digital_map = DigitalMap()

    for state, result in zip(
        network.states,
        mdntf_results,
    ):
        betti_numbers = {}

        for persistence_result in (
            result.persistence
        ):
            for dimension in (
                persistence_result.intervals
            ):
                betti_numbers[dimension] = (
                    persistence_result.count(
                        dimension
                    )
                )

        digital_map.add_snapshot(
            DigitalMapSnapshot(
                time=state.time,
                adjacency=state.adjacency,
                betti_numbers=betti_numbers,
            )
        )

    return digital_map


def main() -> None:
    """Run the complete demonstration."""

    times = np.linspace(
        0.0,
        2.0,
        21,
    )

    sensor_array = create_sensor_array()

    field_model = SyntheticMagneticField(
        coupling=1.0
    )

    measurements = generate_measurements(
        sensor_array,
        field_model,
        times,
    )

    network = build_dynamic_network(
        measurements,
        times,
    )

    mdntf_results = analyze_network(
        network
    )

    digital_map = build_digital_map(
        network,
        mdntf_results,
    )

    print(
        "DynoNetTopology pipeline completed."
    )

    print(
        f"Sensor measurements: "
        f"{measurements.shape}"
    )

    print(
        f"Network states: "
        f"{len(network.states)}"
    )

    print(
        f"Digital Map snapshots: "
        f"{digital_map.n_snapshots}"
    )


if __name__ == "__main__":
    main()