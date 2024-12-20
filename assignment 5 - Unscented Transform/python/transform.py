import numpy as np

def transform(points, sel):

    points = np.copy(points)

    if sel == 1:
        points[0, :] = points[0, :] + 1
        points[1, :] = points[1, :] + 2

    if sel == 2:
        x = points[0, :]
        y = points[1, :]
        r = np.linalg.norm(points, axis=0)
        theta = np.arctan2(y, x)
        points = np.array([r, theta])


    if sel==3:
        points[0, :] = points[0, :] * np.cos(points[0,:]) * np.sin(points[0,:])
        points[1, :] = points[1, :] * np.cos(points[1,:]) * np.sin(points[1,:])


    return points