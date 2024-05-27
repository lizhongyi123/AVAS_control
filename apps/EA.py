import random
from scipy.optimize import minimize
from typing import List
import copy
import numpy as np
from core.AVAS import AVAS
from dataprovision.latticeparameter import LatticeParameter
from dataprovision.datasetparameter import DatasetParameter
from utils.treat_directory import list_files_in_directory, copy_directory, delete_directory
import time
import multiprocessing
from dataprovision.beamparameter import DstParameter
import global_varible
import copy
from utils.readfile import read_txt
from utils.treatlist import flatten_list, list_one_two, get_dimension
from utils.treatfile import copy_file


import os
import sys

# for i in sys.path:
#     print(i)
sys.path.append(r'C:\Users\anxin\Desktop\AVAS_control')


import random

from core.AVAS import AVAS
import time
import multiprocessing

import global_varible
import copy


class EA():
    """
    工程分析
    """

    def __init__(self, project_path):
        self.project_path = project_path

        self.lattice_mulp_path = os.path.join(self.project_path, 'InputFile', 'lattice_mulp.txt')
        self.lattice_path = os.path.join(self.project_path, 'InputFile', 'lattice.txt')

        self.input_path = os.path.join(self.project_path, 'InputFile')
        self.output_path = os.path.join(self.project_path, 'OutputFile')

        self.error_middle_path = os.path.join(self.project_path, 'OutputFile', 'error_middle')
        self.error_middle_output0_path = os.path.join(self.project_path, 'OutputFile', 'error_middle', 'output_0')
        self.error_output_path = os.path.join(self.project_path, 'OutputFile', 'error_output')

        self.loss = []
        self.opti_res = []
        self.error_elemment_command = global_varible.error_elemment_command
        self.error_elemment_stat = global_varible.error_elemment_command_stat
        self.error_elemment_dyn = global_varible.error_elemment_command_dyn

        self.error_beam_command = global_varible.error_beam_command
        self.error_beam_stat = global_varible.error_beam_stat
        self.error_beam_dyn = global_varible.error_beam_dyn

        self.all_group = 1
        self.all_time = 1
        self.lattice_mulp_list = []

        max_err_quad_tran = 5
        max_err_quad_rot = 5
        max_err_quad_k = 5

        self.err_quad_dx = max_err_quad_rot
        self.err_quad_dy = max_err_quad_rot
        self.err_quad_dz = max_err_quad_rot

        self.err_quad_dphix = max_err_quad_tran
        self.err_quad_dphiy = max_err_quad_tran
        self.err_quad_dphiz = max_err_quad_tran
        self.err_quad_dk = max_err_quad_k
        self.err_quad_max_value_lis = [self.err_quad_dx, self.err_quad_dy, self.err_quad_dphix, self.err_quad_dphiy,self.err_quad_dphiz, self.err_quad_dk, self.err_quad_dz]

        max_err_cav_tran = 5
        max_err_cav_rot = 5
        max_err_cav_k = 5
        max_err_cav_phis = 2
        
        
        self.err_cav_dx = max_err_cav_tran
        self.err_cav_dy = max_err_cav_tran
        self.err_cav_dz = max_err_cav_tran

        self.err_cav_dphix = max_err_cav_rot
        self.err_cav_dphiy = max_err_cav_rot
        self.err_cav_dk = max_err_cav_k
        self.err_cav_dphis = max_err_cav_phis

        self.err_cav_max_value_lis = [self.err_cav_dx, self.err_cav_dy, self.err_cav_dphix, self.err_cav_dphiy, self.err_cav_dk, self.err_cav_dphis, self.err_cav_dz]

        self.err_beam_parameter_num = 13
        self.err_quad_parameter_num = 7
        self.err_cav_parameter_num = 7




        self.decimal = 5  # 小数点保留多少位

        self.result_queue = multiprocessing.Queue()
        if os.path.exists(self.error_middle_path):
            delete_directory(self.error_middle_path)
        os.makedirs(self.error_middle_path)

        if os.path.exists(self.error_output_path):
            delete_directory(self.error_output_path)
        os.makedirs(self.error_output_path)

    def generate_basic_lattice(self):
        lines = read_txt(self.lattice_mulp_path, out='list')
        lines = [i for i in lines if i[0] in global_varible.mulp_basic_command]

        #为每一个场元件添加误差
        for i in range(len(lines)):
            if lines[i][0] == 'field' and lines[i][4] == '3':
                t_lis = ["err_quad_ncpl_dyn", 1, 0] + [0] * 8

                lines[i].append(t_lis)

            # 在叠加场添加高频腔原件误差
            elif lines[i][0] == 'field' and lines[i][4] == '1':
                t_lis = ["err_cav_ncpl_dyn", 1, 0] + [0] * 8
                lines[i].append(t_lis)

        new_lines = []
        for i in lines:
            if get_dimension(i) == 2:
                i_copy = copy.deepcopy(i)
                new_lines.append(i[-1])
                i_copy.pop()
                new_lines.append(i_copy)
            else:
                new_lines.append(i)

        new_lines = self.add_index(new_lines)
        new_lines = self.add_element_on_command(new_lines)
        new_lines = self.add_beam_err_command(new_lines)
        new_lines.insert(1, ['step', 1 , 1])
        # for i in new_lines:
        #     print(i)

        return new_lines





    #为误差增加编号
    def add_index(self, lattice):
        lattice = copy.deepcopy(lattice)
        num = 0
        for i in lattice:
            if i[0] == "err_quad_ncpl_dyn":
                i.append(f"mag_{num}")
                num += 1

        num = 0
        for i in lattice:
            if i[0] == "err_cav_ncpl_dyn":
                i.append(f"cav_{num}")
                num +=1
        return lattice

    #增加开关
    def add_element_on_command(self,  lattice):
        lattice = copy.deepcopy(lattice)
        if lattice[0][0] != "start":
            print("No start command")

        quad_dyn_on = ["err_quad_dyn_on"] +[1] * 7
        cav_dyn_on = ["err_cav_dyn_on"] +[1] * 7

        lattice.insert(1, quad_dyn_on)
        lattice.insert(1, cav_dyn_on)
        return lattice

    def add_beam_err_command(sel,lattice):
        err_beam_dyn_on = ["err_beam_dyn_on"] +[1] *13
        err_beam_dyn = ["err_beam_dyn", 0] + [0] *13

        lattice= copy.deepcopy(lattice)

        lattice.insert(1, err_beam_dyn)
        lattice.insert(1, err_beam_dyn_on)

        return lattice

    def add_err(self, lattice, err):
        """
        为lattice增加误差
        err:二维列表，元素为err_type, err_index, err_choose, err_value
        """

        lattice = copy.deepcopy(lattice)
        for i in lattice:
            for j in err:
                if i[0] == "err_beam_dyn":
                    if i[0] == j[0]:
                        i[j[2] + 2] = j[3]

                elif i[0] == j[0] and int(i[-1].split("_")[-1]) == j[1]:
                    i[j[2] + 3] = j[3]



        return lattice




    def get_err_element_num(self, lattice):
        quad_num = 0
        cav_num = 0
        for i in lattice:
            if i[0] == "err_quad_ncpl_dyn":
                quad_num += 1
            elif i[0] == "err_cav_ncpl_dyn":
                cav_num += 1
        return quad_num, cav_num

    def generate_max_element_err(self, quad_num, cav_num):
        #该功能为产生所有原件的最大误差命令课表
        #元素为err_type, err_index, err_choose, err_value
        lis = []
        #此处只产生元件误差
        for i in range(quad_num):
            for j in range(self.err_quad_parameter_num):
                v_lis = ["err_quad_ncpl_dyn", i, j, self.err_quad_max_value_lis[j]]
                lis.append(v_lis)

        for i in range(cav_num):
            for j in range(self.err_cav_parameter_num):
                v_lis = ["err_cav_ncpl_dyn", i, j, self.err_cav_max_value_lis[j]]
                lis.append(v_lis)
        return lis



    def write_to_lattice(self, lattice):
        lattice = copy.deepcopy(lattice)
        for i in lattice:
            if i[0] == "err_quad_ncpl_dyn" or i[0] =="err_cav_ncpl_dyn":
                i.pop()
        with open(self.lattice_path, 'w') as f:
            for i in lattice:
                f.write(' '.join(map(str, i)) + '\n')


    def basic_simulate(self, project_path, out_putfile):
        AVAS_obj = AVAS(project_path)
        res = AVAS_obj.run(output_file=out_putfile)
        print("模拟结束")

    def simulate(self, lattice):
        self.write_to_lattice(lattice)

        process = multiprocessing.Process(target=self.basic_simulate,
                                          args=(self.project_path, 'outputfile\error_middle'))

        process.start()  # 启动子进程
        process.join()  # 等待子进程运行结束

        suffix = self.get_max_file_suffix(self.error_output_path) + 1
        new_name = f"output_{suffix}"

        copy_file(self.lattice_path, self.error_middle_output0_path)

        copy_directory(self.error_middle_output0_path, self.error_output_path, new_name)
        delete_directory(self.error_middle_output0_path)

    def get_max_file_suffix(self, directory):
        #得到该文件夹的最大后缀
        """
        查找一个文件夹下面的所有文件
        :param directory:
        :return:【】

        """

        suffix = []


        res = list_files_in_directory(directory)
        for i in res:
            suffix.append(int(i.split("_")[-1]))

        if len(suffix) == 0:
            max_suffix = -1
        else:
            max_suffix = max(suffix)
        print(max_suffix)
        return max_suffix


    def add_max_err_run(self):
        # 为每个原件设置最大误差，并且进行模拟
        lattice = self.generate_basic_lattice()
        quad_num, cav_num = self.get_err_element_num(lattice)
        com_lis = self.generate_max_element_err(quad_num, cav_num)
        print(com_lis)

        for i in com_lis[:2]:
            new_lattice = self.add_err(lattice, [i])
            self.simulate(new_lattice)



    def test(self):
        # lattice = self.generate_basic_lattice()

        # lis = [["err_beam_dyn", 0, 0, 5],
        #     ["err_quad_ncpl_dyn", 0, 0, 5],
        #        ["err_quad_ncpl_dyn", 1, 0, 5]
        #        ]
        # lattice = self.add_err(lattice, lis)
        # for i in lattice:
        #     print(i)
        # self.add_max_err_run()
        self.add_max_err_run()
if __name__ == "__main__":
    obj = EA(r"C:\Users\anxin\Desktop\test_mulp")
    obj.test()