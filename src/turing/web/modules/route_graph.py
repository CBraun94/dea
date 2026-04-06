from flask import Blueprint
import sys
import os
from threading import Thread
from flask import render_template
from tornado.ioloop import IOLoop
from bokeh.embed import server_document
from bokeh.server.server import Server
from bokeh.models import ColumnDataSource
from bokeh.document import Document


bp_p_graph = Blueprint('bp_p_graph', __name__)

_PROPERTY = 'Property'
_VALUE = 'Value'

_THEME = 'carbon'

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
new_table_data: dict = None


def ttt():
    return new_table_data


def aaa():
    return table_source


def bkapp(doc: Document):
    SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    sys.path.append(SCRIPT_DIR)

    from . import route_graph_util as wb
    import reader as r

    doc.theme = _THEME

    _graph = r.mermaid_td.read_mermaid_flowchart(r.mermaid_td.mermaid.splitlines())

    G = r.graph.graph_to_nx(_graph)
    wb.get_netgraph(G=G, doc=doc)


def bktable(doc: Document):
    from bokeh.models import DataTable, TableColumn
    global table_source

    doc.theme = _THEME

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

    if new_table_data is not None:
        table_source.data = new_table_data
        new_table_data = None


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

    new_table_data = {_PROPERTY: _p, _VALUE: _v}

    return request.json


def bk_worker():
    _apps = {}
    _apps['/bkapp'] = bkapp
    _apps['/bktable'] = bktable
    server = Server(_apps, io_loop=IOLoop(), allow_websocket_origin=_ORIGIN)
    server.start()
    server.io_loop.start()


def init() -> Thread:
    t = Thread(target=bk_worker).start()
    return t
