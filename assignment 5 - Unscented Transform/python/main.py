import numpy as np
import matplotlib.pyplot as plt
from drawprobellipse import drawprobellipse
from compute_sigma_points import compute_sigma_points
from transform import transform
from recover_gaussian import recover_gaussian

# arbitrary simple 2d gaussian
sigma = 0.1 * np.eye(2)
mu = np.array([1, 2])
n = mu.size

# set parameters for the unscented transform, Compute lambda_
alpha = 0.9
beta = 2
kappa = 1
lambda_ = alpha * alpha * (n+kappa) - n

# Compute the sigma points corresponding to mu and sigma
sigma_points, w_m, w_c = compute_sigma_points(mu, sigma, lambda_, alpha, beta)

# Draw original distribution with sampled sigma points
plt.scatter(mu[0], mu[1], marker='o', s=32, color='r', linewidth=3, label='original distribution')
drawprobellipse(mu, sigma, plt, 2.146, 'r')
plt.scatter(sigma_points[0,:], sigma_points[1,:], marker='x', s=12, color='k', linewidth=3)

for tfm_sel in range(1, 3+1):

    # transform the sigma_points, and estimate gaussian based on the transformed points
    sigma_points_trans = transform(sigma_points, tfm_sel)
    mu_trans, sigma_trans = recover_gaussian(sigma_points_trans, w_m, w_c)

    # Draw the transformed estimated gaussian
    plt.scatter(mu_trans[0], mu_trans[1], color='b', marker='o', s=32, linewidth=3, label='transformed distribution  ' + str(tfm_sel))
    drawprobellipse(mu_trans, sigma_trans, plt, 2.146, 'b');
    plt.scatter(sigma_points_trans[0, :], sigma_points_trans[1, :], color='k', marker='x', s=10, linewidth=3)

plt.xlim([-1, 6])
plt.ylim([-2, 5])
plt.grid(True)
ax = plt.gca()
ax.set_aspect('equal', adjustable='box')
plt.title('Unscented Transform')
ax.legend()
plt.savefig('../plots/5.png', format='PNG')
plt.show()




