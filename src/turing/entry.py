from turing.web import app as web_app
from turing.app import app


def dir_walk(start_path='/home/chris/dev/dea/input/') -> list[str]:
    import os
    _r = []
    for root, dirs, files in os.walk(start_path):
        for file in files:
            _r.append(os.path.join(root, file))
    return _r


def init_df():
    from turing import reader as r
    _df = app.get_df_first()
    graph = r.mermaid_td.read_mermaid_flowchart(r.mermaid_td.mermaid.splitlines())
    _df.graphs['t'] = graph


def test():
    from turing.reader import graph
    df_nodes, df_edges = graph.graph_to_df(app.get_df_first().graphs['t'])

    df_nodes.to_html('nodes.html')
    df_edges.to_html('edges.html')


def files_mermaid(files: list[str]) -> list[str]:
    import pathlib

    _r = []
    for file in files:
        file_extension = pathlib.Path(file).suffix
        if file_extension == '.mermaid':
            _r.append(file)
    return _r


def main():
    import sys

    _files = dir_walk()
    print(_files)
    _f_mermaid = files_mermaid(_files)
    print(_f_mermaid)

    if len(sys.argv) == 1:
        init_df()
        web_app.run()


if __name__ == '__main__':
    main()
