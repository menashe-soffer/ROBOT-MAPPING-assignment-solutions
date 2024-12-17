import numpy as np

def prediction_step(mu, sigma, u):

    r1, t, r2 = u['r1'], u['t'], u['r2']

    # compute new robot pose
    theta = mu[2] + u['r1'] # direction for movement
    mu[0] += u['t'] * np.cos(theta)   # x
    mu[1] += u['t'] * np.sin(theta)   # y
    mu[2] += u['r1'] + u['r2'] # rotation
    mu[2] = mu[2] % (2 * np.pi)

    # localized Jacobian
    Gx = np.eye(3)
    Gx[0, 2] = -u['t'] * np.sin(theta)
    Gx[1, 2] = u['t'] * np.cos(theta)

    # update pose covariance
    R3 = np.diag([0.1, 0.1, 0.01])
    sigma[:3, :3] = Gx @ sigma[:3, :3] @ Gx.T + R3

    # update the robot-landmarks cross-covaraiances
    sigma[:3, 3:] = Gx @ sigma[:3, 3:]
    sigma[3:, :3] = sigma[:3, 3:].T

    return mu, sigma




