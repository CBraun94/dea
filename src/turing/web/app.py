import route_about as r_a
import route_ide as r_ide
import route_graph as r_graph

from flask import Flask, render_template


template_html = r'embed.html'

app = Flask(__name__)
app.register_blueprint(r_a.bp_p_about)
app.register_blueprint(r_ide.bp_p_ide)
app.register_blueprint(r_graph.bp_p_graph)


@app.route('/')
def prepare_template_ide():
    html = render_template(
        template_name_or_list=template_html,
        iframe_graph='/graph',
        iframe_about='/ide'
    )

    return html


if __name__ == '__main__':
    app.run(port=8000)
