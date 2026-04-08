from turing.dataframe import DataFrame
from typing import Dict, Optional


class Application(object):
    def __init__(self):
        self.df: Dict[str, DataFrame] = {}
        self.data: Dict[str] = {}
        self.env: Dict[str, Optional[str]] = {}

        _df: DataFrame = DataFrame()
        self.df[str(_df.uuid)] = _df

        self.__init_env()

    def get_df_first(self) -> DataFrame:
        return self.df[next(iter(self.df))]

    def __init_env(self):
        import dotenv
        self.env = dotenv.dotenv_values()


app: Application = Application()
