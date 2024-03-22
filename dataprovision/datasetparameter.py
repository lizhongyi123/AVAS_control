from utils.readfile import read_dst, read_txt
import math
import numpy as np
from global_varible import c_light


class DatasetParameter():
    """
    对dataset文件进行解析
    """
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path
        self.z = []


    def get_parameter(self):
        dataset_info = read_txt(self.dataset_path, out='list')
        num_of_particle = float(dataset_info[0][28])
        # print(dataset_info[0])
        # print(len(dataset_info[0]))
        dataset_info = [[float(j) for j in i] for i in dataset_info]

        # self.z = [i[5] for i in dataset_info]

        self.z = []
        sign1 = 0
        sign2 = 0

        for i in range(len(dataset_info)):
            if (dataset_info[i][35] == 0):
                sign2 = 0
                if (sign1 == 0):
                    self.z.append(dataset_info[i][5] + dataset_info[i][33])
                else:
                    self.z.append(self.z[-1] + dataset_info[i][38])
            elif (dataset_info[i][35] == 1):
                self.z.append(self.z[-1] + math.sqrt(dataset_info[i][37] ** 2 + dataset_info[i][38] ** 2))
                sign1 = 1
                sign2 = 0
            elif (sign2 == 0):
                self.z.append(self.z[-1] + math.sqrt(dataset_info[i][37] ** 2 + dataset_info[i][38] ** 2))
                sign2 = 1
            else:
                continue

        self.x = [i[1] for i in dataset_info]   #m
        self.px = [i[2] for i in dataset_info]   #MeV

        self.y = [i[3] for i in dataset_info]
        self.py = [i[4] for i in dataset_info]


        self.pz = [i[6] for i in dataset_info]

        self.beta_x = [i[10] for i in dataset_info]  ##  mm/π.mrad
        self.beta_y = [i[11] for i in dataset_info]
        self.beta_z = [i[12] for i in dataset_info]


        self.emit_x = [i[13] for i in dataset_info]  # * 10**6 以后是 π.mm.mrad
        self.emit_y = [i[14] for i in dataset_info]
        self.emit_z = [i[15] for i in dataset_info]

        self.rms_x = [i[16] for i in dataset_info]         #原本的单位是m, * 10**3 以后是mm
        self.rms_xx = [-1 * i[16] for i in dataset_info]

        self.rms_y = [i[18] for i in dataset_info]
        self.rms_yy = [-1 * i[18] for i in dataset_info]

        self.rms_z = [i[20] for i in dataset_info]
        self.rms_zz = [-1 * i[20] for i in dataset_info]

        self.max_x = [i[22] for i in dataset_info]     #m
        self.max_xx = [-1 * i[22] for i in dataset_info]

        self.max_y = [i[24] for i in dataset_info]
        self.max_yy = [-1 * i[24] for i in dataset_info]

        self.ek = [i[0] for i in dataset_info]  ##MeV
        self.loss = [num_of_particle - i[28] for i in dataset_info]  ##



if __name__ == "__main__":
    project_path = r"C:\Users\anxin\Desktop\test_a_t\AVAS\OutputFile\DataSet.txt"
    # res = DatasetParameter(project_path)
    # res.get_parameter()
