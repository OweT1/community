from dataclasses import dataclass
from typing import List, Union

from loguru import logger

@dataclass(frozen=True)
class Node:
  id: Union[int, str]
  
@dataclass(frozen=True)
class Edge:
  node1: Node
  node2: Node
  weight: Union[int, float]

  def __eq__(self, other):
    return isinstance(other, Edge) and \
    (
      (self.node1 == other.node1 and self.node2 == other.node2) or
      (self.node1 == other.node2 and self.node2 == other.node1)
    ) and \
    self.weight == other.weight

class Graph:
  def __init__(self, nodes: List[Node], edges: List[Edge]):
    self.nodes = nodes
    self.edges = edges

    self._build_initial()

  def _build_initial(self):
    self._build_initial_communities()
    self._build_edge_mapping()
    
  def _build_initial_communities(self):
    community_mapping = {}
    for node in self.nodes:
      node_id = node.id
      community_mapping[node] = node_id
    self.community_mapping = community_mapping
    
  def _build_edge_mapping(self):
    def _is_valid_edge(edge: Edge):
      node1, node2 = edge.node1, edge.node2
      if node1 not in self.nodes or node2 not in self.nodes or node1 == node2:
        logger.info("Node {} not in nodes list. Skipping...")
        return False
      return True
    
    graph_total_edge_weight = 0
    node_edge_weight_mapping, adjacency_mapping = {}, {}
    for edge in self.edges:
      if _is_valid_edge(edge):
        node1, node2, weight = edge.node1, edge.node2, edge.weight
        node1_id = node1.id
        
        # Mapping for Adjacency matrix
        if node1 not in adjacency_mapping:
          adjacency_mapping[node1] = {}
        adjacency_mapping[node1][node2] = weight
        
        if node2 not in adjacency_mapping:
          adjacency_mapping[node2] = {}
        adjacency_mapping[node2][node1] = weight
        
        # Mapping for total edge weight for each node
        node_edge_weight_mapping[node1] = node_edge_weight_mapping.get(node1, 0) + weight
        node_edge_weight_mapping[node2] = node_edge_weight_mapping.get(node2, 0) + weight
        
        # Sum of total edge weight in graph
        graph_total_edge_weight += weight

    self.adjacency_mapping = adjacency_mapping
    self.node_edge_weight_mapping = node_edge_weight_mapping
    self.graph_total_edge_weight = graph_total_edge_weight

  def __repr__(self):
    return f"Graph(nodes={self.nodes}, edges={self.edges})"
