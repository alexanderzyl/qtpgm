import numpy as np
from pgmpy.factors.discrete import DiscreteFactor
from pgmpy.models import MarkovNetwork
from typing import List


def info_matrix_2_markov_net(info_matrix: np.ndarray, titles: List[str], threshold: float = 0.0) -> MarkovNetwork:
    # Create the Markov Model
    model = MarkovNetwork()

    # Create the nodes
    for i in range(info_matrix.shape[0]):
        model.add_node(titles[i])
        factor = DiscreteFactor([titles[i]], [1], np.exp(-info_matrix[i, i]))
        model.add_factors(factor)

    # Create the edges
    for i in range(info_matrix.shape[0]):
        for j in range(i + 1, info_matrix.shape[0]):
            if abs(info_matrix[i, j]) > threshold:
                model.add_edge(titles[i], titles[j])
                factor = DiscreteFactor([titles[i], titles[j]], [1, 1], np.exp(-info_matrix[i, j]))
                model.add_factors(factor)

    # Check the model
    # print(model.check_model())

    return model
