import numpy as np
from tools.normalize_angle import normalize_angle



def measurement_model(particle_mu, landmark_mu):

    expected_range = np.linalg.norm(landmark_mu - particle_mu[:2, :])
    expectedBearing = normalize_angle(np.arctan2(landmark_mu[1] - particle_mu[1], landmark_mu[0] - particle_mu[0]) - particle_mu[2]).squeeze()
    expected_z = np.array((expected_range, expectedBearing)).reshape(2, 1)

    H = np.zeros((2, 2))
    H[0, 0] = (landmark_mu[0] - particle_mu[0]) / expected_range
    H[0, 1] = (landmark_mu[1] - particle_mu[1]) / expected_range
    H[1, 0] = -H[0, 1] / expected_range
    H[1, 1] = H[0, 0] / expected_range

    return expected_z, H





def correction_step(particles, z):

    # particles is particle list
    # z is a list of measurements

    Q = 0.01 * np.eye(2) # measurement noise


    for pidx, particle in enumerate(particles):

        # expected z
        p_x, p_y, p_bearing = particle['pose']
        for zi in z:
            z_id, z_range, z_bearing = zi['id'], zi['range'], zi['bearing']
            z_id -= 1

            if not particle['landmarks'][z_id]['observed']:

                # new landmark
                x = p_x + z_range * np.cos(p_bearing + z_bearing)
                y = p_y + z_range * np.sin(p_bearing + z_bearing)
                particle['landmarks'][z_id]['mu'] = np.array((x, y)).reshape(2, 1)

                expected_z, H = measurement_model(particle_mu=particle['pose'], landmark_mu=particle['landmarks'][z_id]['mu'])
                particle['landmarks'][z_id]['sigma'] = np.linalg.inv(H) @ Q @ np.linalg.inv(H).T
                particle['landmarks'][z_id]['observed'] = True

            else:

                # existing landmark
                expected_z, H = measurement_model(particle_mu=particle['pose'], landmark_mu=particle['landmarks'][z_id]['mu'])
                # measurement covariance
                covar = H @ particle['landmarks'][z_id]['sigma'] @ H.T + Q
                # kalman gain
                K = particle['landmarks'][z_id]['sigma'] @ H.T @ np.linalg.inv(covar)
                # diff between measurement and expected
                zdiff = np.array((z_range, z_bearing)).reshape(expected_z.shape) - expected_z
                # update landmark location
                particle['landmarks'][z_id]['mu'] += K @ zdiff
                # update uncertainty
                particle['landmarks'][z_id]['sigma'] -= K @ H @ particle['landmarks'][z_id]['sigma']
                # PATCH: don't let sigma collapse too much
                particle['landmarks'][z_id]['sigma'] *= max(1, 1e-2 * np.linalg.det(Q) / np.linalg.det(particle['landmarks'][z_id]['sigma']))

                # likelihood of this observation(s)
                particle['weight'] *= np.sqrt(1 / np.linalg.det(2 * np.pi * covar)) * np.exp(-0.5 * zdiff.T @ np.linalg.inv(covar) @ zdiff)

    return particles