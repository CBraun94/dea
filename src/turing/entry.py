from turing.web import app as web_app
from turing.app import app


def init_df():
    from turing import reader as r
    _df = app.get_df_first()
    graph = r.mermaid.read_mermaid_flowchart(r.mermaid.mermaid.splitlines())
    _df.graphs['t'] = graph

    _df.read_mermaid_from_dir(path='/home/chris/dev/dea/input/')


def test():
    from turing.reader import graph
    df_nodes, df_edges = graph.graph_to_df(app.get_df_first().graphs['t'])

    df_nodes.to_html('nodes.html')
    df_edges.to_html('edges.html')


def main():
    import sys

    if len(sys.argv) == 1:
        init_df()
        web_app.run()


if __name__ == '__main__':
    main()
