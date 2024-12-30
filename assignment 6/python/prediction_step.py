import numpy as np
from tools.normalize_angle import normalize_angle
from compute_sigma_points import compute_sigma_points


def prediction_step(mu, sigma, u, no_sigma_update=False):

    if no_sigma_update:
        save_sigma = np.copy(sigma)

    r1, t, r2 = u['r1'], u['t'], u['r2']

    # compute sigma points
    sigma_points, w_m, w_c = compute_sigma_points(mu, sigma, lambda_=3, alpha=1, beta=2)

    # apply odometry input on sigma points
    sigma_points[0] += t * np.cos(sigma_points[2] + r1)
    sigma_points[1] += t * np.sin(sigma_points[2] + r1)
    sigma_points[2] += r1 + r2
    sigma_points[2] = normalize_angle(sigma_points[2])

    # compute new robot pose
    mu[:2] = (sigma_points[:2] @ w_m)
    mu[2] = normalize_angle(np.arctan2(np.sin(sigma_points[2]) @ w_m, np.cos(sigma_points[2]) @ w_m))

    # recover sigma
    d = sigma_points - mu.reshape(mu.size, 1)
    d[2] = normalize_angle(d[2])
    sigma = d @ (d.T * np.repeat(w_c, mu.size, 1))

    R3 = np.diag([0.01, 0.1, 0.01])
    sigma[:3, :3] += R3

    if no_sigma_update:
        sigma = save_sigma

    return mu, sigma




