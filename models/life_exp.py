from typing import Any

import numpy as np
import pandas as pd

from converters.to_pgmpy import info_matrix_2_markov_net


class LifeExpModel:
    def __init__(self, data_file: str):
        _df = pd.read_csv(filepath_or_buffer=data_file)
        self.df: pd.DataFrame = _df._get_numeric_data().select_dtypes(include=[float])
        self.mean_vector: pd.Series = self.df.mean()
        self.cov_matrix: pd.DataFrame = self.df.cov()
        self.cor_matrix: pd.DataFrame = self.df.corr()

        self.info_matrix: np.ndarray = np.linalg.inv(self.cor_matrix)

        self.titles = self.df.columns
        self.markov_net: Any = self.build_markov_net(threshold=0.5)

    def build_markov_net(self, threshold: float = 0.5) -> Any:
        self.markov_net = info_matrix_2_markov_net(self.info_matrix, self.titles, threshold=threshold)
        return self.markov_net

# if __name__ == '__main__':
#     model = LifeExpModel(data_file='/Users/aliaksandrzyl/Desktop/projects/qtpgm/data/life expectancy.csv')
#     model.build_markov_net(threshold=0.5)
#
#     # visualise the markov net
#     import networkx as nx
#     import matplotlib.pyplot as plt
#
#     G = nx.Graph()
#     G.add_nodes_from(model.markov_net.nodes())
#     G.add_edges_from(model.markov_net.edges())
#     nx.draw(G, with_labels=True, font_weight='bold')
#
#     plt.show()
