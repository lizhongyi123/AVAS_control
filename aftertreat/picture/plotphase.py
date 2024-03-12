"""此文件为画相图"""
import numpy
import matplotlib.pyplot as plt
import math
import random
import struct
from scipy.stats import gaussian_kde



class PlotPhase():
    def __init__(self, inFileName):
        self.inFileName = inFileName
        self.fontsize = 14
    

    def run(self, show_):
        value = 2
        # plt.figure(figsize=(6.4*2, 4.6*2))

        f = open(self.inFileName, 'rb')
        f.read(2)

        data = struct.unpack("<i", f.read(4))
        number = int(data[0])

        data = struct.unpack("<d", f.read(8))
        Ib = float(data[0])

        data = struct.unpack("<d", f.read(8))
        freq = float(data[0])
        freq = freq

        f.read(1)

        partran_dist = numpy.arange(6 * number, dtype='float64').reshape(number, 6)

        for i in range(number):
            data = f.read(48)
            data = struct.unpack("<dddddd", data)
            partran_dist[i, 0] = data[0]
            partran_dist[i, 1] = data[1]
            partran_dist[i, 2] = data[2]
            partran_dist[i, 3] = data[3]
            partran_dist[i, 4] = data[4]
            partran_dist[i, 5] = data[5]

        data = struct.unpack("<d", f.read(8))
        BaseMassInMeV = data[0]
        f.close()


        xx = []
        yy = []
        E = []

        x_ = []
        y_ = []
        Phi = []
        for i in range(number):
            if(random.random() < value):
                xx.append(partran_dist[i, 0] * 10)
                x_.append(partran_dist[i, 1])
                yy.append(partran_dist[i, 2] * 10)
                y_.append(partran_dist[i, 3])
                Phi.append(partran_dist[i, 4])
                E.append(partran_dist[i, 5])

        #print(numpy.mean(E))   #能量

        for i in range(len(y_)):
            y_[i] = y_[i] * 1000
        for i in range(len(x_)):
            x_[i] = x_[i] * 1000

        #-------------------------------x-x'-----------------------
        x = numpy.array(xx)
        y = numpy.array(x_)

        xy = numpy.vstack([x, y])
        z = gaussian_kde(xy)(xy)

        idx = z.argsort()
        x, y, z = x[idx], y[idx], z[idx]
        maxcoloebar = 0
        for i in range(len(z)):
            if z[i] > maxcoloebar:
                maxcoloebar = z[i]

        for i in range(len(z)):
            z[i] = z[i] / maxcoloebar

        font1 = {'family': 'Times New Roman',
                'weight': 'bold',
                'size': self.fontsize}
        # plt.figure(figsize=(6.4 * 2, 4.8*2))、


        plt.subplot(221)
        plt.scatter(x, y, c=z, s=4.0, cmap='Spectral_r', vmin=0, vmax=1.0)
        plt.colorbar()
        plt.xlabel("x(mm)", font1)
        plt.ylabel("x'(mrad)", font1)
        plt.grid(linestyle="--")
        #plt.xlim([-5, 5])
        #plt.ylim([-0.7, 0.7])
        #plt.xticks([-4.0, -2.0, 0, 2.0, 4.0], fontsize=20,family='Times New Roman',weight = 'bold')
        #plt.yticks([-0.6, -0.3, 0, 0.3, 0.6], fontsize=20,family='Times New Roman',weight = 'bold')
        # plt.xticks(fontsize=14,family='Times New Roman',weight = 'bold')
        #plt.yticks([-2.0,-1.0,0,1.0,2.0],fontsize=20,family='Times New Roman',weight = 'bold')
        #-------------------------------------y-y'-----------------------
        x = numpy.array(yy)
        y = numpy.array(y_)

        xy = numpy.vstack([x, y])
        z = gaussian_kde(xy)(xy)

        # Sort the points by density, so that the densest points are plotted last
        idx = z.argsort()
        x, y, z = x[idx], y[idx], z[idx]

        maxcoloebar = 0
        for i in range(len(z)):
            if z[i] > maxcoloebar:
                maxcoloebar = z[i]

        for i in range(len(z)):
            z[i] = z[i] / maxcoloebar   #0.24776766316586    0.25533280078150344   0.25156341977740837   0.25007947389036805


        plt.subplot(222)
        plt.scatter(x, y, c=z, s=4.0, cmap='Spectral_r', vmin=0, vmax=1.0)
        plt.colorbar()
        plt.xlabel("y(mm)", font1)
        plt.ylabel("y'(mrad)", font1)
        plt.grid(linestyle="--")
        #plt.xlim([-6, 6])
        #plt.ylim([-0.9, 0.9])
        #plt.xticks([-4.0, -2.0, 0, 2.0, 4.0], fontsize=20,family='Times New Roman',weight = 'bold')
        #plt.yticks([-0.6, -0.3, 0, 0.3, 0.6], fontsize=20,family='Times New Roman',weight = 'bold')
        # plt.xticks(fontsize=20,family='Times New Roman',weight = 'bold')
        #plt.yticks([-2.0,-1.0,0,1.0,2.0],fontsize=20,family='Times New Roman',weight = 'bold')
        #-------------------------------------Phi-E-----------------------
        x = numpy.array(Phi)
        y = numpy.array(E)

        xy = numpy.vstack([x, y])
        z = gaussian_kde(xy)(xy)

        # Sort the points by density, so that the densest points are plotted last
        idx = z.argsort()
        x, y, z = x[idx], y[idx], z[idx]

        maxcoloebar = 0
        for i in range(len(z)):
            if z[i] > maxcoloebar:
                maxcoloebar = z[i]

        for i in range(len(z)):
            z[i] = z[i] / maxcoloebar   #0.24776766316586    0.25533280078150344   0.25156341977740837   0.25007947389036805




        plt.subplot(223)
        plt.scatter(x, y, c=z, s=4.0, cmap='Spectral_r', vmin=0, vmax=1.0)
        plt.colorbar()
        plt.xlabel("φ(rad)", font1)
        plt.ylabel("Energy(MeV)", font1)
        plt.grid(linestyle="--")
        #plt.xlim([-0.014, 0.014])
        #plt.ylim([619.75, 622.25])
        #plt.xticks([-0.01, -0.005, 0, 0.005, 0.01], fontsize=16,family='Times New Roman',weight = 'bold')
        #plt.yticks([620, 620.50, 621, 621.50, 622], fontsize=16,family='Times New Roman',weight = 'bold')
        #plt.xticks([-0.08,-0.04,0.0,0.04,0.08,0.12],fontsize=20,family='Times New Roman',weight = 'bold')
        # plt.yticks(fontsize=20,family='Times New Roman',weight = 'bold')
        x = numpy.array(xx)
        y = numpy.array(yy)

        xy = numpy.vstack([x, y])
        z = gaussian_kde(xy)(xy)

        # Sort the points by density, so that the densest points are plotted last
        idx = z.argsort()
        x, y, z = x[idx], y[idx], z[idx]

        maxcoloebar = 0
        for i in range(len(z)):
            if z[i] > maxcoloebar:
                maxcoloebar = z[i]

        for i in range(len(z)):
            z[i] = z[i] / maxcoloebar   #0.24776766316586    0.25533280078150344   0.25156341977740837   0.25007947389036805




        plt.subplot(224)
        plt.scatter(x, y, c=z, s=4.0, cmap='Spectral_r', vmin=0, vmax=1.0)
        plt.colorbar()
        plt.xlabel("x(mm)", font1)
        plt.ylabel("y(mm)", font1)
        plt.grid(linestyle="--")
        #plt.xlim([-5, 5])
        #plt.ylim([-6, 6])
        #plt.xticks([-4.0, -2.0, 0, 2.0, 4.0], fontsize=20,family='Times New Roman',weight = 'bold')
        #plt.yticks([-4.0, -2.0, 0, 2.0, 4.0], fontsize=20,family='Times New Roman',weight = 'bold')
        # plt.xticks(fontsize=20,family='Times New Roman',weight = 'bold')
        # plt.yticks(fontsize=20,family='Times New Roman',weight = 'bold')
        # plt.savefig('figuren4.dst.png',dpi=400,bbox_inches='tight')
        # plt.tight_layout()
        if show_:
            plt.show()
            return None

        else:
            return None

if __name__ == "__main__":
    a = PlotPhase(r"C:\Users\anxin\Desktop\AVAS_control\user\user_qt\part_dtl1.dst")
    a.run(1)