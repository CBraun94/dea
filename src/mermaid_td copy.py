import re
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


# Node pattern: A[Text], B(Text), C{Decision}, D[[Subroutine]], E((Circle))
NODE_PATTERN = re.compile(
    r"""
    ^\s*
    (?P<id>[A-Za-z0-9_]+)
    \s*
    (?P<shape>
        

\[

\[.*?\]

\]

 |      # [[Subroutine]]
        \(\(.*?\)\) |      # ((Circle))
        

\[.*?\]

     |      # [Text]
        \(.*?\)     |      # (Text)
        \{.*?\}            # {Decision}
    )
    """,
    re.VERBOSE,
)

# Edge pattern: A --> B, A -->|Label| B
EDGE_PATTERN = re.compile(
    r"""
    ^\s*
    (?P<src>[A-Za-z0-9_]+)
    \s*
    --(?:>|->|-)?
    \s*
    (?:\|(?P<label>[^|]+)\|\s*)?
    (?P<dst>[A-Za-z0-9_]+)
    """,
    re.VERBOSE,
)


def extract_label(shape: str) -> str:
    """Remove the outer brackets of any Mermaid node shape."""
    if shape.startswith("[[") and shape.endswith("]]"):
        return shape[2:-2]
    if shape.startswith("((") and shape.endswith("))"):
        return shape[2:-2]
    if shape.startswith("[") and shape.endswith("]"):
        return shape[1:-1]
    if shape.startswith("(") and shape.endswith(")"):
        return shape[1:-1]
    if shape.startswith("{") and shape.endswith("}"):
        return shape[1:-1]
    return shape


def parse_flowchart(text: str) -> Flowchart:
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    if not lines:
        raise ValueError("Empty Mermaid text")

    header = lines[0]
    if not header.lower().startswith("flowchart"):
        raise ValueError("First line must start with 'flowchart'")

    direction = header.split()[1]  # TD, LR, RL, BT

    nodes: Dict[str, Node] = {}
    edges: List[Edge] = []

    for line in lines[1:]:
        # Node
        m_node = NODE_PATTERN.match(line)
        if m_node:
            node_id = m_node.group("id")
            shape_raw = m_node.group("shape")
            label = extract_label(shape_raw)

            nodes[node_id] = Node(
                id=node_id,
                label=label,
                shape=shape_raw
            )
            continue

        # Edge
        m_edge = EDGE_PATTERN.match(line)
        if m_edge:
            src = m_edge.group("src")
            dst = m_edge.group("dst")
            label = m_edge.group("label")

            if src not in nodes:
                nodes[src] = Node(id=src)
            if dst not in nodes:
                nodes[dst] = Node(id=dst)

            edges.append(Edge(source=src, target=dst, label=label))
            continue

    return Flowchart(direction=direction, nodes=nodes, edges=edges)


if __name__ == "__main__":
    mermaid = """
    flowchart TD
        A[Christmas] -->|Get money| B(Go shopping)
        B --> C{Let me think}
        C -->|One| D[Laptop]
        C -->|Two| E[iPhone]
        C -->|Three| F[fa:fa-car Car]
    """

    chart = parse_flowchart(mermaid)

    print("Direction:", chart.direction)
    print("\nNodes:")
    for n in chart.nodes.values():
        print(f"  {n.id}: label='{n.label}', shape='{n.shape}'")

    print("\nEdges:")
    for e in chart.edges:
        print(f"  {e.source} -> {e.target} (label={e.label})")
