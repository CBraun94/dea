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
    LabelSet
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


def prepare_labels(graph_renderer):
    x,y=zip(*graph_renderer.layout_provider.graph_layout.values())
    graph_renderer.node_renderer.data_source.data['x']=x
    graph_renderer.node_renderer.data_source.data['y']=y

    labels=LabelSet(x='x', y='y', text='index',level='glyph', source=graph_renderer.node_renderer.data_source)

    return labels


def get_netgraph(plot_width: int = 800, plot_height: int = 800):

    # Prepare Data
    G = get_net_data()


    # Show with Bokeh
    p = Plot(
        width=plot_width,
        height=plot_height,
        x_range=Range1d(-1.1, 1.1),
        y_range=Range1d(-1.1, 1.1),
    )
    p.title.text = "DFA"

    node_hover_tool = HoverTool(tooltips=[("index", "@index"), ("club", "@club")])
    p.add_tools(node_hover_tool, BoxZoomTool(), ResetTool())

    graph_renderer = from_networkx(G, nx.spectral_layout, scale=1, center=(0, 0))

    labels = prepare_labels(graph_renderer=graph_renderer)

    p.renderers.append(graph_renderer)

    p.renderers.append(labels)

    return p
