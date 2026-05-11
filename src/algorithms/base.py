from __future__ import annotations

# Standard Library Packages
from abc import ABC, abstractmethod

# Local Project
from src.graph import Graph


class CommunityDetectionAlgorithm(ABC):
    @abstractmethod
    def build_communities(self, graph: Graph, verbose: bool) -> Graph:
        pass
