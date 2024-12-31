import numpy as np



def v2t(x):

    M = np.zeros((3, 3))
    c, s = np.cos(x[2]), np.sin(x[2])
    M[:2, :2] = np.array([[c, -s], [s, c]]).squeeze()
    M[:2, 2] = x[:2].squeeze()
    M[2, 2] = 1

    return M


def t2v(M):

    v = np.zeros((3, 1))
    v[:2, 0] = M[:2, 2]
    v[2, 0] = np.arctan2(M[0, 1], M[0, 0])

    return v


def world_to_map_coordinates(pntsWorld, gridSize, offset):

    #n = pntsWorld.shape[1]
    return (pntsWorld - offset) / gridSize

def raedLaser(fname='../data/csail.log'):

    fd = open(fname, 'rt')
    laser = []
    for line in fd:
        #print(line)
        currentReading = dict()
        tokens = line.split()
        assert tokens[0] == 'ROBOTLASER1'
        currentReading['start_angle'], _ = float(tokens[2]), float(tokens[3])
        currentReading['angular_resolution'] = float(tokens[4])
        currentReading['maximum_range'] = float(tokens[5])
        num_readings = int(tokens[8])
        currentReading['ranges'] = np.array([float(tkn) for tkn in tokens[9:9+num_readings]])
        mdata_tokens = tokens[9+num_readings:]
        num_remissions = int(mdata_tokens[0])
        mdata_tokens = mdata_tokens[num_remissions:]
        laser_pose = np.array([float(tkn) for tkn in mdata_tokens[1:4]]).reshape(3, 1)
        currentReading['pose'] = np.array([float(tkn) for tkn in mdata_tokens[4:7]]).reshape(3, 1)
        currentReading['laser_offset'] = t2v(np.linalg.inv(v2t(currentReading['pose'])) @ v2t(laser_pose))
        currentReading['timestamp'] = float(mdata_tokens[12])
        laser.append(currentReading)

    fd.close()
    return laser


def prob_to_log_odds(p):

    p = np.maximum(np.minimum(p, 1 - 1e-6), 1e-6)
    return np.log(p) - np.log(1 - p)
def log_odds_to_prob(l):

    return 1 - 1 / (1 + np.exp(l))