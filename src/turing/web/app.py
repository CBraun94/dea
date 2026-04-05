import modules as m
from flask import Flask, render_template


template_html = r'__ide_gui.html'

app = Flask(__name__)
app.register_blueprint(m.route_about.bp_p_about)
app.register_blueprint(m.route_ide_ace.bp_p_ide_ace)
app.register_blueprint(m.route_graph.bp_p_graph)
app.register_blueprint(m.route_menubar.bp_p_menubar)


@app.route('/')
def prepare_template_ide():
    script_graph = m.route_graph.get_graph_script()
    html = render_template(
        template_name_or_list=template_html,
        script_graph=script_graph
    )

    return html


def run():
    t = m.route_graph.init()
    app.run(port=8000)


if __name__ == '__main__':
    run()
