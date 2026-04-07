from turing.dataframe import DataFrame


class Application(object):
    def __init__(self):
        self.df: dict[str, DataFrame] = {}
        self.data: dict[str] = {}

        _df: DataFrame = DataFrame()
        self.df[str(_df.uuid)] = _df

    def get_df_first(self) -> DataFrame:
        return self.df[next(iter(self.df))]


app: Application = Application()
