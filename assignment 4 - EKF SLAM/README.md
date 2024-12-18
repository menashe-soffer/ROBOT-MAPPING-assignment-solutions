Assignment 4 is the first "real" coding assignmnet in the course.
A 2D EKF filter to track the path of a robot in 2D, with 9 landmarks.
The data (odometry and sensor readings in range/bearing format) is given in a single file in the data folder, as well as a file with ground trith landmark locations.
All the code is in the python folder.
### If you intend to run the code, don't forget to add an empty folder named plots into which the plots will be written.

#### comments:

1. In the original assignment, the guida was to stack all the observations from each step and proccess jointly (stack all observation Jacobian matrices Hi and calculate "joint" kalman gain). I the code I have made update for each observation seperately, thus only inverting 2x2 matrices. This follows the lecture notes, BTW. I confirmed that he results are indistinguishable.
2. In principle I have used the recomended noise variances, but I suspect they are not the best for the data: the motion (odometry) seems quite accurate, while the sensor data is very noisy. In fact, with the correction step, mainly the path seems to become eratic. with "infinite" observation variances (nulling kalman gain), the path looks much smoother and ends up in the same place.


here is the path with the original variances:

![ekf_330_0 01](https://github.com/user-attachments/assets/ff56aac5-0818-49d9-8e71-eb5aa297085f)

and here is the path with "infinite" sensor noise variance: 
(since the correction step is neutralized, the uncertainty ellipses are huge, though the actual locations are very accurate).
![ekf_330_100000000000 01](https://github.com/user-attachments/assets/df393a46-87b1-48fb-acbe-2bdb7ddd1466)



## maybe one day I will add odometry noise to make the excersize more illustrative.

