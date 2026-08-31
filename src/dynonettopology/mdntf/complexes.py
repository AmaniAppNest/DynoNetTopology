"""Simplicial-complex construction from network states."""

from __future__ import annotations

from dataclasses import dataclass

import networkx as nx
import numpy as np


@dataclass
class SimplicialComplex:
    """Simple representation of a finite simplicial complex."""

    simplices: dict[int, list[tuple[int, ...]]]

    @property
    def dimensions(self) -> list[int]:
        """Return the dimensions present in the complex."""

        return sorted(self.simplices.keys())

    def count(self, dimension: int) -> int:
        """Return the number of simplices of a given dimension."""

        return len(
            self.simplices.get(dimension, [])
        )


def clique_complex(
    adjacency: np.ndarray,
    max_dimension: int = 2,
) -> SimplicialComplex:
    """Construct a clique complex from an adjacency matrix.

    Parameters
    ----------
    adjacency:
        Square weighted adjacency matrix. Non-zero entries
        represent graph edges.

    max_dimension:
        Maximum simplex dimension to construct.

    Returns
    -------
    SimplicialComplex
        The clique complex represented by simplex dimension.
    """

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

    if not np.all(
        np.isfinite(adjacency)
    ):
        raise ValueError(
            "adjacency must contain finite values."
        )

    if max_dimension < 0:
        raise ValueError(
            "max_dimension must be non-negative."
        )

    graph = nx.Graph()

    n_nodes = adjacency.shape[0]

    graph.add_nodes_from(
        range(n_nodes)
    )

    for i in range(n_nodes):
        for j in range(i + 1, n_nodes):
            if adjacency[i, j] > 0:
                graph.add_edge(i, j)

    simplices: dict[int, list[tuple[int, ...]]] = {
        0: [
            (node,)
            for node in graph.nodes
        ]
    }

    if max_dimension == 0:
        return SimplicialComplex(
            simplices=simplices
        )

    for clique in nx.enumerate_all_cliques(graph):
        dimension = len(clique) - 1

        if dimension == 0:
            continue

        if dimension > max_dimension:
            break

        simplex = tuple(
            sorted(clique)
        )

        simplices.setdefault(
            dimension,
            [],
        ).append(simplex)

    return SimplicialComplex(
        simplices=simplices
    )
