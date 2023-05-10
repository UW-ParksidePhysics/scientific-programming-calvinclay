from generate_matrix import generate_matrix
from calculate_lowest_eigenvectors import lowest_eigenvector
import numpy as np
from annotate_plot import annotate_plot
import matplotlib.pyplot as plt

matrix = generate_matrix(-10, 10, 90, 'Square', 100)
eigenvalue, eigenvector = lowest_eigenvector(matrix,3)
eigenvalues = eigenvalue[0:3]
eigenvectors = eigenvector[0:3]
x = np.linspace(-10,10,90)
labels = []
for i in range(0,3):
    labels.append(rf'$\psi_{i}, E_{i} $ = {eigenvalue[i]:.3f}a.u.')
plt.figure(figsize=(12,8))
line1 = plt.plot(x, eigenvectors[0])
line2 = plt.plot(x, eigenvectors[1])
line3 = plt.plot(x, eigenvectors[2])
plt.xlabel(r'$x$[a.u.]')
plt.ylabel(r'$\psi(x)$[a.u.]')
plt.legend(labels=labels, loc='upper right')
plt.ylim(-2*np.amax(eigenvectors), 2 * np.amax(eigenvectors))
plt.plot(x, np.linspace(0, 0, 90), color='black')
#plt.title()
name = 'Calvin Clay'
plt.annotate(f'Created by {name} {date.today().isoformat()}', (0,0), (-50, -25),
             xycoords='axes fraction', textcoords='offset points', va='top')

if display_graph:
    plt.show()
else:
    plt.savefig('Square.png')