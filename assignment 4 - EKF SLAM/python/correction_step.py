import numpy as np

def correction_step(mu, sigma, z, observedLandmarks):

    N = int((mu.size - 3) / 2)
    add_mu, add_sigma = np.zeros(mu.shape), np.zeros(sigma.shape)
    H = np.zeros((2*N, 3+2*N))
    Zdiff = np.zeros((2*N, 1))

    for zi in z:
        id, r, theta = zi['id'], zi['range'], zi['bearing']
        addr = 3 + 2 * (id - 1)
        if id not in observedLandmarks:
            # initialize the landmark position
            observedLandmarks.append(id)
            theta += mu[2] # convert to world
            mu[addr] = mu[0] + r * np.cos(theta)
            mu[addr + 1] = mu[1] + r * np.sin(theta)

        # calculate the expected measurement
        dxy = mu[addr:addr+2] - mu[:2]
        sq = np.linalg.norm(dxy) # expected range
        q = sq ** 2
        expected_Z = np.array([sq, np.arctan2(dxy[1], dxy[0]) - mu[2]])
        expected_Z[1] = expected_Z[1] % (2 * np.pi)

        # Compute the Jacobian Hi of the measurement function h for this observation
        Hi5 = (1 / q) * np.array([[-sq * dxy[0], -sq * dxy[1], 0, sq * dxy[0], sq * dxy[1]],
                                  [dxy[1], -dxy[0], -q, -dxy[1], dxy[0]]])
        Hi = np.zeros((2, 3+2*N))
        Hi[:, :3] = Hi5[:, :3]
        Hi[:, addr:addr+2] = Hi5[:, 3:]
        H[addr-3:addr+2-3, :] = Hi
        # Q = 0.01 * np.eye(2)
        # K = sigma @ Hi.T @ np.linalg.inv(Hi @ sigma @ Hi.T + Q)
        # print('\t', K[:7])

        Z = np.array((zi['range'], zi['bearing']))
        dz = (Z - expected_Z).reshape(2, 1)
        dz[1, 0] = dz[1, 0] % (2 * np.pi)
        dz[1, 0] = dz[1, 0] - 2 * np.pi if dz[1, 0] > np.pi else dz[1, 0]
        # print('\texpected_Z:', expected_Z)
        # print('\tZ:', Z)
        # print('\tdz:', dz.squeeze())
        # add_mu += (K @ dz).squeeze()
        # print('\tadd_mue', add_mu[:7])
        # add_sigma -= K @ Hi @ sigma
        Zdiff[addr-3:addr+2-3] = dz

    Q = 0.01 * np.eye(2*N)
    K = sigma @ H.T @ np.linalg.inv(H @ sigma @ H.T + Q)
    mu += (K @ Zdiff).squeeze()
    sigma = (np.eye(3+2*N) - K @ H) @ sigma


    return mu, sigma, observedLandmarks