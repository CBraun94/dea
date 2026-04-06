import pandas as pd
from uuid import UUID, uuid4
import json
from turing.reader.graph import Graph

KEY_UUID = 'uuid'
KEY_DF = 'df'


class DataFrame(object):
    def __init__(self):
        self.uuid: UUID = uuid4()
        self.df: dict[str, pd.DataFrame] = {}
        self.graphs: dict[str, Graph] = {}

    def to_dict(self) -> dict:
        _d = {}
        _d[KEY_UUID] = str(self.uuid)
        _d[KEY_DF] = {}

        for key in self.df:
            _d[KEY_DF][key] = self.df[key].to_dict()

        return _d

    def to_json(self) -> str:
        _d = self.to_dict()
        _r: str = json.dumps(_d)

        return _r
    
    def read_mermaid_from_dir(path: str):
        from turing import io

        _files = io.dir_walk(path)
        _files_mermaid = io.files_mermaid(_files)
