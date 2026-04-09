import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
from bokeh.models import (
    WheelZoomTool,
    PanTool,
    TapTool,
    Circle,
    HoverTool,
    ResetTool,
    LabelSet
)
from bokeh.plotting import figure
from typing import List
from bokeh.models.renderers import GraphRenderer


CSS_CLASSES: List[str] = []
tooltips = [("index", "@index"), ("name", "@name"), ("shape", "@shape"), ("docstring", "@docstring")]


def prepare_labels(graph_renderer: GraphRenderer) -> LabelSet:
    x, y = zip(*graph_renderer.layout_provider.graph_layout.values())
    graph_renderer.node_renderer.data_source.data['x'] = x
    graph_renderer.node_renderer.data_source.data['y'] = y

    labels = LabelSet(x='x',
                      y='y',
                      text='name',
                      level='glyph',
                      source=graph_renderer.node_renderer.data_source,
                      text_color="#FFFFFF")

    return labels


def prepare_tools():
    from bokeh.models import CustomJS
    import os

    cb_js_code: str = None
    with open(file=os.getenv('TURING_PATH_JS_TAPTOOL'), mode='r') as f:
        cb_js_code = f.read()

    node_hover_tool = HoverTool(tooltips=tooltips)
    node_tap_tool = TapTool(behavior='select',  callback=CustomJS(code=cb_js_code))
    tools = [node_hover_tool, ResetTool(), WheelZoomTool(), PanTool(), node_tap_tool]

    return tools


def prepare_graph_renderer(G: nx.classes.Graph):
    from bokeh.plotting import from_networkx
    __layout: str = 'graphviz'

    graph_renderer: GraphRenderer = None

    if __layout == 'spectral':
        graph_renderer = from_networkx(G, nx.spectral_layout, scale=1, center=(0, 0))
        graph_renderer.node_renderer.glyph = Circle(radius=0.03)
    elif __layout == 'spring':
        import math
        graph_renderer = from_networkx(G, nx.spring_layout, scale=1, center=(0, 0), k=5/math.sqrt(G.order()), seed=0)
        graph_renderer.node_renderer.glyph = Circle(radius=0.03)
    elif __layout == 'graphviz':
        graph_renderer = from_networkx(graph=G, layout_function=graphviz_layout, prog='dot')
        graph_renderer.node_renderer.glyph = Circle(radius=3)

    return graph_renderer


def prepare_graph_figure():
    p = figure(
        toolbar_location='below',
        toolbar_sticky=False,
        resizable=True
    )
    p.toolbar.autohide = False
    p.toolbar.logo = None

    tools = prepare_tools()

    p.tools = tools

    return p


def get_netgraph(G: nx.classes.Graph, doc=None):
    import os
    p = prepare_graph_figure()

    doc.add_root(p)
    doc.theme = os.getenv('T_BOKEH_THEME')

    graph_renderer = prepare_graph_renderer(G)

    labels = prepare_labels(graph_renderer=graph_renderer)

    p.renderers.append(graph_renderer)
    p.renderers.append(labels)

    return p
