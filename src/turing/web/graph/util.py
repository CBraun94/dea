from bokeh.models import LabelSet


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
