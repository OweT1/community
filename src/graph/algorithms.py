from typing import Union

from src.graph import Graph

# --- Louvain Algorithm --- #
def calculate_modularity(
  m: Union[int, float],
  nodes: list[Node],
  adjacency_matrix: dict[Node, dict[Node, Union[int, float]]],
  node_edge_weight_mapping: dict[Node, Union[int, float]],
  community_mapping: dict[Node, Union[int, str]]
) -> float:
  Q = 0
  for i in range(len(nodes)):
    for j in range(len(nodes)):
      node_i, node_j = nodes[i], nodes[j]
      
      Aij = adjacency_matrix[node1][node2]
      ki = node_edge_weight_mapping[node1]
      kj = node_edge_weight_mapping[node2]
      kronecker_delta = community_mapping[node1] == communty_mapping[node2]
      
      Q += (Aij - (ki*kj)/(2*m)) * kronecker_delta

  return Q / (2*m)

def calculate_max_modularity(
  node: Node,
  m: Union[int, float],
  nodes: list[Node],
  adjacency_matrix: dict[Node, dict[Node, Union[int, float]]],
  node_edge_weight_mapping: dict[Node, Union[int, float]],
  community_mapping: dict[Node, Union[int, str]]
):
  max_Q, best_node = float('-inf'), None
  for other in nodes:
    if node != other: # only calculate modularity if not the same node
      new_community_mapping = {
        **community_mapping,
        other: node.id
      }
      curr_Q = calculate_modularity(
        m=m,
        nodes=nodes,
        adjacency_matrix=adjacency_matrix,
        node_edge_weight_mapping=node_edge_weight_mapping,
        community_mapping=new_community_mapping
      )
      if curr_Q > max_Q:
        max_Q = curr_Q
        best_node = other
  
  if max_Q > 0:
    community_mapping.update({best_node: node.id})
  return community_mapping
