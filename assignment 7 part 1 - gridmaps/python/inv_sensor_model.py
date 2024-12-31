import numpy as np
from tools.tools import v2t, t2v, prob_to_log_odds, world_to_map_coordinates


def robotlaser_as_cartesian(rl):

    valid_mask = rl['ranges'] < rl['maximum_range']

    numBeams = rl['ranges'].size
    angles = np.linspace(rl['start_angle'], rl['start_angle'] + numBeams * rl['angular_resolution'], numBeams)
    points = np.array([rl['ranges'] * np.cos(angles) , rl['ranges'] * np.sin(angles) , np.ones((numBeams))])
    transf = v2t(rl['laser_offset'])

    return transf @ points[:, valid_mask]






def inv_sensor_model(map, scan, robPose, gridSize, offset, probOcc, probFree):

    # inputs:
    # map is the matrix containing the occupancy values (IN LOG ODDS) of each cell in the map.
    # scan is a laser scan made at this time step. Contains the range readings of each laser beam.
    # gridSize is the size of each grid in meters.
    # offset = [offsetX; offsetY] is the offset that needs to be subtracted from a point when converting to map coordinates.
    # probOcc is the probability that a cell is occupied by an obstacle given that a laser beam endpoint hit that cell.
    # probFree is the probability that a cell is occupied given that a laser beam passed through it.
    # outputs:
    # mapUpdate is a matrix of the same size as map. It has the log odds values that need to be added for the cell
    #            affected by the current laser scan. All unaffected cells should be zeros.
    # robPoseMapFrame is the pose of the robot in the map coordinates frame.
    # laserEndPntsMapFrame are map coordinates of the endpoints of each laser beam (also used for visualization purposes).


    # robot location in map
    robTrans = v2t(robPose)
    robPoseMapFrame = world_to_map_coordinates(robPose[:2].reshape(2, 1), gridSize, offset).squeeze()

    # range readings in map
    laserEndPnts = robotlaser_as_cartesian(scan)
    laserEndPnts = robTrans @ laserEndPnts
    laserEndPntsMapFrame = world_to_map_coordinates(laserEndPnts[:2,:], gridSize, offset)

    # init update map
    mapUpdate, freeCellsMask, occCellsMask = np.zeros(map.shape), np.zeros(map.shape), np.zeros(map.shape)

    for sc in range(laserEndPntsMapFrame.shape[1]):

        # all cells between robot and laser detected range are free cells
        delta = laserEndPntsMapFrame[:, sc] - robPoseMapFrame
        distance = np.linalg.norm(delta)
        step = delta / distance
        for s in range(1, int(distance)):
            XY = np.round(robPoseMapFrame + s * step).astype(int)
            freeCellsMask[XY[0], XY[1]] = 1

        # mark cell at range as occ
        XY = np.round(laserEndPntsMapFrame[:, sc]).astype(int)
        occCellsMask[XY[0], XY[1]] = 1

    mapUpdate += prob_to_log_odds(probFree) * freeCellsMask
    mapUpdate += prob_to_log_odds(probOcc) * occCellsMask

    return mapUpdate, robPoseMapFrame, laserEndPntsMapFrame








