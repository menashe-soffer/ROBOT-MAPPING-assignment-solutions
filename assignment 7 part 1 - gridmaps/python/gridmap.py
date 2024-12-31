import numpy as np
from tools.tools import *
from tools.plot_map import plot_map
from inv_sensor_model import inv_sensor_model

laser = raedLaser()
print(len(laser))

# parameters
prior = 0.50 # prior occupancy probability
probOcc, probFree = 0.9, 0.35 # single reading probabilities
gridSize = 0.5 # gridmap resolution (meters)
border = 30 # range of map beyond robot path (meters)

# generating the empty map
poses = np.array([l['pose'] for l in laser]).squeeze()
robXMin, robXMax = min(poses[:, 0]), max(poses[:, 0])
robYMin, robYMax = min(poses[:, 1]), max(poses[:, 1])
mapBox = [robXMin-border, robXMax+border, robYMin-border, robYMax+border]
offsetX, offsetY = mapBox[0], mapBox[2]
offset = np.array([offsetX, offsetY]).reshape(2, 1)
mapSizeMeters = np.array([mapBox[1]-offsetX, mapBox[3]-offsetY])
mapSize = np.ceil(mapSizeMeters / gridSize).astype(int)
map = prob_to_log_odds(prior) * np.ones(mapSize)

for t, sc in enumerate(laser):

    robPose = poses[t]

    mapUpdate, robPoseMapFrame, laserEndPntsMapFrame = inv_sensor_model(map, sc, robPose, gridSize, offset, probOcc, probFree)
    mapUpdate -= prob_to_log_odds(prior) * np.ones(map.shape)
    map += mapUpdate

    plot_map(map, mapBox, robPoseMapFrame, poses, laserEndPntsMapFrame, gridSize, offset, t)


