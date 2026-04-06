from dataframe import DataFrame


class Application(object):
    def __init__(self):
        self.df: dict[str, DataFrame] = {}
