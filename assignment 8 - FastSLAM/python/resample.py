import copy

import numpy as np

def resample(particles):

    numParticles = len(particles)
    w = np.array([p['weight'] for p in particles]).squeeze()
    w /= w.sum()
    cs = np.cumsum(w)

    new_particles = []

    step = 1 / numParticles
    position = np.random.uniform(0, 1)
    i_src = 0

    for i_dst in range(numParticles):
        position += step
        if position > 1:
            position -= 1
            i_src = 0
        while position > cs[i_src]:
            i_src += 1
        #print(position, i_src)
        new_particles.append(copy.deepcopy(particles[i_src]))
        new_particles[-1]['weight'] = 1 / numParticles

    return new_particles


