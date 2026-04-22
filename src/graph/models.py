# Standard Library Packages
from dataclasses import dataclass
from typing import Dict, List, Union

# Third Party Packages
from loguru import logger


@dataclass(order=True, frozen=True)
class Node:
    id: Union[int, str]


@dataclass(order=True, frozen=True)
class Edge:
    node1: Node
    node2: Node
    weight: Union[int, float]

    def __eq__(self, other):
        return (
            isinstance(other, Edge)
            and (
                (self.node1 == other.node1 and self.node2 == other.node2)
                or (self.node1 == other.node2 and self.node2 == other.node1)
            )
            and self.weight == other.weight
        )


class Graph:
    def __init__(
        self,
        nodes: List[Node],
        edges: List[Edge],
        community_mapping: Union[Dict[Node, Node], None] = None,
    ):
        self.nodes = nodes
        self.edges = edges
        self.community_mapping = community_mapping

        self._build_initial()

    def _build_initial(self):
        if self.community_mapping is None:
            self._build_initial_communities()
        self._build_edge_mapping()

    def _build_initial_communities(self):
        community_mapping = {}
        for node in self.nodes:
            community_mapping[node] = node
        self.community_mapping = community_mapping

    def _build_edge_mapping(self):
        def _is_valid_edge(edge: Edge):
            node1, node2 = edge.node1, edge.node2
            if node1 not in self.nodes or node2 not in self.nodes:
                logger.info("Node {} not in nodes list. Skipping...")
                return False
            return True

        graph_total_edge_weight = 0
        node_edge_weight_mapping, adjacency_matrix = {}, {}
        for edge in self.edges:
            if _is_valid_edge(edge):
                node1, node2, weight = edge.node1, edge.node2, edge.weight

                # Mapping for Adjacency matrix
                if node1 not in adjacency_matrix:
                    adjacency_matrix[node1] = {}
                adjacency_matrix[node1][node2] = weight

                if node2 not in adjacency_matrix:
                    adjacency_matrix[node2] = {}
                adjacency_matrix[node2][node1] = weight

                # Mapping for total edge weight for each node
                if node1 == node2:  # for `aggregate_communities`, where edge.node1 == edge.node2
                    node_edge_weight_mapping[node1] = (
                        node_edge_weight_mapping.get(node1, 0) + weight
                    )
                else:  # as per normal
                    node_edge_weight_mapping[node1] = (
                        node_edge_weight_mapping.get(node1, 0) + weight
                    )
                    node_edge_weight_mapping[node2] = (
                        node_edge_weight_mapping.get(node2, 0) + weight
                    )

                # Sum of total edge weight in graph
                graph_total_edge_weight += weight

        self.adjacency_matrix = adjacency_matrix
        self.node_edge_weight_mapping = node_edge_weight_mapping
        self.graph_total_edge_weight = graph_total_edge_weight

    def __repr__(self):
        return f"Graph(nodes={self.nodes}, edges={self.edges})"
