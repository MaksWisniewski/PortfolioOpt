import numpy as np


def semi_covariance(X, Y):
    N = len(X)
    XX, YY = X - X.mean(), Y - Y.mean()
    XX[XX > 0] = 0
    YY[YY > 0] = 0
    return np.sum(XX * YY) / N


def semi_variance(X):
    return semi_covariance(X,X)


def semi_covariance_matrix(X):
    N,M = X.shape
    result = np.empty((M,M))
    for i in range(M):
        for j in range(M):
            result[i,j] = semi_covariance(X[:,i], X[:,j])
    return result
