import numpy as np
import matplotlib.pyplot as plt


def plot_conf_ellipse(cent, covar, ax, alpha=1, color='b'):

    def draw_ellipse(cent, angle, a, b, color, fig):

        s = 2 * np.pi * np.linspace(0, 1, num=100)
        px, py = a * np.cos(s).reshape(1, 100), b * np.sin(s).reshape(1, 100)
        R = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
        pnts = cent.reshape(2, 1) + R @ np.concatenate((px, py), axis=0)
        ax.plot(pnts[0], pnts[1], c=color, linewidth=2)




    # calculate axes (half) length
    sxx, sxy, syy = covar[0, 0], covar[0, 1], covar[1, 1]
    a = np.sqrt(0.5 * (sxx + syy + np.sqrt((sxx - syy) ** 2 + 4 * sxy ** 2))) # longer
    b = np.sqrt(0.5 * (sxx + syy - np.sqrt((sxx - syy) ** 2 + 4 * sxy ** 2))) # smaller
    (a, b) = (b, a) if sxx < syy else (a, b)

    # # for case of neg. definite Cov (SHOULD NOT OCCUR!!!)
    # a, b = np.real(a), np.real(b)

    # Calculate inclination (numerically stable)
    if sxx != syy:
        angle = 0.5 * np.arctan(2*sxy/(sxx-syy))
    else:
        if sxy == 0:
            angle = 0     # angle doesn't matter , its a circle
        else:
            angle = np.sign(sxy) * np.pi / 4

    draw_ellipse(cent, angle, a*alpha, b*alpha, color, ax)




def plot_state(mu, sigma, landmarks, timestep, observedLandmarks, z, fig, trace):

    if fig is None:
        fig = plt.figure()
    fig.clf()
    ax = fig.gca()
    ax.grid(True)
    ax.set_title('timestep  {}'.format(timestep))
    ax.set_xlim((-2, 12))
    ax.set_ylim((-2, 12))
    ax.axis('square')

    ax.scatter([l['x'] for l in landmarks], [l['y'] for l in landmarks], marker='s', s=15, c='k')
    for id in observedLandmarks:
        addr = 3 + 2 * (id - 1)
        ax.scatter(mu[addr], mu[addr+1], marker='s', s=12, c='b')
        plot_conf_ellipse(mu[addr:addr+2], sigma[addr:addr+2, addr:addr+2], ax, alpha=1.35, color='b')

    # robot position and viewing lines
    ax.scatter(mu[0], mu[1], marker='o', c='r', s=12)
    plot_conf_ellipse(mu[:2], sigma[:2, :2], ax, alpha=1.35, color='r')

    for zi in z:
        addr = 3 + 2 * (zi['id'] - 1)
        ax.plot([mu[0], mu[addr]], [mu[1], mu[addr+1]], c='b', linewidth=1)

    trace.append(np.copy(mu[:2]))
    ax.plot([s[0] for s in trace], [s[1] for s in trace], c='r', linewidth=1)


    plt.draw_all()
    plt.pause(0.1)

    return fig, trace