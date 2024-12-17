import numpy as np
import matplotlib.pyplot as plt

from tools.read_world import read_world
from tools.read_data import read_data
from tools.plot_state import plot_state
from prediction_step import prediction_step
from correction_step import correction_step

landmarks = read_world('../data/world.dat');
data = read_data('../data/sensor_data.dat');

N = len(landmarks)
print(N)
INF = 1000;

mu = np.zeros(2*N+3)
sigma = np.zeros((3+2*N, 3+2*N))
sigma[3:, 3:] = INF * np.eye(2*N)

fig, trace = None, []
observedLandmarks = []

for t in range(len(data)):

    print(t)
    # Perform the prediction step of the EKF
    mu, sigma = prediction_step(mu, sigma, data[t]['odom'])

    # % Perform the correction step of the EKF
    mu, sigma, observedLandmarks = correction_step(mu, sigma, data[t]['sensor'], observedLandmarks)
    #
    # %Generate visualization plots of the current state of the filter
    fig, trace = plot_state(mu, sigma, landmarks, t+1, observedLandmarks, data[t]['sensor'], fig, trace)
    fig.savefig('../plots/ekf_{:03d}.jpg'.format(t), format='JPEG')
