import numpy as np
#import matplotlib.pyplot as plt

from tools.read_data import read_data, read_world
from tools.plot_state import plot_state
from prediction_step import prediction_step
from correction_step import correction_step

landmarks = read_world('../data/world.dat')
data = read_data('../data/sensor_data.dat')

add_odometry_noise = True
odometry_only = False

# add noise to the odometry data
if add_odometry_noise:
    for i in range(len(data)):
        data[i]['odom']['r1'] += 0.02 * np.random.normal()
        data[i]['odom']['r2'] += 0.02 * np.random.normal()
        data[i]['odom']['t'] += 0.2 * np.random.normal()

mu = np.zeros((3, 1))
sigma = 0.001 * np.eye(3)

fig, trace = None, []
observedLandmarks = []


for t in range(len(data)):

    print(t)
    # Perform the prediction step of the EKF
    mu, sigma = prediction_step(mu, sigma, data[t]['odom'], no_sigma_update=odometry_only)

    # % Perform the correction step of the EKF
    mu, sigma, observedLandmarks = correction_step(mu, sigma, data[t]['sensor'], observedLandmarks, no_update=odometry_only)
    #
    # %Generate visualization plots of the current state of the filter
    fig, trace = plot_state(mu, sigma, landmarks, t+1, observedLandmarks, data[t]['sensor'], fig, trace)
    fig.savefig('../plots/eku_{:03d}.png'.format(t), format='PNG')
