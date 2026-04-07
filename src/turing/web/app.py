import turing.web.modules as m
import turing.web._const as _c
from flask import Flask, render_template


template_html = _c.TEMPLATE_APP_ROUTE

app = Flask(__name__)
app.register_blueprint(m.route_about.bp_p_about)
app.register_blueprint(m.route_ide_ace.bp_p_ide_ace)
app.register_blueprint(m.route_graph.bp_p_graph)
app.register_blueprint(m.route_menubar.bp_p_menubar)


@app.route(_c.ROUTE_APP_ROOT)
def prepare_template_ide():
    data = r"{'A': {'A': ['A'], 'B': ['A', 'B'], 'C': ['A', 'B', 'C'], 'D': ['A', 'B', 'C', 'D'], 'E': ['A', 'B', 'C', 'E'], 'F': ['A', 'B', 'C', 'F']}, 'B': {'B': ['B'], 'C': ['B', 'C'], 'D': ['B', 'C', 'D'], 'E': ['B', 'C', 'E'], 'F': ['B', 'C', 'F']}, 'C': {'C': ['C'], 'D': ['C', 'D'], 'E': ['C', 'E'], 'F': ['C', 'F']}, 'D': {'D': ['D']}, 'E': {'E': ['E']}, 'F': {'F': ['F']}}"
    script_graph = m.route_graph.get_graph_script()
    script_table = m.route_graph.get_table_script()
    html = render_template(
        template_name_or_list=template_html,
        script_graph=script_graph,
        script_table=script_table,
        data=data
    )

    return html


def run():
    t = m.route_graph.init()
    app.run(port=_c.PORT_FLASK)


if __name__ == '__main__':
    run()
