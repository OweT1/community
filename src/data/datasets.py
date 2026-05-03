# Standard Library Packages
from functools import lru_cache

# Local Project
from src.graph import Edge, Node

from .models import Dataset


@lru_cache(maxsize=1)
def get_dataset1() -> Dataset:
    n1 = Node(1)
    n2 = Node(2)
    n3 = Node(3)
    n4 = Node(4)
    n5 = Node(5)
    n6 = Node(6)

    e1 = Edge(n1, n2, 3)
    e2 = Edge(n2, n3, 5)
    e3 = Edge(n3, n4, 1)
    e4 = Edge(n4, n5, 8)
    e5 = Edge(n5, n6, 2)
    e6 = Edge(n4, n6, 9)

    nodes = [n1, n2, n3, n4, n5, n6]
    edges = [e1, e2, e3, e4, e5, e6]
    return Dataset(nodes=nodes, edges=edges)


DATASET_1 = get_dataset1()
