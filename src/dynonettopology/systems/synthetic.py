"""Synthetic dynamic systems for development and testing."""

from __future__ import annotations

import numpy as np

from .base import DynamicSystem


class CoupledOscillatorSystem(DynamicSystem):
    """Simple network of coupled dynamical nodes.

    The model is intentionally lightweight so that it can be used
    to validate the DynoNetTopology pipeline before introducing
    domain-specific physical models.
    """

    def __init__(
        self,
        n_nodes: int = 16,
        coupling: float = 0.2,
        damping: float = 0.1,
        seed: int | None = 42,
    ) -> None:
        if n_nodes < 2:
            raise ValueError("n_nodes must be at least 2.")

        if coupling < 0:
            raise ValueError("coupling must be non-negative.")

        if damping < 0:
            raise ValueError("damping must be non-negative.")

        self.n_nodes = n_nodes
        self.coupling = coupling
        self.damping = damping
        self.seed = seed

        self._rng = np.random.default_rng(seed)

        self._coupling_matrix = self._build_coupling_matrix()

    def _build_coupling_matrix(self) -> np.ndarray:
        """Create a symmetric nearest-neighbor coupling matrix."""

        matrix = np.zeros(
            (self.n_nodes, self.n_nodes),
            dtype=float,
        )

        for i in range(self.n_nodes - 1):
            matrix[i, i + 1] = self.coupling
            matrix[i + 1, i] = self.coupling

        return matrix

    def reset(
        self,
        state: np.ndarray | None = None,
    ) -> np.ndarray:
        """Return an initial state."""

        if state is not None:
            state = np.asarray(state, dtype=float)

            if state.shape != (self.n_nodes,):
                raise ValueError(
                    f"Expected state shape {(self.n_nodes,)}, "
                    f"got {state.shape}."
                )

            return state.copy()

        return self._rng.normal(
            loc=0.0,
            scale=1.0,
            size=self.n_nodes,
        )

    def step(
        self,
        state: np.ndarray,
        dt: float,
    ) -> np.ndarray:
        """Advance the system by one Euler integration step."""

        if dt <= 0:
            raise ValueError("dt must be positive.")

        state = np.asarray(state, dtype=float)

        if state.shape != (self.n_nodes,):
            raise ValueError(
                f"Expected state shape {(self.n_nodes,)}, "
                f"got {state.shape}."
            )

        interaction = (
            self._coupling_matrix @ state
            - np.sum(self._coupling_matrix, axis=1) * state
        )

        derivative = (
            -self.damping * state
            + interaction
        )

        return state + dt * derivative

    def observe(
        self,
        state: np.ndarray,
    ) -> np.ndarray:
        """Return observable node values."""

        state = np.asarray(state, dtype=float)

        if state.shape != (self.n_nodes,):
            raise ValueError(
                f"Expected state shape {(self.n_nodes,)}, "
                f"got {state.shape}."
            )

        return state.copy()
