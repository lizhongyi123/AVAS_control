import os.path

from utils.readfile import read_dst, read_txt
import math
import numpy as np
from global_varible import c_light
from global_varible import Pi, c_light
from dataprovision.latticeparameter import LatticeParameter
class DatasetParameter():
    """
    对dataset文件进行解析
    """
    def __init__(self, dataset_path, project_path=None):
        self.dataset_path = dataset_path
        self.z = []
        self.project_path = project_path

    def get_parameter(self):
        dataset_info = read_txt(self.dataset_path, out='list')
        if '-nan(ind)' in dataset_info[-1]:
            return False

        self.num_of_particle = float(dataset_info[0][28])
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

        self.x = [i[1] + i[29] for i in dataset_info]   #m
        self.px = [i[2] for i in dataset_info]   #MeV

        self.y = [i[3] + i[31] for i in dataset_info]
        self.py = [i[4] for i in dataset_info]


        self.pz = [i[6] for i in dataset_info]
        
        self.x_1 = [self.px[i]/self.pz[i] for i in range(len(self.pz))]   #rad
        self.y_1 = [self.py[i]/self.pz[i] for i in range(len(self.pz))]


        self.beta_x = [i[10] for i in dataset_info]  ##  mm/π.mrad
        self.beta_y = [i[11] for i in dataset_info]
        self.beta_z = [i[12] for i in dataset_info]


        self.emit_x = [i[13] for i in dataset_info]  # * 10**6 以后是 π.mm.mrad
        self.emit_y = [i[14] for i in dataset_info]
        self.emit_z = [i[15] for i in dataset_info]

        self.rms_x = [i[16] for i in dataset_info]         #原本的单位是m, * 10**3 以后是mm
        self.rms_xx = [-1 * i[16] for i in dataset_info]
        self.rms_x1 = [i[17] for i in dataset_info]        #rad

        self.rms_y = [i[18] for i in dataset_info]
        self.rms_yy = [-1 * i[18] for i in dataset_info]
        self.rms_y1 = [i[19] for i in dataset_info]

        self.rms_z = [i[20] for i in dataset_info]
        self.rms_zz = [-1 * i[20] for i in dataset_info]

        self.max_x = [i[22] for i in dataset_info]     #m
        self.max_xx = [-1 * i[22] for i in dataset_info]

        self.max_y = [i[24] for i in dataset_info]
        self.max_yy = [-1 * i[24] for i in dataset_info]

        self.ek = [i[0] for i in dataset_info]  ##MeV
        self.loss = [self.num_of_particle - i[28] for i in dataset_info]  ##

        if self.project_path:
            self.get_phi()

        return True


    def get_lattice_end_index(self):
        lattice_mulp_path = os.path.join(self.project_path, 'InputFile', 'lattice_mulp.txt')
        lattice_obj = LatticeParameter(lattice_mulp_path)
        lattice_obj.get_parameter()
        total_length = lattice_obj.total_length

        end_index = 0
        for i in range(len(self.z)):
            if self.z[i] > total_length:
                end_index = i
                break
        print("end_index", end_index)
        return end_index

    def get_mass_freq(self):
        beam_txt = self.project_path + r'/InputFile/beam.txt'
        res = read_txt(beam_txt)
        if res.get('readparticledistribution') is None:
            BaseMassInMeV = float(res.get('particlerestmass'))
            freq = float(res.get('frequency'))
        else:
            dstfile = self.project_path + r'/InputFile' + r"/" + res.get('readparticledistribution')
            dst_res = read_dst(dstfile)
            BaseMassInMeV = float(dst_res.get('basemassinmev'))
            freq = float(dst_res.get('freq'))
        return BaseMassInMeV, freq

    def get_phi(self):
        self.BaseMassInMeV, self.freq = self.get_mass_freq()
        beta = []
        self.phi = []
        self.phi_phi = []
        for i in range(len(self.rms_z)):
            gammaaaa = self.ek[i] / self.BaseMassInMeV + 1
            beta.append(math.sqrt(1 - 1.0 / gammaaaa / gammaaaa))
            v = self.rms_z[i] / (beta[-1] * c_light) * self.freq * 360
            self.phi.append(v)
            self.phi_phi.append(-1 * v)


if __name__ == "__main__":
    # project_path = r"C:\Users\anxin\Desktop\test_err_dyn1\OutputFile\error_output\output_1_1\DataSet.txt"
    project_path = r"C:\Users\anxin\Desktop\test_acct"
    dataset_path = r"C:\Users\shliu\Desktop\test_err_dyn\OutputFile\error_output\output_0_0\DataSet.txt"
    dataset_path = r"C:\Users\shliu\Desktop\test_err_dyn\OutputFile\error_output\output_-1_-1\DataSet.txt"
    res = DatasetParameter(dataset_path)
    if res.get_parameter() is False:
        print("fadsf")
    print(res.z[-1])
    # print(res.emit_x[0] * 10 **6)
    # print(res.emit_x[-1] * 10 **6)
    #
    # print(res.emit_y[0] * 10 **6)
    # print(res.emit_y[-1] * 10 **6)
    #
    # print(res.emit_z[0] * 10 **6)
    # print(res.emit_z[-1] * 10 **6)