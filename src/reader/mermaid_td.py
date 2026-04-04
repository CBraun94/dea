import re
from graph import Node, Edge, Flowchart

S = 'flowchart'
T = '-->'
N = '[*]'


testttt = r'/(<index>[a-zA-Z]+)'

re_bracket_curly = r'\{([^}]+)\}'
re_bracket_rect = r'\[([^]]+)\]'
re_bracket_round = r'\(([^)]+)\)'
re_string = r'([A-Za-z]+)'
re_bars = r'\|([^|]+)\|'

RE_STRING = re.compile(re_string)

RE_LABEL = re.compile(re_bars)
RE_RECT_ROUND = re.compile(re_string+re_bracket_round)
RE_RECT = re.compile(re_string+re_bracket_rect)
RE_DIA = re.compile(re_string+re_bracket_curly)


def read(path: str = '') -> list[str]:
    _f: list[str] = None
    with open(path, mode='r') as f:
        _f = f.readlines()
        print(_f)
    return _f


def read_head(head: str, fc: Flowchart) -> bool:
    _r: bool = False
    if head.startswith(S):
        _r = True

    return _r


def read_body(body: list[str], fc: Flowchart):
    for __l in body:
        _line = __l.strip()
        if _line.find(T) == -1:
            print('Error: couldnt find: ' + T)
        else:
            _t = _line.split(T)
            print(_t)

            _source = _t[0]
            _target = _t[1]

            read_target(text=_target)


def read_target(text: str):
    _target = text

    target_node_id: str = None
    target_node_name: str = None
    target_node_shape: str = None
    edge_label: str = None

    aa = RE_STRING.findall(_target)

    ss = RE_RECT_ROUND.findall(_target)
    ff = RE_RECT.findall(_target)
    bb = RE_DIA.findall(_target)

    print('test')

def read_targets(text: str):
    if len(ss) > 0:
        target_node_name = ss
        target_node_shape = 'rect_round'
    elif len(ff) > 0:
        target_node_name = ff
        target_node_shape = 'rect'
    elif len(bb) > 0:
        target_node_name = bb
        target_node_shape = 'diamond'
    else:
        raise ValueError()


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
