from flask import Flask, render_template

from bokeh.embed import components
from bokeh.plotting import figure

from bokeh.models import Plot


template_html = 'embed.html'

app = Flask(__name__)


def prepare_compontents_graph(p: Plot) -> tuple[str, str]:
    script_graph, div_graph = components(p)

    return script_graph, div_graph


def prepare_inline() -> tuple[str, str]:
    from bokeh.resources import INLINE

    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    return js_resources, css_resources


@app.route('/')
def prepare_template_graph():
    import web_net as wb
    p = wb.get_netgraph()

    script_graph, div_graph = prepare_compontents_graph(p=p)

    js_resources, css_resources = prepare_inline()

    html = render_template(
        template_name_or_list=template_html,
        script=script_graph,
        div=div_graph,
        js_resources=js_resources,
        css_resources=css_resources,
    )

    return html


if __name__ == '__main__':
    app.run()
