import numpy as np
import matplotlib.pyplot as plt

def ls_calibrate_odometry(odom, scan):


    def jacobian(u_odom):

        J = np.zeros((3, 9))

        for i in range(3):
            J[i, (i * 3):((i+1) * 3)] = -u_odom

        return J

    # initial solution (identity), h vector and H matrix
    X = np.eye(3)
    b = np.zeros((9, 1))
    H = np.zeros((9, 9))
    num_steps = odom.shape[0]

    # build g and H
    for i in range(num_steps):
        e = scan[i] - odom[i]
        J = jacobian(odom[i])
        b += (e.T @ J).reshape(b.shape)
        H += J.T @ J

    # solve
    L = np.linalg.cholesky(H)
    y = np.linalg.solve(L, b)
    x = np.linalg.solve(L.T, y)
    deltaX = x.reshape(3, 3)
    X -= deltaX

    # Actualy the whole thing can be solve as simple MMSE
    # X = (scan.T @ odom) @ np.linalg.inv(odom.T @ odom)

    return X



def compute_trajectory(U):


    def v2t(v):

        c, s = np.cos(v[2]), np.sin(v[2])
        return np.array([[c, -s, v[0]], [s, c, v[1]], [0, 0, 1]])

    def t2v(t):

        return np.array([t[0, 2], t[1, 2], np.arctan2(t[1, 0], t[0, 0])])


    T = np.zeros((U.shape[0] + 1, 3))
    T[0, :] = 0
    currentPose = v2t(T[0])


    for i in range(U.shape[0]):

        currentPose = v2t(U[i]) @ currentPose
        T[i+1] = t2v(currentPose)

    return T



if __name__ == '__main__':


    # load the odometry measurements and scanmatchd data
    odom = np.loadtxt('../data/odom_motions')
    scan = np.loadtxt('../data/scanmatched_motions')

    X = ls_calibrate_odometry(odom, scan)
    print('calibration result', X)

    # apply the estimated calibration parameters
    C = odom @ X.T


    # # compute the current odometry trajectory, the scanmatch result, and the calibrated odom
    odom_trajectory = compute_trajectory(odom)
    scanmatch_trajectory = compute_trajectory(scan)
    calibrated_trajectory = compute_trajectory(C)

    # plot the trajectories
    plt.plot(odom_trajectory[:, 0], odom_trajectory[:, 1], label='Uncalibrated Odometry')
    plt.plot(scanmatch_trajectory[:, 0], scanmatch_trajectory[:, 1], label='Scan-Matching')
    plt.plot(calibrated_trajectory[:, 0], calibrated_trajectory[:, 1], label='Calibrated Odometry')
    plt.legend()
    plt.show()
