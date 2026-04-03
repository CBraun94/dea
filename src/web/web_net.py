import networkx as nx

from bokeh.io import show
from bokeh.models import (
    BoxZoomTool,
    Circle,
    HoverTool,
    MultiLine,
    Plot,
    Range1d,
    ResetTool,
)
from bokeh.palettes import Spectral4
from bokeh.plotting import from_networkx


def get_net_data():
    G = nx.MultiDiGraph()
    G.add_node('START_STATE')
    G.add_node('Still')
    G.add_edge('START_STATE', 'Still', weight=1.0, color='red')
    G.add_edge('Still', 'END_STATE', weight=1.0, color='red')
    G.add_edge('Still', 'Moving', weight=1.0, color='red')
    G.add_edge('Moving', 'Crash', weight=1.0, color='red')
    G.add_edge('Crash', 'END_STATE', weight=1.0, color='red')
    return G


def get_netgraph():

    # Prepare Data
    G = get_net_data()


    # Show with Bokeh
    p = Plot(
        width=400,
        height=400,
        x_range=Range1d(-1.1, 1.1),
        y_range=Range1d(-1.1, 1.1),
    )
    p.title.text = "DFA"

    node_hover_tool = HoverTool(tooltips=[("index", "@index"), ("club", "@club")])
    p.add_tools(node_hover_tool, BoxZoomTool(), ResetTool())

    graph_renderer = from_networkx(G, nx.spectral_layout, scale=1, center=(0, 0))


    p.renderers.append(graph_renderer)

    show(p)

    return p