from flask import Flask, render_template

from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE


template_html = 'embed.html'

app = Flask(__name__)


@app.route('/')
def test():
    import web_net as wb
    p = wb.get_netgraph()
    script, div = components(p)

    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    html = render_template(
        template_name_or_list=template_html,
        script=script,
        div=div,
        js_resources=js_resources,
        css_resources=css_resources,
    )

    return html


if __name__ == '__main__':
    app.run()
