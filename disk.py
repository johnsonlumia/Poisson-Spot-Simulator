#!usr/bin/python

#
# The main function to operate the Poisson Spot plot
#
# By Zhexing Zhang June 03 2018
#

import numpy as np
import matplotlib.pyplot as plt
import time

C = 299792458  # set the light speed
GRID_HOLE = 1500


class Poisson:
    def __init__(self, lamda=633e-9, rad=0.003, L=1.0, grid_l=200, screenl=0.008):
        self.lamda = lamda  # the wavelength of light
        self.rad = rad  # the radius of the disk
        self.L = L  # distance between the disk and the c=screen
        self.grid_r = int(grid_l * np.sqrt(2)) + 1  # grid of radius on the screen
        self.grid_l = grid_l  # grid of screen in x-y plane
        self.screenl = screenl  # half of length of one side of the screen
        # define the list of r, and corresponding intensity arrays
        self.r = np.linspace(0, screenl * np.sqrt(2),
                             self.grid_r)  # the distance from the origin to the endpoint is screenl * np.sqrt(2)
        self.list_int_r = np.zeros(self.grid_r)
        self.intxy = np.zeros((2 * self.grid_l, 2 * self.grid_l))
        # use complex number to define the points on the screen
        self.scnx = np.linspace(-screenl, screenl, 2 * self.grid_l)
        self.scny = np.linspace(-screenl, screenl, 2 * self.grid_l)
        self.scn = self.scnx + 1j * self.scny[:, None]
        # define a matrix of points taken outside the disk to calculate the overall intensity at points on the screen
        self.circlex = np.linspace(-2 * screenl, 2 * screenl, GRID_HOLE)
        self.circley = np.linspace(-2 * screenl, 2 * screenl, GRID_HOLE)
        self.circle = self.circlex + 1j * self.circley[:, None]
        self.out_circle = np.less(rad, np.abs(self.circle))  # matrix to judge if the points are outside the disk

    # define a function to calculate the pattern of the Poisson Spot
    def poiss(self):
        coeff = 2 * np.pi / self.lamda  # the coefficient of the phase is a constant
        # use the lists to plot the intensity in x-y plane
        rxy = np.abs(self.scn)  # calculate the distance of the points from the origin
        for i in range(self.grid_r):
            ri = self.r[-i]
            phase = coeff * np.sqrt(np.abs(
                self.circle - ri) ** 2 + self.L ** 2)  # the phase for each point outside the disk to the point at (ri, 0)
            complex_amplitude = np.exp(phase[self.out_circle] * 1j).sum()  # use the phase to find the amplitude
            int_point = np.abs(complex_amplitude)  # transform from complex number to intensity
            # put the intensity into the intensity matrix
            self.intxy[np.less(rxy,
                               ri + 0.2 * self.rad / self.grid_r)] = int_point  # add a small piece to r[i] to include points equal to r[i]
        return self.intxy

    # show the figure
    def showfig(self, intxy):
        f1, ax1 = plt.subplots()
        ax1.imshow(intxy, interpolation='none', cmap='gray')
        ax1.set_title('The Simulation of Poisson Spot on the Screen of Side Length 16 mm')
        ax1.set_xlabel('Position of Points in x axis')
        ax1.set_ylabel('Position of Points in y axis')
        return f1, ax1


if __name__ == '__main__':
    t0 = time.perf_counter()
    ex = Poisson()
    m = ex.poiss()
    fig, ax = ex.showfig(m)
    fig.savefig('disk.eps')
    t = time.perf_counter() - t0
    print(t)
