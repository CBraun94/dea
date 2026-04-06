from turing.web import app as web_app
from turing.app import app


def init_df():
    from turing import reader as r
    _df = app.get_df_first()
    graph = r.mermaid_td.read_mermaid_flowchart(r.mermaid_td.mermaid.splitlines())
    _df.graphs['t'] = graph


def main():
    import sys

    if len(sys.argv) == 1:
        init_df()
        web_app.run()


if __name__ == '__main__':
    main()
