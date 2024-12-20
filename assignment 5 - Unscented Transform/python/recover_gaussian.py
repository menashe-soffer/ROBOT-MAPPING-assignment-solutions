import numpy as np

def recover_gaussian(sigma_points, w_m, w_c):


    mu = sigma_points @ w_m

    d = sigma_points - mu
    sigma = np.zeros((2, 2))
    for i in range(sigma_points.shape[1]):
        sigma += w_c[i] * d[:, i:i+1] @ d[:, i:i+1].T

    return mu, sigma