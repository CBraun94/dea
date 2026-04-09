import turing.web.modules as m
import turing.web._const as _c
from flask import Flask, render_template


template_html = _c.TEMPLATE_APP_ROUTE

app = Flask(__name__)


BLUEPRINTS = [m.route_about.bp_p_about,
              m.route_ide_ace.bp_p_ide_ace,
              m.route_graph.bp_p_graph,
              m.route_menubar.bp_p_menubar]


def register_blueprints():
    for bp in BLUEPRINTS:
        app.register_blueprint(bp)


def tree_find(e, t):
    if e in t:
        return t
    for v in t.values():
        r = tree_find(e, v)
        if r:
            return r
    return None


def template_treeview(dict_: dict):
    tree = {}
    for k, v in dict_.items():
        n = tree_find(k, tree)
        (tree if not n else n)[k] = {e: {} for e in v}
    return tree


def all_edges_to_table():
    import os
    fn = os.getenv('TURING_PATH_OUTPUT')+'edges.html'
    r: str = ''
    if os.path.exists(fn):
        with open(file=fn, mode='r') as f:
            r = f.read()

    return r


@app.route(_c.ROUTE_APP_ROOT)
def prepare_template_ide():
    from turing.app import app as t_app

    dict_ = {'files': t_app.data['files'].copy()}

    data = all_edges_to_table()
    script_graph = m.route_graph.get_graph_script()
    script_table = m.route_graph.get_table_script()
    treeview = template_treeview(dict_)

    context = {}
    context['template_name_or_list'] = template_html
    context['script_graph'] = script_graph
    context['script_table'] = script_table
    context['data'] = data
    context['tree'] = treeview

    html = render_template(**context)

    return html


@app.route(_c.ROUTE_APP_ROOT+'callback')
def doc_callback():
    from flask import request, jsonify

    return {}


def run():
    t = m.route_graph.init()
    register_blueprints()
    t.start()
    app.run(port=_c.PORT_FLASK)
