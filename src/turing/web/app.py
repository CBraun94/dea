import route_about as r_a
import route_ide as r_ide
import route_graph as r_graph
import route_menubar as r_menubar
from flask import Flask, render_template


template_html = r'__ide_gui.html'

app = Flask(__name__)
app.register_blueprint(r_a.bp_p_about)
app.register_blueprint(r_ide.bp_p_ide)
app.register_blueprint(r_graph.bp_p_graph)
app.register_blueprint(r_menubar.bp_p_menubar)


@app.route('/')
def prepare_template_ide():
    html = render_template(
        template_name_or_list=template_html,
        iframe_menubar='/menubar',
        iframe_graph='/graph',
        iframe_ide='/ide'
    )

    return html


if __name__ == '__main__':
    app.run(port=8000)
