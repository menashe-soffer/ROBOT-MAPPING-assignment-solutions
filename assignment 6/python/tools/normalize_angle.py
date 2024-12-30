import numpy as np

def normalize_angle(x):

    return ((x + np.pi) % (2 * np.pi)) - np.pi