import numpy as np

def compute_sigma_points(mu, sigma, lambda_, alpha, beta):

    n = mu.size
    sigma_points = np.zeros((n, 2 * n + 1))

    # compute all sigma points
    sigma_points[:, 0] = mu
    cc = (n + lambda_) * sigma
    u, s, vt = np.linalg.svd(cc)
    c = u @ np.diag(np.sqrt(s))
    addr = 1
    for i in range(n):
        sigma_points[:, addr] = mu + c[:, i]
        sigma_points[:, addr + 1] = mu - c[:, i]
        addr = addr + 2

    w_m = np.zeros((2 * n + 1, 1))
    w_c = np.zeros((2 * n + 1, 1))
    w_m[0] = lambda_ / (lambda_ + n)
    w_c[0] = w_m[0] + 1 - alpha ** 2 + beta ** 2
    w_m[1:2*n+1] = 1 / (2 * (n + lambda_))
    w_c[1:2*n+1] = w_m[1:2*n+1]

    return sigma_points, w_m, w_c
