from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class Node:
    id: str
    name: Optional[str] = None
    shape: Optional[str] = None


@dataclass
class Edge:
    source: str
    target: str
    name: Optional[str] = None


@dataclass
class Graph:
    nodes: Dict[str, Node]
    edges: List[Edge]
    direction: Optional[str] = None

    def __init__(self, nodes={}, edges=[]):
        self.nodes = nodes
        self.edges = edges
