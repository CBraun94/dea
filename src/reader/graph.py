from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class Node:
    id: str
    label: Optional[str] = None
    shape: Optional[str] = None


@dataclass
class Edge:
    source: str
    target: str
    label: Optional[str] = None


@dataclass
class Flowchart:
    direction: str
    nodes: Dict[str, Node]
    edges: List[Edge]
