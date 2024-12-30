import numpy as np
from tools.normalize_angle import normalize_angle

def compute_sigma_points(mu, sigma, lambda_, alpha, beta):

    n = mu.size
    sigma_points = np.repeat(mu.reshape(n, 1), 2*n+1, 1)

    # compute all sigma points
    cc = (n + lambda_) * sigma
    u, s, vt = np.linalg.svd(cc)
    c = u @ np.diag(np.sqrt(s))
    sigma_points[:, 1:n+1] += c
    sigma_points[:, n+1:] -= c

    w_m = np.zeros((2 * n + 1, 1))
    w_c = np.zeros((2 * n + 1, 1))
    w_m[0] = lambda_ / (lambda_ + n)
    w_c[0] = w_m[0] + 1 - alpha ** 2 + beta ** 2
    w_m[1:2*n+1] = 1 / (2 * (n + lambda_))
    w_c[1:2*n+1] = w_m[1:2*n+1]

    return sigma_points, w_m, w_c


def recover_gaussian(sigma_points, w_m, w_c):

    mu = sigma_points @ w_m
    mu[2] = np.arctan2(np.sin(sigma_points[2]) @ w_m, np.cos(sigma_points[2]) @ w_m)

    d = sigma_points - mu
    d[2] = normalize_angle(d[2])
    sigma = d @ (d.T * np.repeat(w_c, mu.size, 1))

    return mu, sigma
