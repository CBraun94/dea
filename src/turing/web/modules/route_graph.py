from flask import Blueprint
import sys
import os
from threading import Thread
from flask import render_template
from bokeh.embed import server_document
from bokeh.server.server import Server
from bokeh.models import ColumnDataSource
from bokeh.document import Document


bp_p_graph = Blueprint('bp_p_graph', __name__)

_PROPERTY = 'Property'
_VALUE = 'Value'

_PORT_APP = '8000'

_ORIGIN_APP_LH = "localhost:"+_PORT_APP
_ORIGIN_APP_IP = "127.0.0.1:"+_PORT_APP
_ORIGIN_BK = 'localhost:5006'

_BK_URL_ROOT = 'http://'+_ORIGIN_BK

_ORIGIN = [_ORIGIN_APP_LH, _ORIGIN_APP_IP, _ORIGIN_BK]


def get_init_table_data_source() -> ColumnDataSource:
    data = {_PROPERTY: ['a', 'b'], _VALUE: ['a', 'b']}
    _source = ColumnDataSource(data)

    return _source


table_source = get_init_table_data_source()
new_table_data: list = []


def bkapp(doc: Document):
    SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    sys.path.append(SCRIPT_DIR)
    from turing.app import app
    from . import t_bokeh as t_bk
    import reader as r

    doc.theme = os.getenv('T_BOKEH_THEME')

    _df = app.get_df_first()
    _g = []
    for key in _df.graphs:
        _g.append(_df.graphs[key])
    # _graph = _df.graphs[next(iter(_df.graphs))]

    G = r.graph.graph_to_nx(_g)
    t_bk.graph.get_netgraph(G=G, doc=doc)


def bktable(doc: Document):
    from bokeh.models import DataTable, TableColumn
    import os
    global table_source

    doc.theme = os.getenv('T_BOKEH_THEME')

    _source = table_source

    columns = [TableColumn(field=_PROPERTY, title=_PROPERTY), TableColumn(field=_VALUE, title=_VALUE)]
    data_table = DataTable(source=_source, columns=columns)

    data_table.autosize_mode = 'force_fit'
    data_table.aspect_ratio = None
    data_table.resizable = False
    data_table.sizing_mode = 'scale_both'

    doc.add_root(data_table)

    doc.add_periodic_callback(update_doc_table, 100)


def update_doc_table():
    global new_table_data
    global table_source

    if len(new_table_data) > 0:
        table_source.data.clear()
        table_source.data = new_table_data[-1]
        new_table_data.clear()


def get_graph_script() -> str:
    script = server_document(_BK_URL_ROOT+'/bkapp')
    return script


def get_table_script() -> str:
    script = server_document(_BK_URL_ROOT+'/bktable')
    return script


@bp_p_graph.route('/graph', methods=['GET'])
def bkapp_page():
    script = get_graph_script()
    return render_template("__base_graph.html", div=script)


@bp_p_graph.route('/graph/select', methods=['POST'])
def run_code():
    from flask import request, jsonify
    global new_table_data

    t = request.json

    _p = []
    _v = []

    for key, value in t.items():
        _p.append(key)
        _v.append(value)

    new_table_data.append({_PROPERTY: _p, _VALUE: _v})

    return jsonify({})


def bk_worker():
    _apps = {}
    _apps['/bkapp'] = bkapp
    _apps['/bktable'] = bktable
    server = Server(_apps, allow_websocket_origin=_ORIGIN)
    server.start()
    server.io_loop.start()


def init() -> Thread:
    t = Thread(target=bk_worker).start()
    return t
