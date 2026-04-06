import pandas as pd
from uuid import UUID, uuid4
import json


class DataFrame(object):
    def __init__(self):
        self.uuid: UUID = uuid4()
        self.df: dict[str, pd.DataFrame] = {}

    def to_dict(self) -> dict:
        _d = {}
        _d['uuid'] = str(self.uuid)
        _d['df'] = {}

        for key in self.df:
            _d['df'][key] = self.df[key].to_dict()

        return _d

    def to_json(self) -> str:
        _d = self.to_dict()
        _r: str = json.dumps(_d)

        return _r
