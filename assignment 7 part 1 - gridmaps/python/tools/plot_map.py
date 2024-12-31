import numpy as np
import matplotlib.pyplot as plt
from tools.tools import log_odds_to_prob, world_to_map_coordinates

def plot_map(map, mapBox, robPoseMapFrame, poses, laserEndPntsMapFrame, gridSize, offset, t):

    plt.clf()
    #plt.title('frame  {}'.format(t))
    xtics = np.linspace(0, map.shape[0]-1, num=7)
    xlabels = np.round(mapBox[0] + xtics * (mapBox[1] - mapBox[0]) / map.shape[0], decimals=1)
    plt.xticks(xtics, xlabels)
    ytics = np.linspace(0, map.shape[1]-1, num=7)
    ylabels = np.round(mapBox[2] + xtics * (mapBox[3] - mapBox[2]) / map.shape[1], decimals=1)
    plt.yticks(ytics, ylabels)

    plt.imshow((np.ones(map.shape) - log_odds_to_prob(map)).T, cmap='gray')

    traj = poses[:t + 1, :2].T
    traj = world_to_map_coordinates(traj, gridSize, offset)
    plt.plot(traj[0, :], traj[1, :], c='g', linewidth=2)
    plt.scatter(robPoseMapFrame[0], robPoseMapFrame[1], c='b', marker='o', s=5, linewidth=4)
    plt.scatter(laserEndPntsMapFrame[0,:], laserEndPntsMapFrame[1,:], c='r', marker='o', s=2)

    plt.show(block=False)
    plt.savefig('../plots/gridmap_{:03d}.png'.format(t+1), format='PNG')
    plt.pause(0.01)

