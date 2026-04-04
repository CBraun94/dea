import networkx as nx
from networkx.drawing.nx_agraph import write_dot, graphviz_layout

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

from bokeh.plotting import figure


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
    tooltips = [("index", "@index"), ("name", "@name"), ("shape", "@shape"), ("docstring", "@docstring")]
    node_hover_tool = HoverTool(tooltips=tooltips)
    node_tap_tool = TapTool()
    tools = [node_hover_tool, ResetTool(), WheelZoomTool(), PanTool(), node_tap_tool]

    return tools


def get_netgraph(G: nx.classes.Graph, doc = None, plot_title: str = None, plot_width: int = 400, plot_height: int = 400):
    import graph
    import math
    from bokeh.plotting import from_networkx, curdoc

    from bokeh import themes

    alpha = 1.0

    p = figure(
        width=plot_width,
        height=plot_height,
        min_width=200,
        min_height=200,
        max_width=1200,
        max_height=800,
        toolbar_location='below',
        toolbar_sticky=False,
        align='center',
        resizable=False,
        sizing_mode='scale_both',
        aspect_ratio=None,
        height_policy='max',
        width_policy='max',
        match_aspect=True
    )
    p.title.text = plot_title
    p.toolbar.autohide = False
    p.toolbar.logo = None

    tools = prepare_tools()

    p.tools = tools

    if doc is not None:
        doc.add_root(p)
        doc.theme = 'carbon'

    graph_renderer = None
    __layout: str = 'graphviz'

    if __layout == 'spectral':
        graph_renderer = from_networkx(G, nx.spectral_layout, scale=1, center=(0, 0))
        graph_renderer.node_renderer.glyph = Circle(radius=0.03)
    elif __layout == 'spring':
        graph_renderer = from_networkx(G, nx.spring_layout, scale=1, center=(0, 0), k=5/math.sqrt(G.order()), seed=0)
        graph_renderer.node_renderer.glyph = Circle(radius=0.03)
    elif __layout == 'graphviz':
        graph_renderer = from_networkx(graph=G, layout_function=graphviz_layout, prog='dot')
        graph_renderer.node_renderer.glyph = Circle(radius=3)

    graph_renderer.node_renderer.data_source.data['index'] = list(G.nodes())
    #graph_renderer.apply_theme(themes._carbon.json)

    labels = graph.util.prepare_labels(graph_renderer=graph_renderer)

    p.renderers.append(graph_renderer)

    p.renderers.append(labels)

    return p
