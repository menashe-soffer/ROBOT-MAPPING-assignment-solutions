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




def plot_state(particles, landmarks, timestep, z, fig):

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

    sel = np.argmax([p['weight'] for p in particles])
    #print('SEL', sel)

    # plot all particles
    all_poses = np.array([p['pose'] for p in particles])[:, :2].squeeze()
    ax.scatter(all_poses[:, 0], all_poses[:, 1], marker='.', c='g', s=6)

    # robot position and viewing lines
    ax.scatter(particles[sel]['pose'][0], particles[sel]['pose'][1], marker='o', c='r', s=16)

    # plot robot trace
    trace = np.array([p for p in particles[sel]['history']])[:, :2].squeeze()
    if len(trace) > 2:
        ax.plot(trace[:, 0], trace[:, 1], color='r')

    # plot estimated landmarks
    for lmark in particles[sel]['landmarks']:
        cent, covar = lmark['mu'], lmark['sigma']
        plot_conf_ellipse(cent, covar, ax, alpha=1, color='b')


    plt.draw_all()
    plt.pause(0.1)

    return fig#, trace