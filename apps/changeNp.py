import numpy
import math
import struct
import random


class ChangeNp():
    """
    粒子数扩充
    """
    def __init__(self, inFileName, outFileName, radiox):
        self.inFileName = inFileName
        self.outFileName = outFileName
        self.radiox = radiox

    def run(self):
        radiox = self.radiox
        para = 0.15
        Intensity = 5.0

        C_light = 299792458
        particleData = []
        BaseMassInMeV = -1
        energy = -1
        phase = -1
        beta = -1
        gamma = -1

        f = open(self.inFileName, 'rb')

        tdata = struct.unpack("<c", f.read(1))
        char1 = str(tdata[0])


        tdata = struct.unpack("<c", f.read(1))
        char2 = str(tdata[0])


        tdata = struct.unpack("<i", f.read(4))
        number = int(tdata[0])


        tdata = struct.unpack("<d", f.read(8))
        Ib = float(tdata[0])

        #Ib = Intensity
        tdata = struct.unpack("<d", f.read(8))
        freq = float(tdata[0])


        tdata = struct.unpack("<c", f.read(1))
        char3 = str(tdata[0])


        xdata = numpy.arange(6 * number, dtype='float64').reshape(number, 6)

        for i in range(number):
            tdata = f.read(48)
            tdata = struct.unpack("<dddddd", tdata)
            xdata[i, 0] = tdata[0]
            xdata[i, 1] = tdata[1]
            xdata[i, 2] = tdata[2]
            xdata[i, 3] = tdata[3]
            xdata[i, 4] = tdata[4]
            xdata[i, 5] = tdata[5]

        tdata = struct.unpack("<d", f.read(8))
        BaseMassInMeV = tdata[0]

        f.close()

        ccxmin = float("inf")
        ccxmax = -float("inf")
        ccx1min = float("inf")
        ccx1max = -float("inf")

        ccymin = float("inf")
        ccymax = -float("inf")
        ccy1min = float("inf")
        ccy1max = -float("inf")

        cczmin = float("inf")
        cczmax = -float("inf")
        ccz1min = float("inf")
        ccz1max = -float("inf")
        for i in range(number):
            if (xdata[i, 0] < ccxmin):
                ccxmin = xdata[i, 0]
            if (xdata[i, 0] > ccxmax):
                ccxmax = xdata[i, 0]

            if (xdata[i, 1] < ccx1min):
                ccx1min = xdata[i, 1]
            if (xdata[i, 1] > ccx1max):
                ccx1max = xdata[i, 1]

            if (xdata[i, 2] < ccymin):
                ccymin = xdata[i, 2]
            if (xdata[i, 2] > ccymax):
                ccymax = xdata[i, 2]

            if (xdata[i, 3] < ccy1min):
                ccy1min = xdata[i, 3]
            if (xdata[i, 3] > ccy1max):
                ccy1max = xdata[i, 3]

            if (xdata[i, 4] < cczmin):
                cczmin = xdata[i, 4]
            if (xdata[i, 4] > cczmax):
                cczmax = xdata[i, 4]

            if (xdata[i, 5] < ccz1min):
                ccz1min = xdata[i, 5]
            if (xdata[i, 5] > ccz1max):
                ccz1max = xdata[i, 5]


        validdata = []
        for i in range(number):
            for j in range(radiox):
                tmp = []
                tmp.append(xdata[i, 0] + (random.random() - 0.5) * (ccxmax - ccxmin) * para)
                tmp.append(xdata[i, 1] + (random.random() - 0.5) * (ccx1max - ccx1min) * para)
                tmp.append(xdata[i, 2] + (random.random() - 0.5) * (ccymax - ccymin) * para)
                tmp.append(xdata[i, 3] + (random.random() - 0.5) * (ccy1max - ccy1min) * para)
                tmp.append(xdata[i, 4] + (random.random() - 0.5) * (cczmax - cczmin) * para)
                tmp.append(xdata[i, 5] + (random.random() - 0.5) * (ccz1max - ccz1min) * para)
                validdata.append(tmp)
        #--------------------------------------------------
        number = len(validdata)
        #--------------------------------------------------
        f = open(self.outFileName, 'wb')
        data = struct.pack('<B', 125)
        f.write(data)
        data = struct.pack('<B', 100)
        f.write(data)
        data = struct.pack('<i', number)
        f.write(data)
        data = struct.pack('<d', Ib)
        f.write(data)
        data = struct.pack('<d', freq)
        f.write(data)
        data = struct.pack('<B', 125)
        f.write(data)

        for i in range(len(validdata)):
            data = struct.pack('<dddddd', validdata[i][0], validdata[i][1], validdata[i][2], validdata[i][3], validdata[i][4], validdata[i][5])
            f.write(data)
        data = struct.pack('<d', BaseMassInMeV)
        f.write(data)
        f.close()

        return None

# if __name__ == "__main__":
#     inFileName = r"C:\Users\anxin\Desktop\test\jinwusuo zhenshi.dst"
#     outFileName = r"C:\Users\anxin\Desktop\test\jinwusuo zhenshi1.dst"
#     a = ChangeNp(inFileName, outFileName, 20)
#     a.run()