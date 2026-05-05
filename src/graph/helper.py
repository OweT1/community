from __future__ import annotations

# Standard Library Packages
from typing import Dict, List, Set, Union

# Third Party Packages
import networkx as nx

# Local Folder
from .models import Graph, Node


def convert_custom_to_networkx_graph(graph: Graph) -> nx.Graph:
    G = nx.Graph()

    for edge in graph.edges:
        node1, node2, weight = edge.node1, edge.node2, edge.weight
        G.add_nodes_from([node1.id, node2.id])
        G.add_edge(node1.id, node2.id, edge_weight=weight)

    return G


def convert_community_mapping_to_sets(
    community_mapping: Dict[Node, Node],
) -> List[Set[Union[int, str]]]:
    parent_child_mapping = {}
    for child, parent in community_mapping.items():
        child_id, parent_id = child.id, parent.id
        if parent_id not in parent_child_mapping:
            parent_child_mapping[parent_id] = set()
        parent_child_mapping[parent_id].add(child_id)
    return list(parent_child_mapping.values())
