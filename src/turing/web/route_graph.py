from flask import Blueprint
from bokeh.models import Plot
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(SCRIPT_DIR)

import reader as r

bp_p_graph = Blueprint('bp_p_graph', __name__)


def prepare_compontents_graph(p: Plot) -> tuple[str, str]:
    from bokeh.embed import components
    script_graph, div_graph = components(p)

    return script_graph, div_graph


def prepare_inline() -> tuple[str, str]:
    from bokeh.resources import INLINE

    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    return js_resources, css_resources


@bp_p_graph.route('/graph')
def prepare_template_graph():
    from flask import render_template
    import web_net as wb
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
