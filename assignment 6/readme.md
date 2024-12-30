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

![Alt text](https://github.com/menashe-soffer/ROBOT-MAPPING-assignment-solutions/blob/main/assignment%206/plots/eku_330_clean.png)


When adding noise and still doing only odometry, we get much noisier trace:
We observe irregularities in the estimated path, which is different from the clean estimation. While the first landmarks are estimated relatively good, subsequent landmarks are severely wrong because they are estimate using robot location with large accumulated error.
#### Note that in UKF, the variances cannot be updated if there is no correction step; they will expand and at some instance the sigma_points will be calculated too far from the centre, rendering them none useful and corrupting the state (mu) as well.

![Alt text](https://github.com/menashe-soffer/ROBOT-MAPPING-assignment-solutions/blob/main/assignment%206/plots/eku_330_noisy.png)


Now, with the noise, enable the correction step:
Note: I have modified both R and Q to values that seem to better describe the odometry and sensor noises.

![Alt text](https://github.com/menashe-soffer/ROBOT-MAPPING-assignment-solutions/blob/main/assignment%206/plots/eku_330.png)


#### now we see clearly the befit of the correction step
