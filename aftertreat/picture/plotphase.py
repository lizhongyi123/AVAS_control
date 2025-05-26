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
# matplotlib.use("TkAgg")
from utils.griddensity import grid_density
from matplotlib.colors import LinearSegmentedColormap
import time
import matplotlib.style as mplstyle
mplstyle.use('fast')


class PlotPhase:
    def __init__(self, dst_path):
        self.dst_path = dst_path
        self.fig_size = (12.8, 9.2)
        self.fontsize = 14
        self.gird_bins = 100
        self.maxpar_num = 10**4
    def run(self, show_, fig=None, save_path=None):
        t0 = time.time()
        res = read_dst_fast(self.dst_path)

        partran_dist = np.array(res['partran_dist'])

        # 限制最大点数以提高效率
        # if len(partran_dist) >= self.maxpar_num:
        #     indices = np.random.choice(len(partran_dist),  self.maxpar_num, replace=False)
        #     partran_dist = partran_dist[indices]

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
        t1 = time.time()
        print(t1-t0)
        if show_:
            plt.show()
            t2 =time.time()

            return None
        else:
            if save_path:  # 如果指定了保存路径，就保存图像
                fig.savefig(save_path)
            plt.close(fig)  # 释放资源，防止内存堆积
            return fig  # 返回 fig 方便外部进一步处理（可选）

    # def _plot_density(self, fig, position, x, y, xlabel, ylabel, font):
    #     ax = fig.add_subplot(position)
    #     xy = np.vstack([x, y]).T
    #     # if xlabel == "φ(deg)":
    #     #     bd = np.max(y)/100
    #     #     kde = KernelDensity(kernel='tophat', bandwidth=bd).fit(xy)
    #     # else:
    #     kde = KernelDensity(kernel='gaussian', bandwidth="scott").fit(xy)
    #     # kde = KernelDensity(kernel='gaussian', bandwidth='scott').fit(xy)
    #
    #     log_density = kde.score_samples(xy)
    #     z = np.exp(log_density)
    #     z /= max(z)  # 归一化
    #
    #     scatter = ax.scatter(x, y, c=z, s=1.0, cmap='Spectral_r', vmin=0, vmax=1.0)
    #     fig.colorbar(scatter, ax=ax)
    #     ax.set_xlabel(xlabel, fontdict=font)
    #     ax.set_ylabel(ylabel, fontdict=font)
    #     ax.grid(linestyle="--")
    def _plot_density(self, fig, position, x, y, xlabel, ylabel, font):
        t0 = time.time()
        ax = fig.add_subplot(position)

        # 设置网格数，比如 100x100，可调整


        # 计算 2D 直方图
        z = grid_density(x, y, self.gird_bins, norm=True)
        # 画密度图
        colors = [(1, 1, 1), *plt.cm.jet(np.linspace(0, 1, 256))]  # 第一个颜色为白色，其余为 'jet'
        custom_cmap = LinearSegmentedColormap.from_list('custom_jet', colors)

        scatter = ax.scatter(x, y, c=z, s=1.0, cmap=custom_cmap, vmin=0, vmax=1.0)
        fig.colorbar(scatter, ax=ax)
        ax.set_xlabel(xlabel, fontdict=font)
        ax.set_ylabel(ylabel, fontdict=font)
        ax.grid(linestyle="--")


if __name__ == "__main__":

    dst_path = r"C:\Users\shliu\Desktop\新建文件夹 (2)\outData_3.192000.dst"
    # dst_path =r"C:\Users\shliu\Desktop\boun\part_dtl1.dst"
    plot_phase = PlotPhase(dst_path)

    plot_phase.run(show_=True)

