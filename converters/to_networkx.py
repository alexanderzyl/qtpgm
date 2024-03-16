import networkx as nx
from networkx import Graph


def markov_net_2_networkx(markov_net: 'MarkovNet') -> Graph:
    graph = nx.Graph()
    graph.add_nodes_from(markov_net.nodes())
    graph.add_edges_from(markov_net.edges())
    return graph
