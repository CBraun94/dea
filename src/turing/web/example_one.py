from flask import Flask, render_template

from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE


app = Flask(__name__)



@app.route('/test')
def bokeh():

    # init a basic bar chart:
    # http://bokeh.pydata.org/en/latest/docs/user_guide/plotting.html#bars
    fig = figure(width=600, height=600)
    fig.vbar(
        x=[1, 2, 3, 4, 5],
        width=0.5,
        bottom=0,
        top=[1.7, 2.2, 4.6, 3.9, 1.1],
        color='navy'
    )

    # grab the static resources
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    # render template
    script, div = components(fig)
    html = render_template(
        'index.html',
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
    )
    return html


@app.route('/')
def test():
    import turing.web.web_net as wb
    p = wb.get_netgraph()
    script, div = components(p)

    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    html = render_template(
        template_name_or_list='embed.html',
        script=script,
        div=div,
        js_resources=js_resources,
        css_resources=css_resources,
    )

    return html


if __name__ == '__main__':
    app.run()
