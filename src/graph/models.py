from typing import List, Union

from loguru import logger

class Node:
  def __init__(self, id: Union[int, str]):
    self.id = id
    
  def _get_id(self):
    return self.id
  
  def __repr__(self):
    return f"Node(id={self.id})"
    
class Edge:
  def __init__(self, node1: Node, node2: Node, weight: int = 1):
    self.node1 = node1
    self.node2 = node2
    self.weight = weight

  def _get_node1(self):
    return self.node1
  
  def _get_node2(self):
    return self.node2
  
  def _get_weight(self):
    return self.weight
  
  def __repr__(self):
    return f"Edge(node1={self.node1}, node2={self.node2}, weight={self.weight})"

class Graph:
  def __init__(self, nodes: List[Node], edges: List[Edge]):
    self.nodes = nodes
    self.edges = edges

    self._build_edge_mapping()
    
  def _build_edge_mapping(self):
    def _is_valid_edge(edge: Edge):
      node1, node2 = edge._get_node1(), edge._get_node2()
      if node1 not in self.nodes or node2 not in self.nodes:
        logger.info("Node {} not in nodes list. Skipping...")
        return False
      return True
      
    edge_mapping = {}
    for edge in edges:
      if _is_valid_edge(edge):
        node1, node2, weight = edge._get_node1(), edge._get_node2(), edge._get_weight()
        edge_mapping[node1] = weight
        edge_mapping[node2] = weight
    self.edge_mapping = edge_mapping
    
  def __repr__(self):
    return f"Graph(nodes={self.nodes}, edges={self.edges})"
