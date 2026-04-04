import networkx as nx
from bokeh.models import (
    BoxZoomTool,
    WheelZoomTool,
    PanTool,
    TapTool,
    Circle,
    HoverTool,
    MultiLine,
    Plot,
    Range1d,
    ResetTool,
    LabelSet,
    Toolbar,
    ToolbarPanel,
)
from bokeh.plotting import from_networkx
from bokeh.layouts import layout, row


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


def prepare_tools():
    node_hover_tool = HoverTool(tooltips=[("index", "@index"), ("name", "@name"), ("shape", "@shape"), ("docstring", "@docstring")])
    node_tap_tool = TapTool()
    tools = [node_hover_tool, ResetTool(), WheelZoomTool(), PanTool(), node_tap_tool]

    return tools


def get_netgraph(G: nx.classes.Graph, plot_title: str = None, plot_width: int = 400, plot_height: int = 400):
    import graph

    p = Plot(
        width=plot_width,
        height=plot_height,
        min_width=200,
        min_height=200,
        max_width=1200,
        max_height=800,
        toolbar_location='below',
        toolbar_sticky=False,
        align='center',
        resizable=True,
        sizing_mode='scale_both',
        aspect_ratio=None,
        height_policy='max',
        width_policy='max'
    )
    p.title.text = plot_title
    p.toolbar.autohide = False
    p.toolbar.logo = None

    tools = prepare_tools()

    p.tools = tools

    graph_renderer = from_networkx(G, nx.spectral_layout, scale=1, center=(0, 0))
    graph_renderer.node_renderer.glyph = Circle(radius=0.03)

    labels = graph.util.prepare_labels(graph_renderer=graph_renderer)

    p.renderers.append(graph_renderer)

    p.renderers.append(labels)

    return p
