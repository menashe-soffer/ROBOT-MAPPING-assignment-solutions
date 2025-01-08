import copy

import numpy as np
#import matplotlib.pyplot as plt

from tools.read_data import read_data, read_world
from tools.plot_state import plot_state
from prediction_step import prediction_step
from correction_step import correction_step
from resample import resample

landmarks = read_world('../data/world.dat')
data = read_data('../data/sensor_data.dat')

print(len(landmarks))
num_landmarks = len(landmarks)
num_particles = 100
particle_noise = np.array([0.005, 0.01, 0.005]).reshape(3, 1)

fig = None
np.random.seed(1)

# initialize the particles
particles = []
for i in range(num_particles):
    particles.append(dict({'weight': 1. / num_particles,
                           'pose': np.zeros((3, 1)),
                           'history': [],
                           'landmarks': [dict({'observed': False,
                                               'mu': np.zeros((2, 1)),
                                               'sigma': np.zeros((2 ,2))}) for i in range(num_landmarks)]}))

for t in range(len(data)):

    print('time:', t)

    particles = prediction_step(particles, data[t]['odom'], particle_noise)

    particles = correction_step(particles, data[t]['sensor'])

    fig = plot_state(particles, landmarks, t, data[t]['odom'], fig)

    particles = resample(particles)




print('here')


