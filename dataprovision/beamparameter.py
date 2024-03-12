import sys
sys.path.append(r'C:\Users\anxin\Desktop\AVAS_control')

from utils.readfile import read_dst, read_txt
import math
import numpy as np
from global_varible import c_light


class DstParameter():
    """
    对dst文件进行解析
    """
    def __init__(self, dst_path):
        self.dst_path = dst_path
        self.number = 0
        self.freq = 0
        self.BaseMassInMeV = 0
        self.Ib = 0
        self.x_list = []   #mm
        self.x1_list = []   #mrad
        self.y_list = []
        self.y1_list = []

        self.phi_list = []
        self.E_list = []

        self.z_list = []
        self.z1_list = []

        self.energy = 0
        self.gamma = 0
        self.beta = 0
        self.z_speed_list = []

    def get_parameter(self):
        data = read_dst(self.dst_path)

        self.number = data.get('number')
        self.freq = data.get('freq')
        self.BaseMassInMeV = data.get('basemassinmev')
        self.Ib = data.get('ib')

        data = data.get('phase')

        self.x_list = [i[0] * 10 for i in data]   #mm
        self.x1_list = [i[1] * 1000 for i in data]  # mrad
        self.y_list = [i[2] * 10 for i in data]
        self.y1_list = [i[3] * 1000 for i in data]

        self.phi_list = [i[4] for i in data]
        self.E_list = [i[5] for i in data]
        self.z_list = []
        self.z_speed_list = []

        for i in data:
            tmp_gamma = 1 + i[5] / self.BaseMassInMeV
            tmp_beta = math.sqrt(1 - 1.0 / tmp_gamma / tmp_gamma)
            tmp_speed = tmp_beta * c_light  # 总速度

            speedz = math.sqrt(pow(tmp_speed, 2) / (pow(i[1], 2) + pow(i[3], 2) + 1))
            tmp_t0 = i[4] / (2 * math.pi * self.freq)

            self.z_list.append(-1 * tmp_t0 * speedz * 1000)  # mm

            ##############################
            # 使用z方向的速度
            # self.z_speed_list.append(speedz)
            # 总速度
            self.z_speed_list.append(tmp_speed)
            #############################################

        average_z_speend = np.mean(self.z_speed_list)

        self.z1_list = [(i - average_z_speend) / i * 1000 for i in self.z_speed_list]

        # 平均能量,gamma, beta
        self.energy = np.mean(self.E_list)

        self.gamma = 1 + self.energy / self.BaseMassInMeV
        self.beta = math.sqrt(1 - 1.0 / self.gamma / self.gamma)

        #中心x
        self.center_x = np.mean(self.x_list)

        #中心y
        self.center_y = np.mean(self.y_list)

        #包络x

        self.rms_x = np.sqrt( np.sum([(i-self.center_x)**2 for i in self.x_list ]) / self.number)

        self.rms_y = np.sqrt( np.sum([(i-self.center_y)**2 for i in self.y_list ]) / self.number)

# def get_entrance_beam_parameter(project_path):
#     project_path = project_path
#
#     beam_path = project_path + r'\InputFile' + r'\beam.txt'
#     lattice_path = project_path + r'\InputFile' + r'\lattice.txt'
#     input_path = project_path + r'\InputFile' + r'\input.txt'
#
#     charge = 0
#
#     res = read_txt(beam_path)
#     charge = float(res.get('numOfCharge'))
#
#     if res.get('readparticledistribution') is None:
#         BaseMassInMeV = float(res.get('particlerestmass'))
#         freq = float(res.get('frequency'))
#         beam_parameter = {
#             'charge': charge,
#             'freq': freq,
#             'basemassinmev': BaseMassInMeV,
#         }
#     else:
#         dst_path = project_path + r'\InputFile' + r"\\" + res.get('readparticledistribution')
#         dst_obj = DstParameter(dst_path)
#         dst_obj.get_parameter()
#
#         beam_parameter = {
#                 'charge': charge,
#                 'number': dst_obj.number,
#                 'freq': dst_obj.freq,
#                 'ib': dst_obj.Ib,
#                 'basemassinmev': dst_obj.BaseMassInMeV,
#                 'gamma': dst_obj.gamma,
#                 'beta': dst_obj.beta,
#                 'energy': dst_obj.energy
#
#         }
#     return beam_parameter

def get_out_beam_parameter(project_path, dst_path):
    project_path = project_path

    beam_path = project_path + r'\InputFile' + r'\beam.txt'
    charge = 0

    res = read_txt(beam_path)
    charge = float(res.get('numOfCharge'))


    dst_obj = DstParameter(dst_path)
    dst_obj.get_parameter()

    beam_parameter = {
            'charge': charge,
            'number': dst_obj.number,
            'freq': dst_obj.freq,
            'ib': dst_obj.Ib,
            'basemassinmev': dst_obj.BaseMassInMeV,
            'gamma': dst_obj.gamma,
            'beta': dst_obj.beta,
            'energy': dst_obj.energy

    }
    return beam_parameter


if __name__ == "__main__":
    # project_path = r"C:\Users\anxin\Desktop\00000"
    # res = get_entrance_beam_parameter(project_path)
    # print(res)

    # dst_path = r"C:\Users\anxin\Desktop\00000\InputFile\part_rfq.dst"
    # # obj = DstParameter(dst_path)
    # # obj.get_parameter()
    # # print(obj.x_list)
    # res = get_entrance_beam_parameter(project_path)
    dst_path = r"C:\Users\anxin\Desktop\test\OutputFile\error_middle\output_0\outData_0.477000.dst"

    obj = DstParameter(dst_path)
    obj.get_parameter()
    print(obj.energy)
