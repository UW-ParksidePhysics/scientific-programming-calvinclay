from generate_matrix import generate_matrix
from calculate_lowest_eigenvectors import lowest_eigenvector
import numpy as np
import matplotlib.pyplot as plt

potential = 'square'
Ndim = 90
parameter = 100
matrix = generate_matrix(-10, 10, Ndim, potential, parameter)
print(matrix)
eigenvalues, eigenvectors = lowest_eigenvector(matrix, number_of_eigenvectors=3)
print(f'eigenvalues{eigenvectors}')
x = np.linspace(-10,10,90)
line1 = plt.plot(x, eigenvectors[0])
line2 = plt.plot(x, eigenvectors[1])
line3 = plt.plot(x, eigenvectors[2])
plt.show()