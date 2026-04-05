import numpy as np

from bokeh import events
from bokeh.layouts import column, row
from bokeh.models import Button, CustomJS, Div
from bokeh.plotting import figure


p.js_on_event(
    events.SelectionGeometry,
    CustomJS(
        args=dict(div=div),
        code="""
div.text = "Selection! <p> <p>" + JSON.stringify(cb_obj.geometry, undefined, 2);
""",
    ),
)