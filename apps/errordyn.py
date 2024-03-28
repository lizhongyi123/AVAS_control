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
from utils.treatlist import flatten_list, list_one_two

# 工作流程：
#    generate_adjust_parameter：根据lattice_mulp记录需要adjust的元件及参数位置，这里的位置是整个
#    lattice_mulp中所有的内容转换成list

#    get_goal：修改参数，添加end，然后写入lattice
#    根据诊断命令，计算loss

import os
import sys

# for i in sys.path:
#     print(i)
sys.path.append(r'C:\Users\anxin\Desktop\AVAS_control')
from sko.GA import GA

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
from utils.treatlist import flatten_list, list_one_two


class ErrorAnalysis():
    """
    该类为误差分析
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
        self.ini = []
        self.error_elemment_command = global_varible.error_elemment_command
        self.error_elemment_stat = global_varible.error_elemment_command_stat
        self.error_elemment_dyn = global_varible.error_elemment_command_dyn

        self.error_beam_command = global_varible.error_beam_command
        self.error_beam_stat = global_varible.error_beam_stat
        self.error_beam_dyn = global_varible.error_beam_dyn

        self.all_group = 1
        self.all_time = 1
        self.lattice_mulp_list = []

        # self.err_beam_stat_on = [0] * 25
        # self.err_quad_stat_on = [0, 0, 0, 0, 0, 0, 0]
        # self.err_cav_stat_on = [0, 0, 0, 0, 0, 0, 0]
        #
        # self.err_beam_dyn_on = [0] * 25
        # self.err_quad_dyn_on = [0, 0, 0, 0, 0, 0, 0]
        # self.err_cav_dyn_on = [0, 0, 0, 0, 0, 0, 0]

        self.err_beam_stat_on = []
        self.err_quad_stat_on = []
        self.err_cav_stat_on = []

        self.err_beam_dyn_on = []
        self.err_quad_dyn_on = []
        self.err_cav_dyn_on = []

        # 只优化
        self.only_adjust_sign = 0
        self.stat_dyn = 0  # 动态静态误差

        self.stat_dyn_err_lattice = []
        self.decimal = 5  # 小数点保留多少位

        self.result_queue = multiprocessing.Queue()
        if os.path.exists(self.error_middle_path):
            delete_directory(self.error_middle_path)
        os.makedirs(self.error_middle_path)

        if os.path.exists(self.error_output_path):
            delete_directory(self.error_output_path)
        os.makedirs(self.error_output_path)

    def delete_element_end_index(self, error_lattice):
        error_lattice_copy = copy.deepcopy(error_lattice)
        for i in error_lattice_copy:
            if i[0] in global_varible.long_element:
                i.pop()
        return error_lattice_copy

    def get_group_time(self):
        """
        得到group和time
        :return:
        """
        input_lines = []
        # with open(self.lattice_mulp_path, encoding='utf-8') as file_object:
        #     for line in file_object:
        #             input_lines.append(line)

        # input_lines = [i.split() for i in input_lines if i.strip()]

        input_lines = read_txt(self.lattice_mulp_path, out='list')

        for i in input_lines:
            if i[0] == 'err_step':
                self.all_group = int(i[1])
                self.all_time = int(i[2])

            elif i[0] == 'err_beam_stat_on':
                self.err_beam_stat_on = [int(j) for j in i[1:]]
                self.err_beam_stat_on += [0] * (25 - len(self.err_beam_stat_on))

            elif i[0] == 'err_quad_stat_on':
                self.err_quad_stat_on = [int(j) for j in i[1:]]
                self.err_quad_stat_on += [0] * (7 - len(self.err_quad_stat_on))

            elif i[0] == 'err_cav_stat_on':
                self.err_cav_stat_on = [int(j) for j in i[1:]]
                self.err_cav_stat_on += [0] * (7 - len(self.err_cav_stat_on))

            elif i[0] == 'err_beam_dyn_on':
                self.err_beam_dyn_on = [int(j) for j in i[1:]]
                self.err_beam_dyn_on += [0] * (25 - len(self.err_beam_dyn_on))

            elif i[0] == 'err_quad_dyn_on':
                self.err_quad_dyn_on = [int(j) for j in i[1:]]
                self.err_quad_dyn_on += [0] * (7 - len(self.err_quad_dyn_on))

            elif i[0] == 'err_cav_dyn_on':
                self.err_cav_dyn_on = [int(j) for j in i[1:]]
                self.err_cav_dyn_on += [0] * (7 - len(self.err_cav_dyn_on))

    def increase_error(self, input_lines):
        """
        向叠加场中添加误差, 将一个误差命令添加到所有的元件上
        """
        N = -1
        command = []
        error_use_index = 0

        res = copy.deepcopy(input_lines)

        for i in range(len(input_lines)):
            if input_lines[i][0] in self.error_elemment_command and N == -1 and input_lines[i][-1] is False:
                N = int(input_lines[i][1])
                command = input_lines[i]
                command[1] = 1
                error_use_index = i

            elif N == -1:
                continue

            elif N == 0 or input_lines[i][0] == 'end':
                res[error_use_index][-1] = True

                err_judge = []
                for i in res:
                    if i[0] in global_varible.error_elemment_command:
                        err_judge.append(i[-1])

                # 当全部都是True
                if all(err_judge):
                    return res

                else:

                    return self.increase_error(res)


            elif input_lines[i][0] in global_varible.long_element and N > 0:
                # 在叠加场添加磁场原件误差
                if input_lines[i][0] == 'field' and input_lines[i][4] == '3':
                    if command[0] in global_varible.error_elemment_command_quad:
                        res[i].append(command)

                # 在叠加场添加高频腔原件误差
                if input_lines[i][0] == 'field' and input_lines[i][4] == '1':
                    if command[0] in global_varible.error_elemment_command_cav:
                        res[i].append(command)

                N -= 1

    def get_dimension(self, lst):
        if not isinstance(lst, list):
            return 0  # 不是列表，维度为 0
        else:
            return 1 + max(self.get_dimension(item) for item in lst)

    def generate_lattice_mulp_list(self):
        """
        :return:

        """
        lattice_mulp_path = os.path.join(self.project_path, 'InputFile', 'lattice_mulp.txt')
        # input_lines = []
        # with open(lattice_mulp_path, encoding='utf-8') as file_object:
        #     for line in file_object:
        #         input_lines.append(line)

        # input_lines = [i.split() for i in input_lines if i.strip()]

        input_lines = read_txt(lattice_mulp_path, out='list')

        inpiut_lines_copy = copy.deepcopy(input_lines)

        for i in range(len(input_lines)):
            if input_lines[i][0] in self.error_elemment_command:
                inpiut_lines_copy[i].append(False)

        res = self.increase_error(inpiut_lines_copy)

        res = [i for i in res if i[0] not in global_varible.error_elemment_command]

        res_treat = []
        for i in res:
            if self.get_dimension(i) == 1:
                res_treat.append(i)

            elif self.get_dimension(i) != 1:
                lis = []
                err_command_exist = []

                i_copy = copy.deepcopy(i)
                for j in i[::-1]:
                    if isinstance(j, list) and j[0] not in err_command_exist:
                        lis.append(j)
                        err_command_exist.append(j[0])
                        i_copy.pop()
                    # 如果已经出现过
                    elif isinstance(j, list) and j[0] in err_command_exist:
                        i_copy.pop()

                    else:
                        lis.append(i_copy)
                        break

                for k in lis:
                    k = copy.deepcopy(k)
                    res_treat.append(k)

        # for i in res_treat:
        #     print(i)
        # breakpoint()

        for i in res_treat:
            if i[0] in self.error_elemment_command:
                i.pop()

        # for i in res_treat:
        #     print(i)
        # breakpoint()

        # 为每个元件加编号
        index = 0
        for i in res_treat:
            if i[0] in global_varible.long_element:
                add_name = f'element_{index}'
                i.append(add_name)
                index += 1
        # print("------------------------")
        # for i in res_treat:
        #     print(i)
        #
        # breakpoint()

        self.lattice_mulp_list = res_treat
        # for i in res_treat:
        #     print(i)

    def generate_error(self, input, group):
        """
        根据每一个error命令产生对应的error
        :param input:
        :param group:
        :return:
        """
        target = None

        if input[0] in self.error_elemment_command:
            input = input + [0] * (10 - len(input))
            target = input

            if int(input[2]) == 0:
                target = input

            elif int(input[2]) == 1:
                for i in range(3, len(input) - 1):
                    dx = float(input[i]) / self.all_group
                    target[i] = round(random.uniform(-1 * dx * (group + 1), dx * (group + 1)), self.decimal)
                target[2] = 0


            elif int(input[2]) == -1:
                for i in range(3, len(input) - 1):
                    dx = float(input[i]) / self.all_group
                    target[i] = round(random.gauss(0, dx * (group + 1)), self.decimal)
                target[2] = 0

            elif int(input[2]) == 2:
                for i in range(3, len(input) - 1):
                    dx = float(input[i]) / self.all_group
                    target[i] = dx * (group + 1)
                target[2] = 0

        if input[0] in self.error_beam_command:
            input = input + [0] * (27 - len(input))

            target = input

            if int(input[1]) == 0:
                target = input

            elif int(input[1]) == 1:
                for i in range(2, len(input)):
                    dx = float(input[i]) / self.all_group
                    target[i] = round(random.uniform(-1 * dx * (group + 1), dx * (group + 1)), self.decimal)
                target[1] = 0


            elif int(input[1]) == -1:
                for i in range(2, len(input)):
                    dx = float(input[i]) / self.all_group
                    target[i] = round(random.gauss(0, dx * (group + 1)), self.decimal)
                target[1] = 0

            elif int(input[1]) == 2:
                for i in range(2, len(input)):
                    dx = float(input[i]) / self.all_group
                    target[i] = dx * (group + 1)
                target[1] = 0

        if input[0] == 'err_quad_ncpl_stat':
            for i in range(len(self.err_quad_stat_on)):
                if int(self.err_quad_stat_on[i]) == 0:
                    target[i + 3] = 0

        elif input[0] == 'err_quad_ncpl_dyn':
            for i in range(len(self.err_quad_dyn_on)):
                if int(self.err_quad_dyn_on[i]) == 0:
                    target[i + 3] = 0

        elif input[0] == 'err_cav_ncpl_stat':
            for i in range(len(self.err_cav_stat_on)):
                if int(self.err_cav_stat_on[i]) == 0:
                    target[i + 3] = 0

        elif input[0] == 'err_cav_ncpl_dyn':
            for i in range(len(self.err_cav_dyn_on)):
                if int(self.err_cav_dyn_on[i]) == 0:
                    target[i + 3] = 0

        elif input[0] == 'err_beam_stat':
            for i in range(len(self.err_beam_stat_on)):
                if int(self.err_beam_stat_on[i]) == 0:
                    target[i + 2] = 0

        elif input[0] == 'err_beam_dyn':

            for i in range(len(self.err_beam_dyn_on)):
                if int(self.err_beam_dyn_on[i]) == 0:
                    target[i + 2] = 0

        return target

    def generate_error_lattice(self, group, time):
        """
        将lattice_mulp写进新的lattice，将误差变成AVAS后端需要的情况
        :param group:
        :return:
        """

        input_lines = copy.deepcopy(self.lattice_mulp_list)

        for i in range(len(input_lines)):
            if len(input_lines[i]) == 0:
                continue

            elif input_lines[i][0] == 'err_step':
                input_lines[i] = ['err_step', '1', '1']


            elif input_lines[i][0] in self.error_elemment_command or \
                    input_lines[i][0] in self.error_beam_command:

                input_lines[i] = self.generate_error(input_lines[i], group)

        return input_lines








    def run_avas(self, p_path, out_putfile_):
        AVAS_obj = AVAS(p_path)
        res = AVAS_obj.run(output_file=out_putfile_)






    def run_err_one_time(self, group, time, type_):
        """
        静态误差或杂动态误差
        跑一次，但是不需要优化
        :param group:
        :param time:
        :return:
        """
        error_lattice = self.generate_error_lattice(group, time)

        error_lattice = self.delete_element_end_index(error_lattice)

        if type_ == 'stat':
            for i in error_lattice:

                if i[0] in self.error_elemment_dyn or i[0] in self.error_beam_dyn:
                    i[0] = "!" + i[0]
                # 如果是静态误差，变成动态误差
                elif i[0] == 'err_beam_stat':
                    i[0] = 'err_beam_dyn'

                elif i[0] == 'err_quad_ncpl_stat':
                    i[0] = 'err_quad_ncpl_dyn'

                elif i[0] == 'err_cav_ncpl_stat':
                    i[0] = 'err_cav_ncpl_dyn'


                # 开关
                elif i[0] in global_varible.error_elemment_dyn_on or i[0] == 'err_beam_dyn_on':
                    i[0] = "!" + i[0]

                elif i[0] == 'err_beam_stat_on':
                    i[0] = 'err_beam_dyn_on'

                elif i[0] == global_varible.error_elemment_stat_on[0]:
                    i[0] = global_varible.error_elemment_dyn_on[0]

                elif i[0] == global_varible.error_elemment_stat_on[1]:
                    i[0] = global_varible.error_elemment_dyn_on[1]

        if type_ == 'dyn':
            for i in error_lattice:
                # 静态误差注释掉
                if i[0] in self.error_elemment_stat or i[0] in self.error_beam_stat:
                    i[0] = "!" + i[0]

                # 开关
                elif i[0] in global_varible.error_elemment_stat_on or i[0] == 'err_beam_stat_on':
                    i[0] = "!" + i[0]

        with open(self.lattice_path, 'w') as f:
            for i in error_lattice:
                f.write(' '.join(map(str, i)) + '\n')

        new_name = f'output_{group}_{time}'

        copy_directory(self.error_middle_output0_path, self.error_output_path, new_name)

        delete_directory(self.error_middle_output0_path)



    def run_err_dyn_all_group(self):
        """
        跑动态误差
        :return:
        """

        self.get_group_time()
        self.generate_lattice_mulp_list()

        for i in range(self.all_group):
            for j in range(self.all_time):
                print(i, j)
                self.run_err_one_time(i, j, 'dyn')


if __name__ == "__main__":
    # obj = ErrorStat(r'C:\Users\anxin\Desktop\test_control\test_error')
    # obj.read_lattice_parameter()
    # obj.generate_error_lattice(1)
    # obj.generate_adjust_parameter()
    # # obj.optimize_one_group(1)
    # obj.treat_diag()

    start = time.time()
    print("start", start)
    obj = ErrorAnalysis(r'C:\Users\anxin\Desktop\test2')
    # obj.run_err_stat_dyn_all_group(False)
    # obj.optimize_all_group()
    obj.only_adjust()

    end = time.time()
    print("end", end)


