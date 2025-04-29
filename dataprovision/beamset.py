import numpy as np
import struct
import os
# 二进制文件，数据格式
# Char + Char + dumpPeriodicity(int) + Np(int) + Ib[mA](double) + freq[MHz](double) + mc2[MeV](double)
# + Nx * [Char + tpye(int) + Index(int) + time[s](double) + location[m](double) +
# Np * [x(d) + px(d) +  y(double) + py(double) + z(double) + pz(double) + lossFlag(int)]]
# Np * [x(double) + px(double) +  y(double) + py(double) + t(double) + pz(double) + recordFlag(double)]]


class BeamsetParameter():
    def __init__(self, beamset_path):
        self.beamset_path = beamset_path


    def get_step(self):
        with open(self.beamset_path, 'rb') as f:

            tdata = struct.unpack("<c", f.read(1))
            char1 = str(tdata[0])
            tdata = struct.unpack("<c", f.read(1))
            char2 = str(tdata[0])

            tdata = struct.unpack("<i", f.read(4))
            self.dumpPeriodicity = int(tdata[0])
            # print("输出间隔为{aa}".format(aa=self.dumpPeriodicity))

            tdata = struct.unpack("<i", f.read(4))
            numofp = int(tdata[0])
            # print("粒子数为：{aa}".format(aa=numofp))

            tdata = struct.unpack("<d", f.read(8))
            self.Ib = float(tdata[0])
            # print("流强为：{aa}mA".format(aa=self.Ib))

            tdata = struct.unpack("<d", f.read(8))
            self.freq = float(tdata[0])
            # print("频率为：{aa}MHz".format(aa=self.freq))

            tdata = struct.unpack("<d", f.read(8))
            self.BaseMassInMeV = float(tdata[0])
            # print("粒子静止质量为：{aa}MeV".format(aa=self.BaseMassInMeV))

            #一步的字节数
        byte_onestep = 1 + 4 + 4 + 8 + 8 + (48 + 8) * numofp
        byte_onestep_head = 1 + 1 + 4*2 + 8*3

        file_size = os.path.getsize(self.beamset_path)
        step = (file_size - byte_onestep_head) / byte_onestep
        return int(step)

    def get_one_parameter(self, num):
        step_num = self.get_step()
        step_list = [i for i in range(step_num)]
        # print(step_list)
        if num < 0:
            num = step_list[num]
        elif num >= step_num or num < step_num*-1:
            print(f"There are {step_num - 1} step in this file, it's beyond that",)
            return 0

        with open(self.beamset_path, 'rb') as f:

            tdata = struct.unpack("<c", f.read(1))
            char1 = str(tdata[0])
            tdata = struct.unpack("<c", f.read(1))
            char2 = str(tdata[0])

            tdata = struct.unpack("<i", f.read(4))
            self.dumpPeriodicity = int(tdata[0])
            # print("输出间隔为{aa}".format(aa=self.dumpPeriodicity))

            tdata = struct.unpack("<i", f.read(4))
            self.numofp = int(tdata[0])
            # print("粒子数为：{aa}".format(aa=self.numofp))

            tdata = struct.unpack("<d", f.read(8))
            self.Ib = float(tdata[0])
            # print("流强为：{aa}mA".format(aa=self.Ib))

            tdata = struct.unpack("<d", f.read(8))
            self.freq = float(tdata[0])
            # print("频率为：{aa}MHz".format(aa=self.freq))

            tdata = struct.unpack("<d", f.read(8))
            self.BaseMassInMeV = float(tdata[0])
            # print("粒子静止质量为：{aa}MeV".format(aa=self.BaseMassInMeV))

            #一步的字节数
            byte_onestep = 1 + 4 + 4 + 8 + 8 + (48 + 8) * self.numofp
            f.seek(num * byte_onestep, 1)

            self.one_step_dict = {}
            self.one_step_list = []

            tdata = struct.unpack("<c", f.read(1))

            tpye = struct.unpack("<i", f.read(4))
            self.one_step_dict["tpye"] = int(tpye[0])
            # print("tpye", tpye)

            Index = struct.unpack("<i", f.read(4))
            self.one_step_dict["index"] = int(Index[0])
            # print("index", Index)

            time = struct.unpack("<d", f.read(8))
            self.one_step_dict["time"] = float(time[0])
            # print(time)

            location = struct.unpack("<d", f.read(8))
            self.one_step_dict["location"] = float(location[0])

            # print("location", location)
            # for i in range(self.numofp):
            #     vdata1 = struct.unpack("<dddddd", f.read(48))
            #     vdata2 = struct.unpack("<ii", f.read(8))
            #
            #     vdata = list(vdata1) + list(vdata2)
            #     self.one_step_list.append(vdata)
            data = np.frombuffer(f.read((48 + 8) * self.numofp), dtype=np.dtype([
                ('x', '<f8'), ('xp', '<f8'), ('y', '<f8'), ('yp', '<f8'), ('z', '<f8'), ('zp', '<f8'),
                ('id', '<i4'), ('status', '<i4')
            ]))
            data = [list(row) for row in data]
            self.one_step_list = data
            # while True:
            #     try:
            #         tdata = struct.unpack("<c", f.read(1))
            #         # print(tdata)
            #     except struct.error:
            #         print("所选步数超过了总步数")
            #         break
            #
            #     else:
            #
            #         tpye = struct.unpack("<i", f.read(4))
            #         self.one_step_dict["tpye"] = int(tpye[0])
            #         # print("tpye", tpye)
            #
            #         Index = struct.unpack("<i", f.read(4))
            #         self.one_step_dict["index"] = int(Index[0])
            #         # print("index", Index)
            #
            #         time = struct.unpack("<d", f.read(8))
            #         self.one_step_dict["time"] = float(time[0])
            #         # print(time)
            #
            #         location = struct.unpack("<d", f.read(8))
            #         self.one_step_dict["location"] = float(location[0])
            #         # print("location", location)
            #         # for i in range(self.numofp):
            #         #     vdata1 = struct.unpack("<dddddd", f.read(48))
            #         #     vdata2 = struct.unpack("<ii", f.read(8))
            #         #
            #         #     vdata = list(vdata1) + list(vdata2)
            #         #     self.one_step_list.append(vdata)
            #         data = np.frombuffer(f.read((48 + 8) * self.numofp), dtype=np.dtype([
            #             ('x', '<f8'), ('xp', '<f8'), ('y', '<f8'), ('yp', '<f8'), ('z', '<f8'), ('zp', '<f8'),
            #             ('id', '<i4'), ('status', '<i4')
            #         ]))
            #         list2d = [list(item) for item in data.tolist()]
            #         print(list2d[0])
            #         self.one_step_list.append(list2d)
            #     break

        return self.one_step_dict, self.one_step_list


    def get_parameter(self):
        with open(self.beamset_path, 'rb') as f:

            tdata = struct.unpack("<c", f.read(1))
            char1 = str(tdata[0])
            tdata = struct.unpack("<c", f.read(1))
            char2 = str(tdata[0])

            tdata = struct.unpack("<i", f.read(4))
            self.dumpPeriodicity = int(tdata[0])
            # print("输出间隔为{aa}".format(aa=self.dumpPeriodicity))

            tdata = struct.unpack("<i", f.read(4))
            self.numofp = int(tdata[0])
            # print("粒子数为：{aa}".format(aa=self.numofp))

            tdata = struct.unpack("<d", f.read(8))
            self.Ib = float(tdata[0])
            # print("流强为：{aa}mA".format(aa=self.Ib))

            tdata = struct.unpack("<d", f.read(8))
            self.freq = float(tdata[0])
            # print("频率为：{aa}MHz".format(aa=self.freq))

            tdata = struct.unpack("<d", f.read(8))
            self.BaseMassInMeV = float(tdata[0])
            # print("粒子静止质量为：{aa}MeV".format(aa=self.BaseMassInMeV))

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
                    print(int(Index[0]))

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
    import numpy as np
    beamset_pasth = r"C:\Users\shliu\Desktop\test_changdu\OutputFile\BeamSet.plt"
    obj = BeamsetParameter(beamset_pasth)

    step = obj.get_step()
    print(step)
    v1, v2 = obj.get_one_parameter(0)
    print(v1, v2)

    # for i in range(697):
    #     v1, v2 =obj.get_one_parameter(i)
    #     print(v1)
    # print(v1)
    # import matplotlib.pyplot as plt
    # # x = [i[0] * 1000 for i in v2]
    # # y = [i[2] * 1000for i in v2]
    #
    # x = [i[4] * 1000 for i in v2]
    # y = np.array([i[5] * 1000for i in v2])
    # y = [(i -np.mean(y))/np.mean(y) *1000 for i in y]
    #
    # plt.scatter(x, y, s = 0.8)
    # plt.show()