import pandas as pd
import numpy as np

df = pd.read_csv(filepath_or_buffer='./life expectancy.csv')
df = df._get_numeric_data().select_dtypes(include=[float])

df = df[['Unemployment', 'Corruption']]

# Filter the data leaving only quantitative variables

# Create the mean vector
mean_vector = df.mean()
# Create the covariance matrix
cov_matrix = df.cov()

# Create the correlation matrix
cor_matrix = df.corr()

print(cor_matrix)

# show 2d gaussian distribution using the mean and covariance matrix
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal

x, y = np.mgrid[-10:30:0.1, -2:5:0.1]
pos = np.empty(x.shape + (2,))
pos[:, :, 0] = x
pos[:, :, 1] = y
rv = multivariate_normal(mean_vector.to_numpy(), cov_matrix.to_numpy())
plt.contourf(x, y, rv.pdf(pos))
plt.show()