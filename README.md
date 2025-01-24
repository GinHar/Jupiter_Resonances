# Jupiter's Resonances
The program simulates the movement between Jupyter and his moons. The objetive is to calculate the period of the moons in different times and see that Io, Europe and Ganymedes are in a 1:2:4 resonance. To calculate the period, the distance between Jupyter and his moons is taken and it is calculated the FFT. The method use for solving the differential equation is a RK5 with complex coefficients (https://arxiv.org/pdf/2110.04402).


## Jupiter.py
It is the code that makes the simulation over 30 years. It gives some archives with the positions and velocities of the bodies in differents times. Each archive have the data of around 14 days. The archives that this code gives are save in the folder named Data.

## Period.py
It is the code that calculates the FFT of the distances and calculates the period of each moon. To do this takes the positions from the Data folder.

## RK5_complex.py
It is a function that make a RK5 with complex coefficients. For more information see https://arxiv.org/pdf/2110.04402

## Data folder
It is a folder where the data calculated from Jupyter.py is saved.
