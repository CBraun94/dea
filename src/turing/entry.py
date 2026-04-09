from turing.web import app as web_app
from turing.app import app


def init_df():
    import os
    _df = app.get_df_first()
    _df.read_mermaid_from_dir(path=os.getenv('TURING_PATH_INPUT'))


def init_app():
    from turing import io
    _files = io.dir_walk()

    app.data['files'] = _files.copy()


def test():
    import os
    import pandas as pd
    df = app.get_df_first()

    e, c = df.graphs_to_list()

    _df = pd.DataFrame(data=e, columns=c)

    _df.to_html(os.getenv('TURING_PATH_OUTPUT')+'edges.html')


def main():
    import sys
    if len(sys.argv) == 1:
        import dotenv
        dotenv.load_dotenv()
        init_app()
        init_df()
        test()
        web_app.run()
