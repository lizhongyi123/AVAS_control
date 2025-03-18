"""此文件为画相图"""
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import math
import random
import struct
from scipy.stats import gaussian_kde
from utils.readfile import read_dst_fast
from sklearn.neighbors import KernelDensity
import global_varible
import time
matplotlib.use("TkAgg")

class PlotPhase:
    def __init__(self, dst_path):
        self.dst_path = dst_path
        self.fig_size = (12.8, 9.2)
        self.fontsize = 14

    def run(self, show_, fig=None):
        try:
            res = read_dst_fast(self.dst_path)
        except Exception as e:
            print(f"Error reading file: {e}")
            return

        partran_dist = np.array(res['partran_dist'])

        # 限制最大点数以提高效率
        if len(partran_dist) > 10000:
            indices = np.random.choice(len(partran_dist), 10000, replace=False)
            partran_dist = partran_dist[indices]

        x = partran_dist[:, 0] * 10
        x1 = partran_dist[:, 1] * 1000
        y = partran_dist[:, 2] * 10
        y1 = partran_dist[:, 3] * 1000
        phi = partran_dist[:, 4] * 180 / global_varible.Pi
        E = partran_dist[:, 5]
        E -= np.mean(E)

        if not fig:
            fig = plt.figure(figsize=self.fig_size)

        font1 = {'family': 'Times New Roman', 'weight': 'bold', 'size': self.fontsize}

        # 绘制子图
        self._plot_density(fig, 221, x, x1, "x(mm)", "x'(mrad)", font1)
        self._plot_density(fig, 222, y, y1, "y(mm)", "y'(mrad)", font1)
        self._plot_density(fig, 223, phi, E, "φ(deg)", "Energy(MeV)", font1)
        self._plot_density(fig, 224, x, y, "x(mm)", "y(mm)", font1)

        if show_:
            plt.show()
        else:
            return fig

    def _plot_density(self, fig, position, x, y, xlabel, ylabel, font):
        ax = fig.add_subplot(position)
        xy = np.vstack([x, y]).T
        # if xlabel == "φ(deg)":
        #     bd = np.max(y)/100
        #     kde = KernelDensity(kernel='tophat', bandwidth=bd).fit(xy)
        # else:
        kde = KernelDensity(kernel='epanechnikov', bandwidth=0.07).fit(xy)
        # kde = KernelDensity(kernel='gaussian', bandwidth='scott').fit(xy)

        log_density = kde.score_samples(xy)
        z = np.exp(log_density)
        z /= max(z)  # 归一化

        scatter = ax.scatter(x, y, c=z, s=1.0, cmap='Spectral_r', vmin=0, vmax=1.0)
        fig.colorbar(scatter, ax=ax)
        ax.set_xlabel(xlabel, fontdict=font)
        ax.set_ylabel(ylabel, fontdict=font)
        ax.grid(linestyle="--")


if __name__ == "__main__":
    dst_path = r"C:\Users\anxin\Desktop\test_ini\OutputFile\outData_12.529930.dst"
    plot_phase = PlotPhase(dst_path)
    plot_phase.run(show_=True)

