S = 'stateDiagram-v2'
T = '-->'
N = '[*]'


def read(path: str = '') -> list[str]:
    _f: list[str] = None
    with open(path, mode='r') as f:
        _f = f.readlines()
        print(_f)
    return _f


def mermaid_state_to_dict(lines: list[str]) -> dict:
    _found = lines[0].find(S)

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


if __name__ == '__main__':
    import dea
    _l = read(r'/home/chris/dev/dea/src/test.mermaid')
    _d = mermaid_state_to_dict(_l)

    s = dea.DEA()
    s.fromDict(_d)

    with open('out.py',  mode='w') as f:
        f.write(s.toPython())
