from typing import Any

import numpy as np
import pandas as pd
from pgmpy.estimators import HillClimbSearch

from converters.to_pgmpy import info_matrix_2_markov_net


class CsvDataModel:
    def __init__(self, csv_file_path: str):
        _df = pd.read_csv(filepath_or_buffer=csv_file_path)
        self.df: pd.DataFrame = _df._get_numeric_data().select_dtypes(include=[float])
        self.mean_vector: pd.Series = self.df.mean()
        self.cov_matrix: pd.DataFrame = self.df.cov()
        self.cor_matrix: pd.DataFrame = self.df.corr()

        self.info_matrix: np.ndarray = np.linalg.inv(self.cor_matrix)

        self.titles = self.df.columns

    def gauss_markov_net(self, threshold: float = 0.5) -> Any:
        markov_net = info_matrix_2_markov_net(self.info_matrix, self.titles, threshold=threshold)
        return markov_net

    def bayes_net(self, discret_bins=5, scoring_method='bicscore', max_indegree=3):
        df = self.df.copy()
        for col in df.columns:
            df[col] = pd.cut(df[col], bins=discret_bins, labels=False)

        estimator = HillClimbSearch(df)

        net = estimator.estimate(scoring_method=scoring_method, max_indegree=max_indegree)
        return net


# if __name__ == '__main__':
#     model = CsvDataModel(csv_file_path='/Users/aliaksandrzyl/Desktop/projects/qtpgm/data/life expectancy.csv')
#
#     net = model.bayes_net()
#
#     import networkx as nx
#     import matplotlib.pyplot as plt
#
#     G = nx.DiGraph()
#     G.add_nodes_from(net.nodes())
#     G.add_edges_from(net.edges())
#     nx.draw(G, with_labels=True, font_weight='bold', arrows=True)
#
#     plt.show()
