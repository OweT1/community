from __future__ import annotations

# Standard Library Packages
from dataclasses import dataclass
from typing import List

# Local Project
from src.graph import Edge, Node


@dataclass
class Dataset:
    nodes: List[Node]
    edges: List[Edge]
