import numpy as np
import matplotlib.pyplot as plt


def drawprobellipse(cent, covar, ax, alpha=1, color='b'):

    def draw_ellipse(cent, angle, a, b, color, ax):

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


