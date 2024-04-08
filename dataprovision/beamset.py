import numpy
import struct

# 二进制文件，数据格式
# Char + Char + dumpPeriodicity(int) + Np(int) + Ib[mA](double) + freq[MHz](double) + mc2[MeV](double)
# + Nx * [Char + tpye(int) + Index(int) + time[s](double) + location[m](double) +
# Np * [x(float) + px(float) +  y(float) + py(float) + z(float) + pz(float) + lossFlag(float)]]
# Np * [x(float) + px(float) +  y(float) + py(float) + t(float) + pz(float) + recordFlag(float)]]
inFileName = r"D:\CodeSolo\solo\AVAS\OutputFile\BeamSet.plt"
selectNumber = 27

C_light = 299792458
particleData = []
energy = -1
phase = -1
beta = -1
gamma = -1
class BeamsetParameter():
    def __init__(self, beamset_path):
        self.beamset_path = beamset_path

    def get_one_parameter(self, num):
        with open(self.beamset_path, 'rb') as f:

            tdata = struct.unpack("<c", f.read(1))
            char1 = str(tdata[0])
            tdata = struct.unpack("<c", f.read(1))
            char2 = str(tdata[0])

            tdata = struct.unpack("<i", f.read(4))
            self.dumpPeriodicity = int(tdata[0])
            print("输出间隔为{aa}".format(aa=self.dumpPeriodicity))

            tdata = struct.unpack("<i", f.read(4))
            self.numofp = int(tdata[0])
            print("粒子数为：{aa}".format(aa=self.numofp))

            tdata = struct.unpack("<d", f.read(8))
            self.Ib = float(tdata[0])
            print("流强为：{aa}mA".format(aa=self.Ib))

            tdata = struct.unpack("<d", f.read(8))
            self.freq = float(tdata[0])
            print("频率为：{aa}MHz".format(aa=self.freq))

            tdata = struct.unpack("<d", f.read(8))
            self.BaseMassInMeV = float(tdata[0])
            print("粒子静止质量为：{aa}MeV".format(aa=self.BaseMassInMeV))

            #一步的字节数
            byte_onestep = 1 + 4 + 4 + 8 + 8 + (48 + 4) * self.numofp

            f.seek( num * byte_onestep, 1)
            self.one_step_dict = {}
            self.one_step_list = []

            while True:

                try:
                    tdata = struct.unpack("<c", f.read(1))
                except struct.error:
                    print("所选步数超过了总步数")
                    break

                else:

                    tpye = struct.unpack("<i", f.read(4))
                    self.one_step_dict["tpye"] = int(tpye[0])
                    # print(tpye)

                    Index = struct.unpack("<i", f.read(4))
                    self.one_step_dict["index"] = int(Index[0])
                    print("index", Index)

                    time = struct.unpack("<d", f.read(8))
                    self.one_step_dict["time"] = float(time[0])
                    # print(time)

                    location = struct.unpack("<d", f.read(8))
                    self.one_step_dict["location"] = float(location[0])
                    # print(location)

                    for i in range(self.numofp):

                        vdata1 = struct.unpack("<dddddd", f.read(48))
                        vdata2 = struct.unpack("<i", f.read(4))
                        vadata = list(vdata1) + list(vdata2)

                        self.one_step_list.append(vadata)
                break

    def get_parameter(self):
        with open(self.beamset_path, 'rb') as f:

            tdata = struct.unpack("<c", f.read(1))
            char1 = str(tdata[0])
            tdata = struct.unpack("<c", f.read(1))
            char2 = str(tdata[0])

            tdata = struct.unpack("<i", f.read(4))
            self.dumpPeriodicity = int(tdata[0])
            print("输出间隔为{aa}".format(aa=self.dumpPeriodicity))

            tdata = struct.unpack("<i", f.read(4))
            self.numofp = int(tdata[0])
            print("粒子数为：{aa}".format(aa=self.numofp))

            tdata = struct.unpack("<d", f.read(8))
            self.Ib = float(tdata[0])
            print("流强为：{aa}mA".format(aa=self.Ib))

            tdata = struct.unpack("<d", f.read(8))
            self.freq = float(tdata[0])
            print("频率为：{aa}MHz".format(aa=self.freq))

            tdata = struct.unpack("<d", f.read(8))
            self.BaseMassInMeV = float(tdata[0])
            print("粒子静止质量为：{aa}MeV".format(aa=self.BaseMassInMeV))

            self.allstep_list = []
            self.allstep_dict = []

            every_step_dict = {}
            every_step_list = []
            phase_zero = 0

            # while True:
            while True:

                every_step_dict = {}
                every_step_list = []

                try:
                    tdata = struct.unpack("<c", f.read(1))
                except struct.error:
                    break

                else:

                    tpye = struct.unpack("<i", f.read(4))
                    every_step_dict["tpye"] = int(tpye[0])
                    # print(tpye)

                    Index = struct.unpack("<i", f.read(4))
                    every_step_dict["Index"] = int(Index[0])
                    print(Index)

                    time = struct.unpack("<d", f.read(8))
                    every_step_dict["time"] = float(time[0])
                    # print(time)

                    location = struct.unpack("<d", f.read(8))
                    every_step_dict["location"] = float(location[0])
                    # print(location)

                    for i in range(self.numofp):

                        vdata1 = struct.unpack("<dddddd", f.read(48))
                        vdata2 = struct.unpack("<i", f.read(4))
                        vadata = list(vdata1) + list(vdata2)

                        every_step_list.append(vadata)

                    self.allstep_dict.append(every_step_dict)
                    self.allstep_list.append(every_step_list)


if __name__ == "__main__":
    import os
    project_path = r"C:\Users\anxin\Desktop\example3"
    beamset_pasth = os.path.join(project_path, "OutputFile", "BeamSet.plt")

    obj = BeamsetParameter(beamset_pasth)
    # obj.get_parameter()
    obj.get_one_parameter(610)
    # print(len(obj.allstep_list))


# if i == selectNumber:
#     try:
#         tdata = struct.unpack("<c", f.read(1))
#         char1 = str(tdata[0])
#     except struct.error:
#         print("selectNumber设置超过最大值".format(aa=i - 1))
#         exit(0)
#     else:
#         print("已读取束团分布，参数如下所示：".format(aa=i))
#         tdata = struct.unpack("<i", f.read(4))
#         type = int(tdata[0])
#         if (type == 0):
#             print("束团分布为T-code模式")
#         else:
#             print("束团分布为Z-code模式")
#         tdata = struct.unpack("<i", f.read(4))
#         Index = float(tdata[0])
#         print("输出为第{aa}次模拟循环中的束团分布".format(aa=Index))
#
#         tdata = struct.unpack("<d", f.read(8))
#         time = float(tdata[0])
#         print("输出束团所处的时间点：{aa}s".format(aa=time))
#         tdata = struct.unpack("<d", f.read(8))
#         Zgen = float(tdata[0])
#         print("输出束团所处的纵向位置为：{aa}m".format(aa=Zgen))
#
#         for j in range(numofp):
#             tdata = f.read(28)
#             tdata = struct.unpack("<fffffff", tdata)
#             xdata[j, 0] = tdata[0]
#             xdata[j, 1] = tdata[1]
#             xdata[j, 2] = tdata[2]
#             xdata[j, 3] = tdata[3]
#             xdata[j, 4] = tdata[4]
#             xdata[j, 5] = tdata[5]
#             xdata[j, 6] = tdata[6]
#         # print(xdata[j, 6])
#         break






