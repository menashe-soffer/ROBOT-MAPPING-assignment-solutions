import numpy as np
from tools.normalize_angle import normalize_angle
from compute_sigma_points import compute_sigma_points, recover_gaussian


def add_new_point(mu, sigma, r, theta):

    # x = mu[0] + r * np.cos(theta + mu[2])
    # y = mu[1] + r * np.sin(theta + mu[2])
    mu = np.concatenate((mu, np.zeros((2, 1))))
    new_sigma = np.zeros((mu.size, mu.size))
    new_sigma[:-2, :-2] = sigma
    new_sigma[-2:, -2:] = 0.01 * np.eye(2)
    sigma = new_sigma

    sigma_points, w_m, w_c = compute_sigma_points(mu, sigma, 3, 1, 2)
    sigma_points[-2] = sigma_points[0] + r * np.cos(sigma_points[2] + theta)
    sigma_points[-1] = sigma_points[1] + r * np.sin(sigma_points[2] + theta)
    mu, sigma = recover_gaussian(sigma_points, w_m, w_c)

    return mu, sigma


def correction_step(mu, sigma, z, observedLandmarks, no_update=False):



    for zi in z:

        id, r, theta = zi['id'], zi['range'], zi['bearing']

        # extend the state if this landmark wasn't observed yet
        if id not in observedLandmarks:
            observedLandmarks.append(id)
            mu, sigma = add_new_point(mu, sigma, r, theta)

        else:

            if no_update:
                save_mu, save_sigma = np.copy(mu), np.copy(sigma)

            # calculate expected measurement
            sigma_points, w_m, w_c = compute_sigma_points(mu, sigma, 3, 1, 2)
            addr = 3 + np.argwhere(id == np.array(observedLandmarks)).squeeze() * 2
            dxy = sigma_points[addr:addr+2] - sigma_points[:2]
            sigma_r = np.linalg.norm(dxy, axis=0)
            sigma_theta = normalize_angle(np.arctan2(dxy[1], dxy[0]) - sigma_points[2])
            num_dim, num_sig = sigma_points.shape

            # expected measurement
            expected_range = sigma_r @ w_m
            expected_bearing = sigma_theta @ w_m
            Zi = np.array((expected_range, expected_bearing)).reshape(2, 1)

            # innovation covariance
            Z_i_preds = np.concatenate((sigma_r.reshape(1, num_sig), sigma_theta.reshape(1, num_sig)), axis=0)
            z_i_diff = Z_i_preds - Zi
            z_i_diff[1] = normalize_angle(z_i_diff[1])
            Q = 0.1 * np.eye(2)
            S = z_i_diff @ (np.repeat(w_c, 2, 1) * z_i_diff.T) + Q

            # cross-variance
            xdiff = sigma_points - mu
            xdiff[2] = normalize_angle(xdiff[2])
            Sxz = (np.repeat(w_c.T, num_dim, 0) * xdiff) @  z_i_diff.T

            # update
            K = Sxz @ np.linalg.inv(S)
            dz = np.array([r, theta]).reshape(2, 1) - Zi
            mu += K @ dz
            sigma -= K @ S @ K.T

            if no_update:
                mu, sigma = save_mu, save_sigma

    return mu, sigma, observedLandmarks


