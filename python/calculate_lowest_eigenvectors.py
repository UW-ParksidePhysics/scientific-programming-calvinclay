"""
Calculates lowest eigenvector and eigenvalue of a matrix.
"""

__author__ = 'Michael Hotchkiss and Calvin Clay'
import numpy as np 


def lowest_eigenvector(square_matrix, number_of_eigenvectors):
    """
    Takes a matrix and returns the eigenvalues and vectors
    :param square_matrix:
    :param number_of_eigenvectors:
    :return: eigen_values_sorted: ndarray,shape(K,)
    :return: eigenvectors_sorted: ndarray, shape(K,M)
    """
    eigen_values , eigenvectors = np.linalg.eig(square_matrix)
    eigen_values_sorted = np.sort(eigen_values)
    eigenvectors_sorted = eigenvectors[:, eigen_values.argsort()].transpose()
    return eigen_values_sorted[:number_of_eigenvectors], eigenvectors_sorted[:number_of_eigenvectors]



if __name__ == '__main__':
    array = np.array([[2,-1], [-1,2]])  # given array
    eigenvalues, eigenvectors = lowest_eigenvector(array, number_of_eigenvectors=2)  # number of eigenvalues
    print(eigenvectors, eigenvalues)  # should print lowest of the three
