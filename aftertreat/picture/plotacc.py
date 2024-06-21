
import numpy as np
import os
import pandas as pd
import numpy
from dataprovision.beamset import BeamsetParameter
import math
from global_varible import c_light, Pi
from dataprovision.latticeparameter import LatticeParameter
import matplotlib.pyplot as plt
from apps.calacceptance import Acceptance

class PlotAcc(Acceptance):
    def __init__(self, project_path = None):
        self.project_path = project_path
        self.plt_path = os.path.join(project_path, "OutputFile", "BeamSet.plt")
        if project_path:
            self.latttice_mulp_path = os.path.join(project_path, 'InputFile', 'lattice_mulp.txt')
    def run(self, kind):
        loss_min_emit, _, _,  _  = self.cal_accptance(kind)

        self.plot(self.t_alpha, self.t_beta, self.t_gamma, loss_min_emit, self.loss_particles, kind)
        return 0

    def plot(self, alpha, beta, gamma, loss_min_emit, loss_particles, kind):

        fig, ax = plt.subplots()
        if kind == 0:
            loss_particles.plot(kind='scatter', x="x", y="xx", s=1, c='k', ax=ax)

            minx = loss_particles['x'].min() * 1.2
            miny = loss_particles['xx'].min() * 1.2

            maxx = loss_particles['x'].max() * 1.2
            maxy = loss_particles['xx'].max() * 1.2

        if kind == 1:
            loss_particles.plot(kind='scatter', x="y", y="yy", s=1, c='k', ax=ax)

            minx = loss_particles['y'].min() * 1.2
            miny = loss_particles['yy'].min() * 1.2

            maxx = loss_particles['y'].max() * 1.2
            maxy = loss_particles['yy'].max() * 1.2

        if kind == 2:
            loss_particles.plot(kind='scatter', x="z", y="zz", s=1, c='k', ax=ax)

            minx = loss_particles['z'].min() * 1.2
            miny = loss_particles['zz'].min() * 1.2

            maxx = loss_particles['z'].max() * 1.2
            maxy = loss_particles['zz'].max() * 1.2

        if kind == 3:
            loss_particles.plot(kind='scatter', x="phi", y="E", s=1, c='k', ax=ax)

            minx = loss_particles['phi'].min() * 1.2
            miny = loss_particles['E'].min() * 1.2

            maxx = loss_particles['phi'].max() * 1.2
            maxy = loss_particles['E'].max() * 1.2


        x = np.linspace(minx, maxx, 40)
        xp = np.linspace(miny, maxy, 40)


        # ax.set_ylim([-60, 60])
        # ax.set_xlim([-40, 40])
        x, xp = np.meshgrid(x, xp)
        ax.contour(x, xp, gamma * x ** 2 + 2 * alpha * x * xp + beta * xp ** 2,
                   [loss_min_emit], colors='r')
        plt.show()



if __name__ == "__main__":
    project_path = r"C:\Users\anxin\Desktop\test_acct"
    obj = PlotAcc(project_path)
    obj.run(1)