import re
from .graph import Node, Edge, Graph

mermaid = """flowchart TD
        A[Christmas] -->|Get money| B(Go shopping)
        B --> C{Let me think}
        C -->|One| D[Laptop]
        C -->|Two| E[iPhone]
        C -->|Three| F[Car]"""

STATE = 'stateDiagram-v2'
S = 'flowchart'
T = '-->'
N = '[*]'


testttt = r'/(<index>[a-zA-Z]+)'

re_bracket_curly = r'\{(?P<name>[^}]+)\}'
re_bracket_rect = r'\[(?P<name>[^]]+)\]'
re_bracket_round = r'\((?P<name>[^)]+)\)'
re_string = r'(?P<index>[A-Za-z]+)'
re_bars = r'\|(?P<label>[^|]+)\|'

RE_STRING = re.compile(re_string)

RE_LABEL = re.compile(re_bars)
RE_RECT_ROUND = re.compile(re_string+re_bracket_round)
RE_RECT = re.compile(re_string+re_bracket_rect)
RE_DIA = re.compile(re_string+re_bracket_curly)


def __read(path: str = '') -> str:
    _f: list[str] = None
    with open(path, mode='r') as f:
        _f = f.read()
    return _f


def mermaid_state_to_dict(lines: list[str]) -> dict:
    _found = lines[0].find(STATE)

    _r: dict = {}

    if _found == -1:
        print("Error: couldn't find: " + S)
    else:
        for i in range(1, len(lines)):
            _s = lines[i].strip().split(' ')
            if _s[1] == T:
                if _s[0] in _r:
                    _r[_s[0]].append(_s[2])
                else:
                    _r[_s[0]] = []
                    _r[_s[0]].append(_s[2])
            else:
                print("Error: couldn't find: " + S)

    return _r


def mermaid_state_to_graph(lines: list[str]) -> Graph:
    _found = lines[0].find(STATE)

    _r: Graph = Graph()

    if _found == -1:
        print("Error: couldn't find: " + S)
    else:
        for i in range(1, len(lines)):
            _s = lines[i].strip().split(' ')
            if _s[1] == T:
                _src = _s[0]
                _dst = _s[2]

                if _src == N:
                    _src = 'START_STATE'

                if _dst == N:
                    _dst = 'ENDSTATE'

                _r.edges.append(Edge(source=_src, target=_dst))

                if _src not in _r.nodes:
                    _r.nodes[_src] = Node(id=_src, name=_src)
                
                if _dst not in _r.nodes:
                    _r.nodes[_dst] = Node(id=_dst, name=_dst)

            else:
                print("Error: couldn't find: " + S)

    return _r


def read_head(head: str, fc: Graph) -> bool:
    _r: bool = False
    if head.startswith(S):
        _r = True

    return _r


def read_body(body: list[str], fc: Graph):
    for __l in body:
        _line = __l.strip()
        if _line.find(T) == -1:
            print('Error: couldnt find: ' + T)
        else:
            _t = _line.split(T)

            _source = _t[0]
            _target = _t[1]

            _e, _nodes = read_edge(left=_source, right=_target)

            fc.edges.append(_e)
            for _node in _nodes:
                if _node.id in fc.nodes:
                    if _node.name is not None:
                        fc.nodes[_node.id].name = _node.name
                    if _node.shape is not None:
                        fc.nodes[_node.id].shape = _node.shape
                else:
                    fc.nodes[_node.id] = _node


def read_edge(left: str, right: str) -> tuple[Edge, list[Node]]:
    _source = left
    _target = right

    source_node_index: str = None
    source_node_name: str = None
    source_node_shape: str = None

    target_node_index: str = None
    target_node_name: str = None
    target_node_shape: str = None

    edge_label: str = None

    aa = RE_LABEL.search(_source)
    if aa is not None:
        edge_label = aa.group('label')

    sss = RE_RECT_ROUND.search(_source)
    if sss is not None:
        source_node_name = sss.group('name')
        source_node_index = sss.group('index')
        source_node_shape = 'ellipse'
    f = RE_RECT.search(_source)
    if f is not None:
        source_node_name = f.group('name')
        source_node_index = f.group('index')
        source_node_shape = 'rect'
    b = RE_DIA.search(_source)
    if b is not None:
        source_node_name = b.group('name')
        source_node_index = b.group('index')
        source_node_shape = 'diamond'

    if source_node_index is None:
        n = RE_STRING.search(_source)
        if n is not None:
            source_node_index = n.group('index')

    aa = RE_LABEL.search(_target)
    if aa is not None:
        edge_label = aa.group('label')

    sss = RE_RECT_ROUND.search(_target)
    if sss is not None:
        target_node_name = sss.group('name')
        target_node_index = sss.group('index')
        target_node_shape = 'ellipse'
    f = RE_RECT.search(_target)
    if f is not None:
        target_node_name = f.group('name')
        target_node_index = f.group('index')
        target_node_shape = 'rect'
    b = RE_DIA.search(_target)
    if b is not None:
        target_node_name = b.group('name')
        target_node_index = b.group('index')
        target_node_shape = 'diamond'

    _r = Edge(source=source_node_index, target=target_node_index, name=edge_label)

    return _r, [
        Node(id=source_node_index, name=source_node_name, shape=source_node_shape),
        Node(id=target_node_index, name=target_node_name, shape=target_node_shape)
        ]


def read_mermaid_flowchart(lines: list[str]) -> Graph:
    head = lines[0].strip()
    body = lines[1:]

    _r: Graph = Graph()

    if read_head(head=head, fc=_r):
        read_body(body=body, fc=_r)

    return _r


def read(file_path: str):
    file_str = __read(path=file_path)

    lines = file_str.splitlines()

    _r: Graph = None

    if lines[0].strip().startswith(STATE):
        _r = mermaid_state_to_graph(lines)
    elif lines[0].strip().startswith(S):
        _r = read_mermaid_flowchart(lines)

    return _r


if __name__ == "__main__":
    chart = read_mermaid_flowchart(mermaid.splitlines())

    print("Direction:", chart.direction)
    print("\nNodes:")
    for n in chart.nodes.values():
        print(f"  {n.id}: label='{n.name}', shape='{n.shape}'")

    print("\nEdges:")
    for e in chart.edges:
        print(f"  {e.source} -> {e.target} (label={e.name})")
