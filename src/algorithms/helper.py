from __future__ import annotations

# Standard Library Packages
from typing import Literal

# Local Project
from src.graph import Graph

# Local Folder
from .louvain import Louvain

COMMUNITY_DETECTION_ALGORITHM_MAPPING = {"louvain": Louvain()}
COMMUNITY_DETECTION_ALGORITHMS = list(COMMUNITY_DETECTION_ALGORITHM_MAPPING.keys())


def build_community(graph: Graph, algorithm: Literal[*COMMUNITY_DETECTION_ALGORITHMS]) -> Graph:
    if algorithm not in COMMUNITY_DETECTION_ALGORITHMS:
        raise ValueError(
            f"Chosen algorithm {algorithm} not available. Please try one of {COMMUNITY_DETECTION_ALGORITHMS} instead."
        )

    algo = COMMUNITY_DETECTION_ALGORITHM_MAPPING[algorithm]
    graph_with_community = algo.build_communities(graph=graph, verbose=True)
    return graph_with_community
