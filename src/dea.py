import mermaid_reader as mr


NONE = '__none'
N = '[*]'
E = 'END_STATE'
S = 'START_STATE'

A = 'def state_{state}(input: list):\n'
B = "    if input[0] == '{input}':\n        state_{dst}(input[1:])\n"
C = "if __name__ == '__main__':\n    import sys\n    state_START_STATE(sys.argv[1:])\n"
D = '    print("done")\n'


def pl_df_edges():
    import polars as pl
    data = []
    _df = pl.DataFrame(data, schema=["node_start", "node_end", "docstring"], orient="row")

    return _df


def pl_df_nodes():
    import polars as pl
    data = []
    _df = pl.DataFrame(data, schema=["name", "docstring"], orient="row")

    return _df


def pl_df_graphs():
    import polars as pl
    data = []
    _df = pl.DataFrame(data, schema=["name", "docstring", "mermaid"], orient="row")

    return _df


class BaseDEAObject(object):
    def __init__(self):
        self.name: str = NONE


class Transition(BaseDEAObject):
    def __init__(self):
        super().__init__()
        self.dst: str = NONE


class State(BaseDEAObject):
    def __init__(self):
        super().__init__()
        self.trans: dict[str, Transition] = {}
        self.isEnd: bool = False


class DEA(BaseDEAObject):
    def __init__(self):
        super().__init__()
        self.states: dict[str, State] = {}

    def fromDict(self, d: dict):
        for key in d:
            _s = State()
            for t in d[key]:
                tt = t
                if tt == N:
                    tt = E
                _t = Transition()
                _t.dst = tt
                _s.trans[tt] = _t
            _s.name = key
            if _s.name == N:
                _s.name = S
            self.states[_s.name] = _s

        _ss = State()
        _ss.name = E
        _ss.isEnd = True
        self.states[_ss.name] = _ss

    def read_mermaid_file(self, path: str = ''):
        _lines = mr.read(path)
        _dict = mr.mermaid_state_to_dict(_lines)
        self.fromDict(_dict)

    def toPython(self) -> str:
        _s = ''
        for state in self.states:
            _state = self.states[state]
            _s += A.format(state=_state.name)
            if _state.isEnd:
                _s += D
            else:
                for t in _state.trans:
                    _trans = _state.trans[t]
                    _s += B.format(input=_trans.name, dst=_trans.dst)
            _s += '\n\n'

        _s += C
        return _s
