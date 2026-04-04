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


def prepare_labels(graph_renderer) -> LabelSet:
    x, y = zip(*graph_renderer.layout_provider.graph_layout.values())
    graph_renderer.node_renderer.data_source.data['x'] = x
    graph_renderer.node_renderer.data_source.data['y'] = y

    labels = LabelSet(x='x',
                      y='y',
                      text='index',
                      level='glyph',
                      source=graph_renderer.node_renderer.data_source)

    return labels


def prepare_tools():
    node_hover_tool = HoverTool(tooltips=[("name", "@index"), ("club", "@club")])
    node_tap_tool = TapTool()
    tools = [node_hover_tool, ResetTool(), WheelZoomTool(), PanTool(), node_tap_tool]

    return tools


def get_netgraph(plot_width: int = 800, plot_height: int = 800):
    G = get_net_data()

    p = Plot(
        width=plot_width,
        height=plot_height,
        x_range=Range1d(-1.1, 1.1),
        y_range=Range1d(-1.1, 1.1),
        toolbar_location='below',
        toolbar_sticky=False
    )
    p.title.text = "DFA"
    p.toolbar.autohide = False
    p.toolbar.logo = None

    tools = prepare_tools()

    p.tools = tools

    graph_renderer = from_networkx(G, nx.spectral_layout, scale=1, center=(0, 0))
    graph_renderer.node_renderer.glyph = Circle(radius=0.03)

    labels = prepare_labels(graph_renderer=graph_renderer)

    p.renderers.append(graph_renderer)

    p.renderers.append(labels)

    return p
