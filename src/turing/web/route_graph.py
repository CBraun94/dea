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
from bokeh.sampledata.sea_surface_temperature import sea_surface_temperature
from bokeh.server.server import Server
from bokeh.themes import Theme

SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(SCRIPT_DIR)

import reader as r

bp_p_graph = Blueprint('bp_p_graph', __name__)


def prepare_compontents_graph(p: Plot) -> tuple[str, str]:
    from bokeh.embed import components
    from bokeh import themes
    from bokeh.plotting import curdoc

    curdoc().theme = 'carbon'
    curdoc().add_root(p)

    script_graph, div_graph = components(p, theme='carbon')

    return script_graph, div_graph


def prepare_inline() -> tuple[str, str]:
    from bokeh.resources import INLINE

    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    return js_resources, css_resources


@bp_p_graph.route('/graph2')
def prepare_template_graph():
    from flask import render_template
    import route_graph_util as wb
    G = wb.get_net_data()
    G = r.graph.graph_to_nx(r.mermaid_td.read_mermaid_flowchart(r.mermaid_td.mermaid.splitlines()))
    p = wb.get_netgraph(G=G, plot_title='state diagram')

    script_graph, div_graph = prepare_compontents_graph(p=p)

    js_resources, css_resources = prepare_inline()

    html = render_template(
        template_name_or_list='__base_graph.html',
        script=script_graph,
        div=div_graph,
        js_resources=js_resources,
        css_resources=css_resources
    )

    return html


def bkapp(doc):
    import route_graph_util as wb
    doc.theme = 'carbon'
    G = wb.get_net_data()
    G = r.graph.graph_to_nx(r.mermaid_td.read_mermaid_flowchart(r.mermaid_td.mermaid.splitlines()))
    p = wb.get_netgraph(G=G, doc=doc, plot_title='state2 diagram')


@bp_p_graph.route('/graph', methods=['GET'])
def bkapp_page():
    script = server_document('http://localhost:5006/bkapp')
    return render_template("__base_graph.html", div=script, template="Flask")


def bk_worker():
    # Can't pass num_procs > 1 in this configuration. If you need to run multiple
    # processes, see e.g. flask_gunicorn_embed.py
    server = Server({'/bkapp': bkapp}, io_loop=IOLoop(), allow_websocket_origin=["localhost:8000"])
    server.start()
    server.io_loop.start()


Thread(target=bk_worker).start()
