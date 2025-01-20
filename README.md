# Jupiter's Resonances
This program simulate the Jupiter's resonance with his moons. This resonance is 1:2:4 Ganymede, Europe and Io. In this program we start with Jupyter in the center and all the moons situated in the x axis and the distance with Jupiter is the mean orbital radius. The velocity of each moon at the start is the same as if they make circular orbits around Jupyter. The simulation is a N-body simulation that takes 20 000 years. The objective is see how the periods change over the time and the method to calculate this is seeing when a moon passes through her periapsis. The method use for solving the differential equation is a RK5 with complex coefficients (https://arxiv.org/pdf/2110.04402)

## Jupiter.py
It is the code that makes the simulation over 20 000 years. It gives some archives with the positions and velocities of the bodies in differents times. Each archive have the data of 10 000 days.

## Period.py
It is the code that calculates when the periapsis have happened. It takes the archives produce by Jupyter.py and gives one archive whith the information of when have happened the periapsis.

## RK5_complex.py
It is a function that make a RK5 with complex coefficients. For more information see https://arxiv.org/pdf/2110.04402
