import networkx as nx
from gui.layout import GuiLayout

from networkx import Graph
from typing import Any


class MainWindow(GuiLayout):
    def __init__(self) -> None:
        super().__init__()

    def _draw_graph(self, G: Graph, ax) -> None:
        pos = nx.spring_layout(G, weight='weight')

        nx.draw_networkx_nodes(G, pos, node_size=200, node_color='blue', ax=ax, )

        nx.draw_networkx_edges(G, pos, width=2.0, edge_color='red', ax=ax, )

        # edge_labels = nx.get_edge_attributes(G, 'weight')
        # nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        nx.draw_networkx_labels(G, pos, font_size=5, font_color='black', font_weight='bold', ax=ax, )

    def draw_graph(self, mn: Any) -> None:
        G: Graph = nx.Graph()
        G.add_nodes_from(mn.nodes())
        G.add_edges_from(mn.edges())

        self.figure.clear()
        self._draw_graph(G, self.figure.add_subplot(111))
        # nx.draw(G, with_labels=True, font_weight='bold', ax=self.figure.add_subplot(111))
        self.canvas.draw()
