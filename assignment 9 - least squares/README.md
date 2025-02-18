Assignment 9 is a very simple assignment, all the code in my solution is contained in a single pytion file.
a simple comparison between the "noisy" odometry and a corrected odometry to find a <b>linear</b> correction (a.k.a calibration) to the odometry.

#### comments: 

The linear square solution, as presented in the course, for this particular, problen, is overkill. there is no need to calculate the vector _<b>b</b>_ and and the matrix _<b>H</b>_.
it is a standard MMSE problem, which is solved simply by X = R<sub>XX</sub><sup>-1</sup> R<sub>XY</sub> (where x is the raw odometry data and y is the fixed data); this soulution is present and commented out in the python file

slides 20-26 are are slightly confusing because there is confusion between X and $\Delta X$. The procedure calculates $\Delta X$.


<img src="https://github.com/menashe-soffer/ROBOT-MAPPING-assignment-solutions/blob/main/assignment%209%20-%20least%20squares/plots/Adobe%20Express%20-%20file.png">
