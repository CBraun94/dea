from flask import Blueprint
import sys
import os
from threading import Thread
from flask import render_template
from tornado.ioloop import IOLoop
from bokeh.embed import server_document
from bokeh.server.server import Server


bp_p_graph = Blueprint('bp_p_graph', __name__)


def bkapp(doc):
    SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    sys.path.append(SCRIPT_DIR)

    from . import route_graph_util as wb
    import reader as r

    doc.theme = 'carbon'

    _graph = r.mermaid_td.read_mermaid_flowchart(r.mermaid_td.mermaid.splitlines())

    df_n, df_e = r.graph.graph_to_df(_graph)

    print(df_n)
    print(df_e)

    G = r.graph.graph_to_nx(_graph)
    p = wb.get_netgraph(G=G, doc=doc, plot_title='state2 diagram')


def bktable(doc):
    from bokeh.models import ColumnDataSource, DataTable, TableColumn

    doc.theme = 'carbon'

    data = {'Property': ['a', 'b'], 'Value': ['a', 'b']}
    _source = ColumnDataSource(data)
    columns = [TableColumn(field='Property', title='Property'), TableColumn(field='Value', title='Value')]
    data_table = DataTable(source=_source, columns=columns)

    data_table.autosize_mode = 'force_fit'
    data_table.aspect_ratio = None
    data_table.resizable = False
    data_table.sizing_mode = 'scale_both'

    doc.add_root(data_table)


def get_graph_script() -> str:
    script = server_document('http://localhost:5006/bkapp')
    return script


def get_table_script() -> str:
    script = server_document('http://localhost:5006/bktable')
    return script


@bp_p_graph.route('/graph', methods=['GET'])
def bkapp_page():
    script = get_graph_script()
    return render_template("__base_graph.html", div=script)


@bp_p_graph.route('/graph/select', methods=['POST'])
def run_code():
    from flask import request, jsonify

    return request.json


def bk_worker():
    # Can't pass num_procs > 1 in this configuration. If you need to run multiple
    # processes, see e.g. flask_gunicorn_embed.py
    _apps = {}
    _apps['/bkapp'] = bkapp
    _apps['/bktable'] = bktable
    server = Server(_apps, io_loop=IOLoop(), allow_websocket_origin=["localhost:8000", "127.0.0.1:8000", 'localhost:5006'])
    server.start()
    server.io_loop.start()


def init() -> Thread:
    t = Thread(target=bk_worker).start()
    return t
