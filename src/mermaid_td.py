import re
from dataclasses import dataclass
from typing import Dict, List, Optional

S = 'flowchart'
T = '-->'
N = '[*]'

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


def read(path: str = '') -> list[str]:
    _f: list[str] = None
    with open(path, mode='r') as f:
        _f = f.readlines()
        print(_f)
    return _f


def read_head(head: str, fc:Flowchart) -> bool:
    _r: bool = False
    if head.startswith(S):
        _r = True

    return _r


def read_body(body: list[str], fc:Flowchart):
    for __l in body:
        _line = __l.strip()
        if _line.find(T) == -1:
            print('Error: couldnt find: ' + T)
        else:
            _t = _line.split(T)
            print(_t)

            _source = _t[0]
            _target = _t[1]


def read_mermaid_flowchart(lines: list[str]) -> Flowchart:
    head = lines[0].strip()
    body = lines[1:]

    _r: Flowchart = Flowchart(direction='', nodes={}, edges=[])

    if read_head(head=head, fc=_r):
        read_body(body=body, fc=_r)

    return _r


if __name__ == "__main__":
    mermaid = """flowchart TD
        A[Christmas] -->|Get money| B(Go shopping)
        B --> C{Let me think}
        C -->|One| D[Laptop]
        C -->|Two| E[iPhone]
        C -->|Three| F[fa:fa-car Car]
    """

    chart = read_mermaid_flowchart(mermaid.splitlines())

    print("Direction:", chart.direction)
    print("\nNodes:")
    for n in chart.nodes.values():
        print(f"  {n.id}: label='{n.label}', shape='{n.shape}'")

    print("\nEdges:")
    for e in chart.edges:
        print(f"  {e.source} -> {e.target} (label={e.label})")
