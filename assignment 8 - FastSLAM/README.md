assignment 8 is about implementing SLAM using particle filter for the robot state, while landmark states for each particle are maintained with EKF.

The code here is as far as I have checked indeed implements the algorithm presented in the lecture.

#### the is a small typo, I beleive, in the lecture slides (e.g. slide 30 eq. 18) regarding the update of the weights, the RHS should multiply the existing weithgt, not override it.


I am not 100% satisfied with this version, I hope to make some updates in the future. 
#### The updates I hope to make are supposed to address the following observations:
* the dataset is the same one that is used for previous SLAM assignmnet, in that it does not reveal the true benefit of SLAM: the odomentry data is perfect, so that the correction step (sensor preocessing) actually deteriorates the results. in that respect I have added noise to the odometry in previous SLAM assignmnet, which I plan to add here as well.

* the assignmnet also does not utilize the strength of particle filter. the robot pose is at the origin in the begining, and there are no multimodal particle "groups" in any stage. I'll try to do something to modify it.
* The estimated landmark variances are inherently shrinking; there is no prediction step done on the landmark estimations that expands the variances, only correction that shrink it. the variance do not realy reprisent the uncertainty, we quicly get particles with wrong landmakrk locations yet very small covaruances, I have add artificial lower bound on variance.
* it is crutial that the variances are not way off: too high variance will "wash out" the differences amont the weights, to small variances will make the weights irrelevant.
* The output throughout most of the simulation cycle is very irritating, as there are many particles that evolved with wrong robot states (mainly orientation) but at the same time with landmark estimations that are in good agreement with the wrong robot state. those particle are dropped only during the last steps of the flow, when the robot "close loop" and re-observe landmarks that were observed before, so that the last ~50 time steps or so look nicer.
* 
