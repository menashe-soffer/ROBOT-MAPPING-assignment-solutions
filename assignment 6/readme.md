Assignment 5 is similar in its structure to assignment 4, but the solution should be done using different tool: UKF instead of EKF.
While the EKF the updated gaussians are calculated using a linearized version of the non-linear odometry and sensor data, in UKF they are estimated using “unscented transform”.

### I have already noticed in assignment 4, that the odometry data is very clean, and the sensor is not; the correction step actually deteriorates the prediction.

Here I have invested some time to confirm this observation.
For that I have added two switches to ukf_slam.py:
* add_odometry_noise = add noise to the odometry data
* odometry_only = skip all updates apart from updating the state mu 

when doing odometry only, with the original data, we are getting a very nice trace:
the estimated trace is nice and smooth. The estimated map is very close to the real map (tiny blue ellipses compared to black markers), meaning that when we 
first observed each landmark, the estimated robot location was very good.
