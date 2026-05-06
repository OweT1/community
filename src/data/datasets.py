from __future__ import annotations

# Standard Library Packages
from functools import lru_cache
from typing import Dict, Optional

# Local Project
from src.graph import Edge, Node

# Local Folder
from .models import Dataset


@lru_cache(maxsize=1)
def get_datasets() -> Dict[int, Dataset]:
    n1 = Node(1)
    n2 = Node(2)
    n3 = Node(3)
    n4 = Node(4)
    n5 = Node(5)
    n6 = Node(6)
    n7 = Node(7)
    n8 = Node(8)
    n9 = Node(9)
    n10 = Node(10)

    e1 = Edge(n1, n2, 3)
    e2 = Edge(n2, n3, 5)
    e3 = Edge(n3, n4, 2)
    e4 = Edge(n4, n5, 8)
    e5 = Edge(n5, n6, 2)
    e6 = Edge(n4, n6, 9)
    e7 = Edge(n4, n7, 3)
    e8 = Edge(n7, n8, 2)
    e9 = Edge(n7, n9, 7)
    e10 = Edge(n5, n9, 1)
    e11 = Edge(n10, n8, 6)

    def _get_dataset1() -> Dataset:
        nodes = [n1, n2, n3, n4, n5, n6]
        edges = [e1, e2, e3, e4, e5, e6]
        return Dataset(nodes=nodes, edges=edges)

    def _get_dataset2() -> Dataset:
        nodes = [n1, n2, n3, n4, n5, n6, n7, n8, n9, n10]
        edges = [e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11]
        return Dataset(nodes=nodes, edges=edges)

    return {
        1: _get_dataset1(),
        2: _get_dataset2(),
    }


def get_dataset(dataset_id: int) -> Optional[Dataset]:
    datasets = get_datasets()
    if dataset_id in datasets:
        return datasets[dataset_id]
    else:
        raise ValueError(
            f"Dataset of id {dataset_id} not found. Please use any of: {list(datasets.keys())}"
        )
