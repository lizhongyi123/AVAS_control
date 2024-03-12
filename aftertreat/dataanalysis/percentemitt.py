from utils.readfile import read_dst
import math
import numpy as np
from dataprovision.beamparameter import DstParameter

class PercentEmit():
    """
    本类为计算发射度及百分比发射度
    get_percent_emit：该函数用来得到百分比发射度，返回结果分别为对于xx1，yy1，zz1使用的是归一化发射度，就是*alpha*beta， xy和phiE
    使用非归一化发射度，

    需要强调的是本例子中的alpha， beta嗾使百分比的，这和tracewin是不一样的，tracewin的alpha和beta都是全部粒子计算出来的


    """
    def __init__(self, dst_path):
        self.x_list = []
        self.x1_list = []
        self.y_list = []
        self.y1_list = []
        self.z_list = []
        self.z1_list = []
        self.phi_list = []
        self.E_list = []
        self.z_speed_list = []
        self.dst_path = dst_path
        self.number = 0
        self.Ib = 0
        self.freq = 0
        self.BaseMassInMeV = 0
        self.__C_light = 299792458

        self.gamma = 0
        self.beta = 0
        self.energy = 0

    def get_data(self):

        dst_obj = DstParameter(self.dst_path)
        dst_obj.get_parameter()

        self.number = dst_obj.number
        self.freq = dst_obj.freq
        self.BaseMassInMeV = dst_obj.BaseMassInMeV

        self.x_list = dst_obj.x_list
        self.x1_list = dst_obj.x1_list
        self.y_list = dst_obj.y_list
        self.y1_list = dst_obj.y1_list

        self.phi_list = [i / math.pi * 180 for i in dst_obj.phi_list]
        self.E_list = dst_obj.E_list

        self.z_list = dst_obj.z_list
        self.z1_list = dst_obj.z1_list
        self.z_speed_list = dst_obj.z_speed_list

        self.energy = dst_obj.energy
        self.gamma = dst_obj.gamma
        self.beta = dst_obj.beta


        #
        # data = read_dst(self.dst_path)
        # self.number = data.get('number')
        # self.freq = data.get('freq')
        # self.BaseMassInMeV = data.get('BaseMassInMeV')
        #
        # data = data.get('phase')
        # self.x_list = [i[0] * 10 for i in data]
        # self.x1_list = [i[1] * 1000 for i in data]
        # self.y_list = [i[2] * 10 for i in data]
        # self.y1_list = [i[3] * 1000 for i in data]
        #
        # self.phi_list = [i[4] for i in data]
        # self.E_list = [i[5] for i in data]
        #
        # for i in data:
        #     tmp_gamma = 1 + i[5] / self.BaseMassInMeV
        #     tmp_beta = math.sqrt(1 - 1.0 / tmp_gamma / tmp_gamma)
        #     tmp_speed = tmp_beta * self.__C_light  # 总速度
        #     speedz = math.sqrt(pow(tmp_speed, 2) / (pow(i[1], 2) + pow(i[3], 2) + 1))
        #     tmp_t0 = i[4] / (2 * math.pi * self.freq)
        #
        #     self.z_list.append(-1 * tmp_t0 * speedz * 1000)  # mm
        #
        #     ##############################
        #     # 使用z方向的速度
        #     # self.z_speed_list.append(speedz)
        #     # 总速度
        #     self.z_speed_list.append(tmp_speed)
        #     #############################################
        #
        # average_z_speend = np.mean(self.z_speed_list)
        #
        # self.z1_list = [(i - average_z_speend) / i * 1000 for i in self.z_speed_list]
        #
        # self.energy = np.mean(self.E_list)
        # self.gamma = 1 + self.energy / self.BaseMassInMeV
        # self.beta = math.sqrt(1 - 1.0 / self.gamma / self.gamma)


    # 计算任意一个twiss参数和发射度
    def cal_twiss_emitt(self, x, x1):
        average_x = np.mean(x)
        average_x1 = np.mean(x1)
        sigma_x = np.average([(i - average_x) ** 2 for i in x])
        sigma_x1 = np.average([(i - average_x1) ** 2 for i in x1])
        print(len(x), len(x1))
        sigma_xx1 = np.average([(x[i] - average_x) * (x1[i] - average_x1) for i in range(len(x))])

        epsilon_x = math.sqrt(sigma_x * sigma_x1 - sigma_xx1 * sigma_xx1)

        beta_x = sigma_x / epsilon_x
        alpha_x = -sigma_xx1 / epsilon_x
        gamma_x = (1 + alpha_x ** 2) / beta_x

        norm_epsilon_x = self.beta * self.gamma * epsilon_x

        return alpha_x, beta_x, gamma_x, epsilon_x, norm_epsilon_x

    def get_size(self, x, x1, alpha_x, beta_x, gamma_x):
        return gamma_x * x ** 2 + 2 * alpha_x * x * x1 + beta_x * x1 ** 2

    # 得到任意一个平面的百分比发射度
    def get_any_emit(self, x, y, ratio):
        #########################################################
        alpha_x, beta_x, gamma_x, epson_x, norm_epson_x = self.cal_twiss_emitt(x, y)

        size_list = []
        for i in range(len(self.x_list)):
            size = self.get_size(x[i], y[i], alpha_x, beta_x, gamma_x)
            size_list.append(size)
        index = int(ratio * self.number)

        if index >= len(size_list):
            index = len(size_list) - 1

        size = sorted(size_list)[index]

        indices = [i for i, x in enumerate(size_list) if x <= size]

        any_x_list = [x[i] for i in indices]
        any_y_list = [y[i] for i in indices]
        # print(len(any_x_list))
        # 根据百分比的例子计算rms的twiss参数
        res = list(self.cal_twiss_emitt(any_x_list, any_y_list))
        ###########################################################
        # 根据全twiss参数，计算的全发射度
        all_epsilon = self.get_all_epsilon(any_x_list, any_y_list, alpha_x, beta_x, gamma_x)

        ###########################################################
        # 根据百分比twiss参数，计算全发射度
        percent_all_epsilon = self.get_all_epsilon(any_x_list, any_y_list, res[0], res[1], res[2])

        ###########################################################
        res.append(float(all_epsilon))
        res.append(float(percent_all_epsilon))

        return res

    # 得到任意一个平面的全发射度
    def get_all_epsilon(self, x, x1, alpha_x, beta_x, gamma_x):

        all_size = []
        for i in range(len(x)):
            all_size.append(self.get_size(x[i], x1[i], alpha_x, beta_x, gamma_x))

        return max(all_size)

    # 得到几个平面的百分比发射度
    def get_percent_emit(self, ratio):
        self.get_data()
        #epsi_xx1：rms发射度  all_epsi_xx1：全发射度  percent_all_epsi_xx1：百分比全发射度
        alpha_xx1, beta_xx1, gamma_xx1, _, epsi_xx1, all_epsi_xx1, percent_all_epsi_xx1 = self.get_any_emit(self.x_list,
                                                                                                            self.x1_list,
                                                                                                            ratio)
        all_epsi_xx1 = all_epsi_xx1 * self.beta * self.gamma

        percent_all_epsi_xx1 = percent_all_epsi_xx1 * self.beta * self.gamma

        xx1_list = [alpha_xx1, beta_xx1, epsi_xx1, all_epsi_xx1, percent_all_epsi_xx1]
        # print('xx1', alpha_xx1, beta_xx1,  epsi_xx1)

        alpha_yy1, beta_yy1, gamma_yy1, _, epsi_yy1, all_epsi_yy1, percent_all_epsi_yy1 = self.get_any_emit(self.y_list,
                                                                                                            self.y1_list,
                                                                                                            ratio)
        all_epsi_yy1 = all_epsi_yy1 * self.beta * self.gamma
        percent_all_epsi_yy1 = percent_all_epsi_yy1 * self.beta * self.gamma

        yy1_list = [alpha_yy1, beta_yy1, epsi_yy1, all_epsi_yy1, percent_all_epsi_yy1]
        # print('yy1', alpha_yy1, beta_yy1,  epsi_yy1)

        alpha_zz1, beta_zz1, gamma_zz1, _, epsi_zz1, all_epsi_zz1, percent_all_epsi_zz1 = self.get_any_emit(self.z_list,
                                                                                                            self.z1_list,
                                                                                                            ratio)
        all_epsi_zz1 = all_epsi_zz1 * self.beta * self.gamma
        percent_all_epsi_zz1 = percent_all_epsi_zz1 * self.beta * self.gamma

        zz1_list = [alpha_zz1, beta_zz1, epsi_zz1, all_epsi_zz1, percent_all_epsi_zz1]
        # print('zz1',alpha_zz1, beta_zz1,  epsi_zz1)

        alpha_xy, beta_xy, gamma_xy, epsi_xy, _, all_epsi_xy, percent_all_epsi_xy = self.get_any_emit(self.x_list,
                                                                                                      self.y_list,
                                                                                                      ratio)
        xy_list = [alpha_xy, beta_xy, epsi_xy, all_epsi_xy, percent_all_epsi_xy]
        # print('xy', alpha_xy, beta_xy,  epsi_xy)
        
        alpha_phie, beta_phie, gamma_phie, epsi_phie, _, all_epsi_phie, percent_all_epsi_phie = self.get_any_emit(self.phi_list,
                                                                                                      self.E_list,
                                                                                                      ratio)
        phie_list = [alpha_phie, beta_phie, epsi_phie, all_epsi_phie, percent_all_epsi_phie]

        res = [xx1_list, yy1_list, zz1_list, xy_list, phie_list]
        return res

    # 得到几个平面的100%发射度
    def get_100_emit(self):
        self.get_data()
        alpha_xx1, beta_xx1, gamma_xx1, _, epsi_xx1 = self.cal_twiss_emitt(self.x_list, self.x1_list)
        # print('xx1', alpha_xx1, beta_xx1,  epsi_xx1)

        alpha_yy1, beta_yy1, gamma_yy1, _, epsi_yy1 = self.cal_twiss_emitt(self.y_list, self.y1_list)
        # print('yy1',alpha_yy1, beta_yy1,  epsi_yy1)

        alpha_zz1, beta_zz1, gamma_zz1, _, epsi_zz1 = self.cal_twiss_emitt(self.z_list, self.z1_list)
        # print('zz1',alpha_zz1, beta_zz1,  epsi_zz1)

        alpha_xy, beta_xy, gamma_xy, epsi_xy, _ = self.cal_twiss_emitt(self.x_list, self.y_list)
        # print('xy', alpha_xy, beta_xy,  epsi_xy)

        xx1_list = [alpha_xx1, beta_xx1, epsi_xx1]
        yy1_list = [alpha_yy1, beta_yy1, epsi_yy1]
        zz1_list = [alpha_zz1, beta_zz1, epsi_zz1]
        xy_list = [alpha_xy, beta_xy, epsi_xy]

        res = [xx1_list, yy1_list, zz1_list, xy_list]
        return res


if __name__ == '__main__':
    dst_path = r"C:\Users\anxin\Desktop\trace\part_rfq.dst"
    # dst_path = r"C:\Users\anxin\Desktop\tace_test\result\part_dtl1.dst"
    # dst_path = r"D:\重要程序\lizituijinzongjie\75\butongliuqiang\OutputFile\outData_100000.000000.dst"
    v = PercentEmit(dst_path)
    res1 = v.get_percent_emit(1)
    print(res1)
    # res2 = v.get_100_emit()
    # print(res1)
    # print(res2)