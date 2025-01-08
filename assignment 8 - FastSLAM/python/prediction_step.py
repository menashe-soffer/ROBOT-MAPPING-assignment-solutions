import numpy as np
from tools.normalize_angle import normalize_angle
import copy

def prediction_step(particles, odometry, particle_noise):

    num_particles = len(particles)
    odometry_noise = np.random.normal(size=(num_particles, 3), scale=particle_noise.T)

    r1 = odometry['r1'] + odometry_noise[:, 0]
    t = odometry['t'] + odometry_noise[:, 1]
    r2 = odometry['r2'] + odometry_noise[:, 2]

    for i, particle in enumerate(particles):

        particles[i]['history'].append(copy.copy(particles[i]['pose']))

        particles[i]['pose'][0] += t[i] * np.cos(r1[i] + particles[i]['pose'][2])
        particles[i]['pose'][1] += t[i] * np.sin(r1[i] + particles[i]['pose'][2])
        particles[i]['pose'][2] = normalize_angle(particles[i]['pose'][2] + r1[i] + r2[i])


    return particles
