from flask import Blueprint
from bokeh.models import Plot
import sys
import os

from threading import Thread

from flask import Flask, render_template
from tornado.ioloop import IOLoop

from bokeh.embed import server_document
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider
from bokeh.plotting import figure
from bokeh.server.server import Server
from bokeh.themes import Theme

SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(SCRIPT_DIR)

import reader as r

bp_p_graph = Blueprint('bp_p_graph', __name__)


def bkapp(doc):
    import web.modules.route_graph_util as wb
    doc.theme = 'carbon'
    G = wb.get_net_data()
    G = r.graph.graph_to_nx(r.mermaid_td.read_mermaid_flowchart(r.mermaid_td.mermaid.splitlines()))
    p = wb.get_netgraph(G=G, doc=doc, plot_title='state2 diagram')

    from bokeh import events
    from bokeh.models import CustomJS
    # alert("Hello! I am an alert box!!");
    #const index = cb_data.source.inspected.indices[0];

    click_event = CustomJS(code="""$("#ttt").text(JSON.stringify(cb_obj, undefined, 2));""")

    cb_sel_geo = CustomJS(code="""$("#ttt").text("Selection! <p> <p>" + JSON.stringify(cb_obj.geometry));console.log(cb_data);console.log(cb_obj);""")

    p.js_on_event(events.SelectionGeometry, cb_sel_geo)
    #p.js_on_event(events.Tap, a)


def get_graph_script() -> str:
    script = server_document('http://localhost:5006/bkapp')
    return script


@bp_p_graph.route('/graph', methods=['GET'])
def bkapp_page():
    script = get_graph_script()
    return render_template("__base_graph.html", div=script)


def bk_worker():
    # Can't pass num_procs > 1 in this configuration. If you need to run multiple
    # processes, see e.g. flask_gunicorn_embed.py
    server = Server({'/bkapp': bkapp}, io_loop=IOLoop(), allow_websocket_origin=["localhost:8000", "127.0.0.1:8000"])
    server.start()
    server.io_loop.start()


def init() -> Thread:
    t = Thread(target=bk_worker).start()
    return t
