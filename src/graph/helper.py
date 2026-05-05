from __future__ import annotations

# Third Party Packages
import networkx as nx

# Local Folder
from .models import Graph


def convert_custom_to_networkx_graph(graph: Graph) -> nx.Graph:
    G = nx.Graph()

    for edge in graph.edges:
        node1, node2, weight = edge.node1, edge.node2, edge.weight
        G.add_nodes_from([node1.id, node2.id])
        G.add_edge(node1.id, node2.id, edge_weight=weight)

    return G
