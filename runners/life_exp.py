import pandas as pd
import numpy as np

from converters.to_pgmpy import info_matrix_2_markov_net

df = pd.read_csv(filepath_or_buffer='./life expectancy.csv')
df = df._get_numeric_data().select_dtypes(include=[float])

# df = df[['Unemployment', 'Corruption']]

# Filter the data leaving only quantitative variables

# Create the mean vector
mean_vector = df.mean()
# Create the covariance matrix
cov_matrix = df.cov()

# Create the correlation matrix
cor_matrix = df.corr()

# Create the information matrix
info_matrix = np.linalg.inv(cor_matrix)

print(info_matrix)

titles = df.columns

markov_net = info_matrix_2_markov_net(info_matrix, titles, threshold=0.5)

# visualise the markov net
import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
G.add_nodes_from(markov_net.nodes())
G.add_edges_from(markov_net.edges())
nx.draw(G, with_labels=True, font_weight='bold')
plt.show()


# # show 2d gaussian distribution using the mean and covariance matrix
# import matplotlib.pyplot as plt
# from scipy.stats import multivariate_normal
#
# x, y = np.mgrid[-10:30:0.1, -2:5:0.1]
# pos = np.empty(x.shape + (2,))
# pos[:, :, 0] = x
# pos[:, :, 1] = y
# rv = multivariate_normal(mean_vector.to_numpy(), cov_matrix.to_numpy())
# plt.contourf(x, y, rv.pdf(pos))
# plt.show()