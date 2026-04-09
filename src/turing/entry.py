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
    df = app.get_df_first()

    for key in df.graphs:
        _fn = os.path.basename(key)

    df_nodes.to_html('nodes.html')
    df_edges.to_html('edges.html')


def main():
    import sys

    import dotenv
    dotenv.load_dotenv()

    if len(sys.argv) == 1:
        init_app()
        init_df()
        web_app.run()


if __name__ == '__main__':
    main()
