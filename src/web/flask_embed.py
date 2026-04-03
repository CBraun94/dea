from bokeh.embed import server_document
from flask import Flask
from flask import render_template
from tornado.ioloop import IOLoop

from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider
from bokeh.plotting import figure
from bokeh.sampledata.sea_surface_temperature import sea_surface_temperature
from bokeh.server.server import Server
from bokeh.themes import Theme


def modify_doc(doc):
    df = sea_surface_temperature.copy()
    source = ColumnDataSource(data=df)

    plot = figure(
        x_axis_type="datetime",
        y_range=(0, 25),
        y_axis_label="Temperature (Celsius)",
        title="Sea Surface Temperature at 43.18, -70.43",
    )
    plot.line("time", "temperature", source=source)

    def callback(attr, old, new):
        if new == 0:
            data = df
        else:
            data = df.rolling("{0}D".format(new)).mean()
        source.data = ColumnDataSource(data=data).data

    slider = Slider(
        start=0, end=30, value=0, step=1, title="Smoothing by N Days"
    )
    slider.on_change("value", callback)

    doc.add_root(column(slider, plot))

    doc.theme = Theme(filename="theme.yaml")


app = Flask(__name__)


@app.route("/", methods=["GET"])
def bkapp_page():
    script = server_document("http://localhost:5006/bkapp")
    return render_template("embed.html", script=script, framework="Flask")


def bk_worker():
    server = Server(
        {"/bkapp": modify_doc},
        io_loop=IOLoop(),
        allow_websocket_origin=["localhost:8000"],
    )
    server.start()
    server.io_loop.start()



if __name__ == "__main__":
    app.run(port=8000, debug=True)