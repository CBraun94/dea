import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(SCRIPT_DIR)

import reader as r

from flask import Flask, render_template
from bokeh.models import Plot


template_html = r'embed.html'

app = Flask(__name__)


def prepare_compontents_graph(p: Plot) -> tuple[str, str]:
    from bokeh.embed import components
    script_graph, div_graph = components(p)

    return script_graph, div_graph


def prepare_inline() -> tuple[str, str]:
    from bokeh.resources import INLINE

    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    return js_resources, css_resources


@app.route('/ide')
def index():
    return render_template('ide_py.html')


@app.route('/ide/run', methods=['POST'])
def run_code():
    from flask import request, jsonify
    from io import StringIO
    code = request.json['code']
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()

    try:
        exec(code)
        sys.stdout = old_stdout
        return jsonify({'output': redirected_output.getvalue()})
    except Exception as e:
        sys.stdout = old_stdout
        return jsonify({'output': str(e)})


@app.route('/about')
def prepare_template_about():
    html = render_template(
        template_name_or_list='about.html')
    return html


@app.route('/graph')
def prepare_template_graph():
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


@app.route('/')
def prepare_template_ide():
    html = render_template(
        template_name_or_list=template_html,
        iframe_graph='/graph',
        iframe_about='/ide'
    )

    return html


if __name__ == '__main__':
    app.run()
