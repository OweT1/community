# Standard Library Packages
from typing import Dict, List, Union

# Third Party Packages
from loguru import logger

# Local Project
from src.graph import Edge, Graph, Node


# --- Phase 1 --- #
def calculate_modularity(
    m: Union[int, float],
    nodes: list[Node],
    adjacency_matrix: Dict[Node, Dict[Node, Union[int, float]]],
    node_edge_weight_mapping: Dict[Node, Union[int, float]],
    community_mapping: Dict[Node, Node],
) -> float:
    Q = 0
    for i in range(len(nodes)):
        for j in range(len(nodes)):
            node_i, node_j = nodes[i], nodes[j]

            Aij = adjacency_matrix.get(node_i, {}).get(node_j, 0)
            ki = node_edge_weight_mapping[node_i]
            kj = node_edge_weight_mapping[node_j]
            kronecker_delta = community_mapping[node_i] == community_mapping[node_j]

            Q += (Aij - (ki * kj) / (2 * m)) * kronecker_delta

    return Q / (2 * m)


def get_node_best_community(
    node: Node,
    m: Union[int, float],
    nodes: list[Node],
    adjacency_matrix: Dict[Node, Dict[Node, Union[int, float]]],
    node_edge_weight_mapping: Dict[Node, Union[int, float]],
    community_mapping: Dict[Node, Node],
) -> Union[Node, None]:
    max_delta_Q, best_node = float("-inf"), None
    for other in nodes:
        if (
            node != other and other in adjacency_matrix[node]
        ):  # only calculate modularity if not the same node
            new_community_mapping = {**community_mapping, other: node}
            old_Q = calculate_modularity(
                m=m,
                nodes=nodes,
                adjacency_matrix=adjacency_matrix,
                node_edge_weight_mapping=node_edge_weight_mapping,
                community_mapping=community_mapping,
            )

            new_Q = calculate_modularity(
                m=m,
                nodes=nodes,
                adjacency_matrix=adjacency_matrix,
                node_edge_weight_mapping=node_edge_weight_mapping,
                community_mapping=new_community_mapping,
            )

            delta_Q = new_Q - old_Q
            if delta_Q > max_delta_Q:
                max_delta_Q = delta_Q
                best_node = other
    return best_node if max_delta_Q > 0 else None


def get_and_update_node_best_community(
    node: Node,
    m: Union[int, float],
    nodes: list[Node],
    adjacency_matrix: Dict[Node, Dict[Node, Union[int, float]]],
    node_edge_weight_mapping: Dict[Node, Union[int, float]],
    community_mapping: Dict[Node, Node],
) -> Dict[Node, Node]:
    best_node = get_node_best_community(
        node=node,
        m=m,
        nodes=nodes,
        adjacency_matrix=adjacency_matrix,
        node_edge_weight_mapping=node_edge_weight_mapping,
        community_mapping=community_mapping,
    )
    if best_node is not None:
        community_mapping.update({best_node: node})
    return community_mapping


def optimise_modularity(graph: Graph) -> Dict[Node, Node]:
    m = graph.graph_total_edge_weight
    nodes = graph.nodes
    adjacency_matrix = graph.adjacency_matrix
    node_edge_weight_mapping = graph.node_edge_weight_mapping
    community_mapping = graph.community_mapping

    new_community_mapping = {**community_mapping}
    for node in nodes:
        new_community_mapping = get_and_update_node_best_community(
            node=node,
            m=m,
            nodes=nodes,
            adjacency_matrix=adjacency_matrix,
            node_edge_weight_mapping=node_edge_weight_mapping,
            community_mapping=new_community_mapping,
        )
    return new_community_mapping


# --- Phase 2 --- #
def get_root_parent(node: Node, community_mapping: Dict[Node, Node]) -> Node:
    c = community_mapping[node]
    while c != community_mapping[node]:
        c = community_mapping[node]
    return c


def clean_community_mapping(community_mapping: Dict[Node, Node]) -> Dict[Node, Node]:
    """Generate a clean community mapping - The keys are the nodes, values are the parent community nodes."""
    new_mapping = {}
    for child in community_mapping.keys():
        parent = get_root_parent(child, community_mapping)
        new_mapping[child] = parent
    return new_mapping


def aggregate_communities(graph: Graph, new_community_mapping: Dict[Node, Node]) -> Graph:
    cleaned_community_mapping = clean_community_mapping(new_community_mapping)

    new_nodes: list[Node] = sorted(list(cleaned_community_mapping.values()))

    graph_edges = graph.edges
    new_edges_mapping = {}
    for edge in graph_edges:
        node1, node2, weight = edge.node1, edge.node2, edge.weight
        c1 = cleaned_community_mapping[node1]
        c2 = cleaned_community_mapping[node2]
        sorted_key = tuple(sorted([c1, c2]))
        new_edges_mapping[sorted_key] = new_edges_mapping.get(sorted_key, 0) + weight

    new_edges = [
        Edge(node1=nodes[0], node2=nodes[1], weight=weight)
        for nodes, weight in new_edges_mapping.items()
    ]
    return Graph(nodes=new_nodes, edges=new_edges)


# --- Main Algorithm --- #
def louvain(graph: Graph, verbose=True):
    if verbose:
        i = 1
        logger.info(f"Started {i} iteration...")

    old_community_mapping = graph.community_mapping
    new_community_mapping = optimise_modularity(graph)

    new_graph: Graph | None = None
    community_mapping_deltas: List[Dict[Node, Node]] = []
    while old_community_mapping != new_community_mapping:
        if verbose:
            logger.info("Old Community Mapping: {}", old_community_mapping)
            logger.info("New Community Mapping: {}", new_community_mapping)
            i += 1
            logger.info(f"Started {i} iteration...")

        # Repeat Phase 1 and 2 till no change in communities
        old_community_mapping = new_community_mapping
        community_mapping_deltas.append(old_community_mapping)

        if new_graph is None:
            new_graph = aggregate_communities(graph, old_community_mapping)
        else:
            new_graph = aggregate_communities(new_graph, old_community_mapping)
        new_community_mapping = optimise_modularity(new_graph)

    output_community_mapping = graph.community_mapping
    for map_delta in community_mapping_deltas:
        for key, val in output_community_mapping.items():
            new_val = map_delta.get(val)
            if new_val:
                output_community_mapping[key] = new_val
    return output_community_mapping
