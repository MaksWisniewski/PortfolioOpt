import numpy as np


def semi_variance(X):
    '''X is 2-dimensional array,
    this function returns 1-dimensional array
    containing semi-variances of each row of X'''

    X_mean = X.mean(axis=1).reshape(-1,1)
    X_diff = X - X_mean
    X_diff[X > X_mean] = 0
    return np.sum(X_diff**2, axis=1)
