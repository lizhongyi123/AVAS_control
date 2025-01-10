"""此文件为画相图"""
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
class PlotPhase():
    def __init__(self, dst_path):
        self.dst_path = dst_path
        self.fontsize = 14

    

    def run(self, show_):
        # value = 2
        if show_:
            plt.figure(figsize=(6.4*2, 4.6*2))
        #
        # f = open(self.inFileName, 'rb')
        # f.read(2)
        #
        # data = struct.unpack("<i", f.read(4))
        # number = int(data[0])
        #
        # data = struct.unpack("<d", f.read(8))
        # Ib = float(data[0])
        #
        # data = struct.unpack("<d", f.read(8))
        # freq = float(data[0])
        # freq = freq
        #
        # f.read(1)
        #
        # partran_dist = numpy.arange(6 * number, dtype='float64').reshape(number, 6)
        #
        # for i in range(number):
        #     data = f.read(48)
        #     data = struct.unpack("<dddddd", data)
        #     partran_dist[i, 0] = data[0]
        #     partran_dist[i, 1] = data[1]
        #     partran_dist[i, 2] = data[2]
        #     partran_dist[i, 3] = data[3]
        #     partran_dist[i, 4] = data[4]
        #     partran_dist[i, 5] = data[5]
        #
        # data = struct.unpack("<d", f.read(8))
        # BaseMassInMeV = data[0]
        # f.close()
        #
        #
        # xx = []
        # yy = []
        # E = []
        #
        # x_ = []
        # y_ = []
        # Phi = []
        # for i in range(number):
        #     if(random.random() < value):
        #         xx.append(partran_dist[i, 0] * 10)
        #         x_.append(partran_dist[i, 1])
        #         yy.append(partran_dist[i, 2] * 10)
        #         y_.append(partran_dist[i, 3])
        #         Phi.append(partran_dist[i, 4])
        #         E.append(partran_dist[i, 5])
        #
        # #print(numpy.mean(E))   #能量
        #
        # for i in range(len(y_)):
        #     y_[i] = y_[i] * 1000
        # for i in range(len(x_)):
        #     x_[i] = x_[i] * 1000
        #
        #
        # #-------------------------------x-x'-----------------------
        # x = numpy.array(xx)
        # y = numpy.array(x_)

        res = read_dst_fast(self.dst_path)

        partran_dist = np.array(res['partran_dist'])

        if len(partran_dist) > 10000:
            indices = np.random.choice(len(partran_dist), 10000, replace=False)
            x = np.array([i[0] * 10 for i in partran_dist])[indices]
            x1 = np.array([i[1] * 1000 for i in partran_dist])[indices]
            y = np.array([i[2] * 10 for i in partran_dist])[indices]
            y1 = np.array([i[3] * 1000 for i in partran_dist])[indices]
            phi = np.array([i[4] * 180/global_varible.Pi for i in partran_dist])[indices]
            E = np.array([i[5] for i in partran_dist])[indices]
            E = E - np.mean(E)

        else:
            x = np.array([i[0] * 10 for i in partran_dist])
            x1 = np.array([i[1] * 1000 for i in partran_dist])
            y = np.array([i[2] * 10 for i in partran_dist])
            y1 = np.array([i[3] * 1000 for i in partran_dist])
            phi = np.array([i[4] * 180/global_varible.Pi for i in partran_dist])
            E = np.array([i[5] for i in partran_dist])
            E = E - np.mean(E)

        xx1 = np.vstack([x, x1]).T
        kde = KernelDensity(kernel='epanechnikov', bandwidth="scott").fit(xx1)
        log_density = kde.score_samples(xx1)
        z = np.exp(log_density)


        max_z = max(z)
        z = [i / max_z for i in z]


        font1 = {'family': 'Times New Roman',
                'weight': 'bold',
                'size': self.fontsize}



        plt.subplot(221)
        plt.scatter(x, x1, c=z, s=1.0, cmap='Spectral_r', vmin=0, vmax=1.0)
        plt.colorbar()
        plt.xlabel("x(mm)", font1)
        plt.ylabel("x'(mrad)", font1)
        plt.grid(linestyle="--")




        yy1 = np.vstack([y, y1]).T
        kde = KernelDensity(kernel='epanechnikov', bandwidth="scott").fit(yy1)
        log_density = kde.score_samples(yy1)
        z = np.exp(log_density)
        max_z = max(z)
        z = [i / max_z for i in z]

        plt.subplot(222)
        plt.scatter(y, y1, c=z, s=1.0, cmap='Spectral_r', vmin=0, vmax=1.0)
        plt.colorbar()
        plt.xlabel("y(mm)", font1)
        plt.ylabel("y'(mrad)", font1)
        plt.grid(linestyle="--")






        phiE = np.vstack([phi, E]).T
        kde = KernelDensity(kernel='epanechnikov', bandwidth="scott").fit(phiE)
        log_density = kde.score_samples(phiE)
        z = np.exp(log_density)
        max_z = max(z)
        z = [i / max_z for i in z]


        plt.subplot(223)
        plt.scatter(phi, E, c=z, s=1.0, cmap='Spectral_r', vmin=0, vmax=1.0)
        plt.colorbar()
        plt.xlabel("φ(deg)", font1)
        plt.ylabel("Energy(MeV)", font1)
        plt.grid(linestyle="--")



        xy = np.vstack([x, y]).T
        kde = KernelDensity(kernel='epanechnikov', bandwidth="scott").fit(xy)
        log_density = kde.score_samples(xy)
        z = np.exp(log_density)
        max_z = max(z)
        z = [i / max_z for i in z]

        plt.subplot(224)
        plt.scatter(x, y, c=z, s=1.0, cmap='Spectral_r', vmin=0, vmax=1.0)
        plt.colorbar()
        plt.xlabel("x(mm)", font1)
        plt.ylabel("y(mm)", font1)
        plt.grid(linestyle="--")



        if show_:
            plt.show()
            return None

        else:
            return None

if __name__ == "__main__":
    a = PlotPhase(r"E:\E\空间电荷效应\shutuan81\不同磁场测试\0.2\outData_0.000000.dst")
    a.run(1)