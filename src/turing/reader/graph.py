from dataclasses import dataclass
from typing import Dict, List, Optional
import networkx as nx


@dataclass
class Node:
    id: str
    name: Optional[str] = None
    shape: Optional[str] = None
    docstring: Optional[str] = None


@dataclass
class Edge:
    source: str
    target: str
    name: Optional[str] = None
    docstring: Optional[str] = None


@dataclass
class Graph:
    nodes: Dict[str, Node]
    edges: List[Edge]
    direction: Optional[str] = None
    docstring: Optional[str] = None

    def __init__(self, nodes={}, edges=[]):
        self.nodes = nodes
        self.edges = edges


def graph_to_nx(graph: Graph) -> nx.Graph:
    G = nx.MultiDiGraph()

    for _g in graph.nodes:
        _n: Node = graph.nodes[_g]
        G.add_node(_n.id, name=_n.name, shape=_n.shape, docstring=_n.docstring, radius=10, size=10)

    for _edge in graph.edges:
        _e: Edge = _edge
        G.add_edge(_e.source, _e.target, name=_e.name, docstring=_e.docstring, weight=1.0)

    return G
