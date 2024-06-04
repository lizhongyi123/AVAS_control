#工作流程：
#    generate_adjust_parameter：根据lattice_mulp记录需要adjust的元件及参数位置，这里的位置是整个
#    lattice_mulp中所有的内容转换成list

#    get_goal：修改参数，添加end，然后写入lattice
#    根据诊断命令，计算loss

import os
import sys

# for i in sys.path:
#     print(i)
sys.path.append(r'C:\Users\anxin\Desktop\AVAS_control')
# from sko.GA import GA

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

        #只优化
        self.only_adjust_sign = 0
        self.stat_dyn = 0 #动态静态误差


        self.stat_dyn_err_lattice = []
        self.decimal = 5 #小数点保留多少位
        
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
                self.all_time =int(i[2])

            elif i[0] == 'err_beam_stat_on':
                self.err_beam_stat_on = [int(j) for j in i[1: ]]
                self.err_beam_stat_on += [0] * (25 - len(self.err_beam_stat_on))

            elif i[0] == 'err_quad_stat_on':
                self.err_quad_stat_on = [int(j) for j in i[1: ]]
                self.err_quad_stat_on += [0] * (7 - len(self.err_quad_stat_on))

            elif i[0] == 'err_cav_stat_on':
                self.err_cav_stat_on = [int(j) for j in i[1: ]]
                self.err_cav_stat_on += [0] * (7 - len(self.err_cav_stat_on))

            elif i[0] == 'err_beam_dyn_on':
                self.err_beam_dyn_on = [int(j) for j in i[1: ]]
                self.err_beam_dyn_on += [0] * (25 - len(self.err_beam_dyn_on))

            elif i[0] == 'err_quad_dyn_on':
                self.err_quad_dyn_on = [int(j) for j in i[1: ]]
                self.err_quad_dyn_on += [0] * (7 - len(self.err_quad_dyn_on))

            elif i[0] == 'err_cav_dyn_on':
                self.err_cav_dyn_on = [int(j) for j in i[1: ]]
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
                    #如果已经出现过
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

        #为每个元件加编号
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
            input = input + [0] * (10-len(input))
            target = input

            if int(input[2]) == 0:
                target = input

            elif int(input[2]) == 1:
                for i in range(3, len(input)-1):
                    dx = float(input[i])/self.all_group
                    target[i] =round(random.uniform(-1 * dx * (group+1), dx * (group+1)),  self.decimal)
                target[2] = 0


            elif int(input[2]) == -1:
                for i in range(3, len(input) -1):
                    dx = float(input[i])/self.all_group
                    target[i] = round(random.gauss(0, dx * (group+1)),  self.decimal)
                target[2] = 0

            elif int(input[2]) == 2:
                for i in range(3, len(input) -1):
                    dx = float(input[i])/self.all_group
                    target[i] = dx * (group+1)
                target[2] = 0

        
        if input[0] in self.error_beam_command:
            input = input + [0] * (27 - len(input))

            target = input

            if int(input[1]) == 0:
                target = input

            elif int(input[1]) == 1:
                for i in range(2, len(input)):
                    dx = float(input[i])/self.all_group
                    target[i] = round(random.uniform(-1 * dx * (group+1), dx * (group+1)),  self.decimal)
                target[1] = 0


            elif int(input[1]) == -1:
                for i in range(2, len(input)):
                    dx = float(input[i])/self.all_group
                    target[i] = round(random.gauss(0, dx * (group+1)),  self.decimal)
                target[1] = 0

            elif int(input[1]) == 2:
                for i in range(2, len(input)):
                    dx = float(input[i])/self.all_group
                    target[i] = dx * (group+1)
                target[1] = 0


        if input[0] == 'err_quad_ncpl_stat':
            for i in range(len(self.err_quad_stat_on)):
                if int(self.err_quad_stat_on[i]) == 0:
                    target[i+3] = 0

        elif input[0] == 'err_quad_ncpl_dyn':
            for i in range(len(self.err_quad_dyn_on)):
                if int(self.err_quad_dyn_on[i]) == 0:
                    target[i+3] = 0

        elif input[0] == 'err_cav_ncpl_stat':
            for i in range(len(self.err_cav_stat_on)):
                if int(self.err_cav_stat_on[i]) == 0:
                    target[i+3] =0

        elif input[0] == 'err_cav_ncpl_dyn':
            for i in range(len(self.err_cav_dyn_on)):
                if int(self.err_cav_dyn_on[i]) == 0:
                    target[i+3] = 0

        elif input[0] == 'err_beam_stat':
            for i in range(len(self.err_beam_stat_on)):
                if int(self.err_beam_stat_on[i]) == 0:
                    target[i+2] = 0

        elif input[0] == 'err_beam_dyn':

            for i in range(len(self.err_beam_dyn_on)):
                if int(self.err_beam_dyn_on[i]) == 0:
                    target[i+2] = 0

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



    def generate_adjust_parameter(self):
        """
        产生定位信息, adjust命令中哪些参数需要修改
        """
        adjust_parameter_lattice_command = [] #原来的命令
        adjust_element_num = [] #第几个元件要改
        adjust_parameter_num = [] #第几个参数要改
        adjust_parameter_range = []#参数的范围
        adjust_parameter_n = []
        adjust_parameter_use_init = []#是否使用初值
        adjust_parameter_initial_value = []
        adjust_parameter_constraint = []#约束条件
        adjust_parameter_link = [] #l



        input_lines = self.lattice_mulp_list

        adjust_parameter_num_per = []
        adjust_parameter_range_per = []
        adjust_parameter_n_per = []
        adjust_parameter_use_init_per = []
        index = -1


        for i in range(len(input_lines)):
            if input_lines[i][0] in global_varible.long_element:
                index += 1


            if input_lines[i][0] == 'adjust':
                adjust_parameter_num_per.append(int(input_lines[i][2]))
                adjust_parameter_range_per.append([float(input_lines[i][4]), float(input_lines[i][5])])
                adjust_parameter_n_per.append(int(input_lines[i][3]))
                adjust_parameter_use_init_per.append(int(input_lines[i][6]))

                tmp_index = index + 1

                if tmp_index not in adjust_element_num:
                    adjust_element_num.append(tmp_index)
            elif input_lines[i][0] != 'adjust' and input_lines[i-1][0] == 'adjust':

                adjust_parameter_lattice_command.append(input_lines[i])

                adjust_parameter_num.append(copy.deepcopy(adjust_parameter_num_per))

                adjust_parameter_initial_value_per = [float(input_lines[i][j]) for j in adjust_parameter_num_per]
                adjust_parameter_initial_value.append(adjust_parameter_initial_value_per)

                adjust_parameter_num_per.clear()



                adjust_parameter_range.append(copy.deepcopy(adjust_parameter_range_per))
                adjust_parameter_range_per.clear()

                adjust_parameter_n.append(copy.deepcopy(adjust_parameter_n_per))
                adjust_parameter_n_per.clear()


                adjust_parameter_use_init.append(copy.deepcopy(adjust_parameter_use_init_per))
                adjust_parameter_use_init_per.clear()


        # print(adjust_parameter_num, adjust_parameter_range, adjust_parameter_n, adjust_parameter_use_init)
        return adjust_parameter_lattice_command, adjust_element_num, adjust_parameter_initial_value, adjust_parameter_num, adjust_parameter_range, \
               adjust_parameter_n, adjust_parameter_use_init
        # print(adjust_parameter_num, adjust_parameter_range, adjust_parameter_n, adjust_parameter_use_init)

    @staticmethod
    def find_index(position, position_list):
        """
           此函数是用来寻找第一个大于目标位置的索引
        """
        first_value = 0
        for i in position_list:
            if i >= position:
                first_value= i
                break
        if first_value == 0:
            raise Exception("没有找到大于diag命令的位置")


        index = position_list.index(first_value)


        return index



    @staticmethod
    def interpolation_(position, position_front, position_behind, target_front, target_behind):
        ratio_front = (position - position_front) / (position_behind - position_front)
        ratio_behind = (position_behind - position) / (position_behind-position_front)

        target = ratio_behind * target_front + ratio_front * target_behind

        return target



    def treat_diag(self, ):
        """
        得到loss
        :return:
        """
        # 读取新的lattice信息

        input_lines = []

        # with open(self.lattice_path, encoding='utf-8') as file_object:
        #     for line in file_object:
        #         input_lines.append(line)


        # input_lines = [i.split() for i in input_lines if i.strip()]
        input_lines = read_txt(self.lattice_path, out='list')


        # 产生每一个diag针对的位置
        lattice_obj = LatticeParameter(self.lattice_path)
        lattice_obj.get_parameter()

        diag_index = []
        diag_command_list = []
        index = -1


        for i in input_lines:
            if i[0] in global_varible.long_element:
                index += 1
            if i[0].startswith("diag"):
                diag_index.append(index)
                diag_command_list.append(i)

        diag = []

        for i in range(len(diag_index)):
            dic = {}
            dic['diag_command'] = diag_command_list[i]
            dic['diag_order'] = i
            dic['position'] = lattice_obj.v_start[diag_index[i]] + lattice_obj.v_len[diag_index[i]]
            diag.append(dic)



        # dataset_path = os.path.join(output_0_path,  'dataset.txt')

        # dataset_obj = DatasetParameter(dataset_path)
        # dataset_obj.get_parameter()

        # z_ = dataset_obj.z



        # print(index)
        # print(z_[191], z_[192])
        dst_path = ''
        all_file = list_files_in_directory(self.error_middle_output0_path)

        loss_type = []
        loss_list = []

        for i in diag:
            position = round(i['position'], 3)
            print('position', position)
            position = str(format(position, '.6f'))



            for file in all_file:
                if position in file:
                    dst_path = file

            if os.path.exists(dst_path):
                pass
            else:
                print("错误", dst_path)

            obj = DstParameter(dst_path)
            obj.get_parameter()

            center_x = obj.center_x
            center_y = obj.center_y

            rms_x = obj.rms_x
            rms_y = obj.rms_y

            energy = obj.energy

            # index = self.find_index(position, z_)
            if i['diag_command'][0] == 'diag_position':
                # dataset_obj.x = [i * 1000 for i in dataset_obj.x]
                # dataset_obj.y = [i * 1000 for i in dataset_obj.y]
                
                target_x, target_y = float(i['diag_command'][2]), float(i['diag_command'][3])
                accuracy = float(i['diag_command'][4])

                # res_x = self.interpolation_(position, z_[index-1], z_[index], dataset_obj.x[index-1],
                #                             dataset_obj.x[index])

                # res_y = self.interpolation_(position, z_[index-1], z_[index], dataset_obj.y[index-1],
                #                             dataset_obj.y[index])

                loss = ((center_x - target_x) **2)/(target_x+1) + ((center_y - target_y) **2)/(target_y+1)
                loss_list.append(loss)
                loss_type.append('diag_position')

            if i['diag_command'][0] == 'diag_size':
                #变成mm
                # dataset_obj.rms_x = [i * 1000 for i in dataset_obj.rms_x]
                # dataset_obj.rms_y = [i * 1000 for i in dataset_obj.rms_y]
            
                target_x, target_y = float(i['diag_command'][2]), float(i['diag_command'][3])

                accuracy = float(i['diag_command'][4])

                # res_x = self.interpolation_(position, z_[index - 1], z_[index], dataset_obj.rms_x[index - 1],
                #                             dataset_obj.rms_x[index])

                # res_y = self.interpolation_(position, z_[index - 1], z_[index], dataset_obj.rms_y[index - 1],
                #                             dataset_obj.rms_y[index])

                loss = ((rms_x - target_x) ** 2)/(target_x+1) + ((rms_y - target_y) ** 2)/(target_y+1)
                loss_list.append(loss)

                loss_type.append('diag_size')

            if i['diag_command'][0] == 'diag_energy':
                target_energy = float(i['diag_command'][2])

                # res_energy = self.interpolation_(position, z_[index - 1], z_[index], dataset_obj.ek[index - 1],
                #                             dataset_obj.ek[index])


                res_energy = obj.energy

                print('target_energy', target_energy)
                print('res_energy', res_energy)

                accuracy = float(i['diag_command'][3])

                loss = ((energy - target_energy) ** 2 ) / (target_energy + 1)

                loss_list.append(loss)
                loss_type.append('diag_energy')

        all_loss = 0
        for i in loss_list:
            all_loss += i

        return all_loss



    def run_avas(self, p_path, out_putfile_ ):
        AVAS_obj = AVAS(p_path)
        res = AVAS_obj.run(output_file = out_putfile_)

    def get_goal(self, error_lattice, adjust_element_num, adjust_parameter_num ):
        def goal(x):
            print("--------------------")
            print('x', x)
            
            self.ini_this.append(x)

            # x =np.array(x).reshape(np.array(adjust_parameter_num).shape)

            x = list_one_two(list(x), adjust_parameter_num)



            # for i in range(len(adjust_element_num)):
            #     for j in range(len(adjust_parameter_num[i])):
            #         error_lattice[adjust_element_num[i]][adjust_parameter_num[i][j]] = x[i][j]


            for i in range(len(adjust_element_num)):
                for j in range(len(adjust_parameter_num[i])):
                    for com in error_lattice:
                        if com[-1] == f'element_{adjust_element_num[i]}':
                            com[adjust_parameter_num[i][j]] = x[i][j]
                            break
            #删除error_lattice最后的编号
            error_lattice_1 = self.delete_element_end_index(error_lattice)

            # for i in error_lattice_1:
            #     print(i)
            # breakpoint()
            # print(error_lattice)

            # for i in range(len(error_lattice)):
            #     if error_lattice[i][0].startswith("diag"):
            #         error_lattice.insert(i+1, ['OutputPlane', 0])
            #将最后一个束诊命令后面加上end

            error_lattice_write = copy.deepcopy(error_lattice_1)

            for index, i in enumerate(error_lattice[::-1]):
                index = -1 * index -1
                if index == -1 and i[0].startswith("diag"):
                    break

                if index == -2 and i[0].startswith("diag"):
                    break
                
                if i[0].startswith("diag"):
                    error_lattice_write.insert(index + 1, ['end'])
                    break

            # for i in error_lattice_write:
            #     print(i)
            #     print(id(i))
            # print('*-')

            for i in error_lattice_write:

                if i[0] in self.error_elemment_dyn or i[0] in self.error_beam_dyn:
                    i[0] = "!" + i[0]
                #如果是静态误差，变成动态误差
                elif i[0] == 'err_beam_stat':
                    i[0] = 'err_beam_dyn'

                elif i[0] == 'err_quad_ncpl_stat':
                    i[0] = 'err_quad_ncpl_dyn'

                elif i[0] == 'err_cav_ncpl_stat':
                    i[0] = 'err_cav_ncpl_dyn'


                #开关
                elif i[0] in global_varible.error_elemment_dyn_on:
                    i[0] = "!" + i[0]

                elif i[0] == global_varible.error_elemment_stat_on[0]:
                    i[0] = global_varible.error_elemment_dyn_on[0]

                elif i[0] == global_varible.error_elemment_stat_on[1]:
                    i[0] = global_varible.error_elemment_dyn_on[1]

                #     print(4)
                # print(2, i)


            with open(self.lattice_path, 'w') as f:
                for i in error_lattice_write:
                    f.write(' '.join(map(str, i)) + '\n')

            try:
                if self.only_adjust_sign == 1:
                    if os.path.exists(self.error_middle_output0_path):
                        delete_directory(self.error_middle_output0_path)
                    os.makedirs(self.error_middle_output0_path)
                    process = multiprocessing.Process(target=self.run_avas, args=(self.project_path, 'outputfile\error_middle\output_0'))
                else:
                    process = multiprocessing.Process(target=self.run_avas, args=(self.project_path, 'outputfile\error_middle'))

                process.start()  # 启动子进程
                process.join()   # 等待子进程运行结束
                process.terminate()  # 终止子进程
                
                loss = self.treat_diag()

            except Exception as e:
                # 处理异常，如果需要
                print(f"An error occurred: {str(e)}")
                loss = 1

            finally:
                if process.is_alive():
                    process.terminate()  # 终止子进程

            error_middle_ouput_0 = self.error_middle_output0_path
            delete_directory(error_middle_ouput_0)
            

            print(loss)
            self.loss_this.append(loss)
            print("--------------------")

            if loss < 0.01:
                raise Exception('已小于0.01')

            return loss

        return goal




    def run_use_corrected_result(self, corrected_result, group, time, error_lattice, 
                                  adjust_element_num, adjust_parameter_num):
    
        # x =np.array(corrected_result).reshape(np.array(adjust_parameter_num).shape)
        x = list_one_two(list(corrected_result), adjust_parameter_num)

        for i in range(len(adjust_element_num)):
            for j in range(len(adjust_parameter_num[i])):
                for com in error_lattice:
                    if com[-1] == f'element_{adjust_element_num[i]}':
                        com[adjust_parameter_num[i][j]] = x[i][j]
                        break
        # 删除error_lattice最后的编号
        error_lattice = self.delete_element_end_index(error_lattice)
    
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

    
        with open(self.lattice_path, 'w') as f:
            for i in error_lattice:
                f.write(' '.join(map(str, i)) + '\n')
    

        if self.only_adjust_sign == 1:
            process = multiprocessing.Process(target=self.run_avas, args=(self.project_path, 'outputfile'))
        else:
            process = multiprocessing.Process(target=self.run_avas, args=(self.project_path, 'outputfile\error_middle'))

        process.start()  # 启动子进程
        process.join()   # 等待子进程运行结束
        process.terminate()  # 终止子进程
        
        if self.only_adjust_sign == 1:
            return 0

        new_name = f'output_{group}_{time}'

        copy_directory(self.error_middle_output0_path, self.error_output_path , new_name)

        delete_directory(self.error_middle_output0_path)


    def optimize_one_group(self, group, time, error_lattice, 
                             adjust_element_num, adjust_parameter_initial_value, adjust_parameter_num, adjust_parameter_range, \
        adjust_parameter_n, adjust_parameter_use_init):

        #lattice中原本的初值
        # lattice_initial_value =np.array(adjust_parameter_initial_value).reshape(-1)

        lattice_initial_value = flatten_list(adjust_parameter_initial_value)
        
        # print('lattice_initial_value', lattice_initial_value)


        #范围
        parameter_range = np.array(flatten_list(adjust_parameter_range)).reshape(-1, 2)
        # print('parameter_range', parameter_range)

        #随机初值
        random_initial_value = [random.uniform(i[0], i[1]) for i in parameter_range]

        #是否使用初值
        # use_initial_value = np.array(adjust_parameter_use_init).reshape(-1)
        use_initial_value = np.hstack(adjust_parameter_use_init)
        #最终初值
        initial_value = random_initial_value
        for i in range(len(initial_value)):
            if use_initial_value[i] == 1:
                initial_value[i] = lattice_initial_value[i]

        # print('initial_value', initial_value)

        #是否使用相同的值
        # n_ = np.array(adjust_parameter_n).reshape(-1)
        n_ = flatten_list(adjust_parameter_n)
        # print('n_', n_)

        unique_elements, unique_indices = np.unique(n_, return_index=True)
        # print(unique_elements)
        indiaces = []

        for i in range(len(unique_elements)):
            if unique_elements[i] != 0:
                indiaces.append([index for index, element in enumerate(n_) if element == unique_elements[i]])
        # print('indiaces', indiaces)
        # breakpoint()

        constraints = []
        for i in indiaces:
            if len(i) == 1:
                continue
            for j in range(1, len(i)):
                # print([i[j]], i[0])
                initial_value[i[j]] = initial_value[i[0]]
                constraints.append( {'type': 'eq', 'fun': lambda x: x[i[j]] -x[i[0]]} )

        # print(initial_value)

        # for constraint in constraints:
        #     print('约束条件函数结果:', constraint)


        goal = self.get_goal(error_lattice, adjust_element_num, adjust_parameter_num)

        options = {'maxiter': 100}
        
        self.ini_this=[]
        self.loss_this = []


        try:
            result = minimize(fun=goal, x0=initial_value, constraints=constraints, bounds=parameter_range,
                            method='SLSQP', options=options)
            
            return result.x, result.fun

        except Exception:
            return self.ini_this[-1], self.loss_this[-1]

        #
        # ga =GA(func=goal, n_dim=len(initial_value),size_pop =10, lb=[0],ub=[3], max_iter=2)
        #
        # best_x, best_y = [], []
        # for i in range(100):
        #     best_x, best_y=ga.run(1)
        #     if best_y[0]<1:
        #         break
        #
        # return best_x, best_y



    def stat_error_run_one_time(self, group, time):
        """
        静态误差完整跑一次, 需要矫正

        :param group:
        :param time:
        :return:
        """

        error_lattice = self.generate_error_lattice(group, time)

        
        if self.stat_dyn == 1:
            self.stat_dyn_err_lattice.append(error_lattice)

        #得到lattice的定位信息
        adjust_parameter_lattice_command, adjust_element_num, adjust_parameter_initial_value, adjust_parameter_num, adjust_parameter_range, \
        adjust_parameter_n, adjust_parameter_use_init = self.generate_adjust_parameter()

        # print(adjust_element_num, adjust_parameter_num)

        ini, loss = self.optimize_one_group(group, time, error_lattice,
                                             adjust_element_num, adjust_parameter_initial_value, adjust_parameter_num, adjust_parameter_range, \
                                            adjust_parameter_n, adjust_parameter_use_init)
        corrected_result = ini

        # best_x, best_y = self.optimize_one_group(group, time, error_lattice, adjust_parameter_lattice_command,
        #                                      adjust_element_num, adjust_parameter_initial_value, adjust_parameter_num, adjust_parameter_range, \
        # adjust_parameter_n, adjust_parameter_use_init)
        # corrected_result = best_x

        self.ini.append(ini)
        self.loss.append(loss)
        print(self.ini)
        self.run_use_corrected_result(corrected_result, group, time, error_lattice, 
                                  adjust_element_num, adjust_parameter_num)
        

    #静态误差并矫正
    def optimize_all_group(self):
        """
        静态误差及矫正
        :return:
        """

        self.get_group_time()
        self.generate_lattice_mulp_list()

        for i in range(self.all_group):
            for j in range(self.all_time):
                print(i, j)
                self.stat_error_run_one_time(i, j)
        
        print(self.ini)
        print(self.loss)



        #将结果保存到output文件中
        correct_initial_value_path = os.path.join(self.output_path, 'stat_error_correct_res.txt')

        with open(correct_initial_value_path, 'w') as f:
            for i in self.ini:
                f.write(' '.join(map(str, i)) + '\n')



########################################################
    def run_err_one_time(self, group, time, type_):
        """
        静态误差或动态误差
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
                #静态误差注释掉
                if i[0] in self.error_elemment_stat or i[0] in self.error_beam_stat:
                    i[0] = "!" + i[0]

                # 开关
                elif i[0] in global_varible.error_elemment_stat_on or i[0] == 'err_beam_stat_on':
                    i[0] = "!" + i[0]



        with open(self.lattice_path, 'w') as f:
            for i in error_lattice:
                f.write(' '.join(map(str, i)) + '\n')



        new_name = f'output_{group}_{time}'

        copy_directory(self.error_middle_output0_path, self.error_output_path , new_name)

        delete_directory(self.error_middle_output0_path)

    def run_err_stat_all_group(self):
        """
        跑静态误差
        :return:
        """

        self.get_group_time()
        self.generate_lattice_mulp_list()

        for i in range(self.all_group):
            for j in range(self.all_time):
                print(i, j)
                self.run_err_one_time(i, j, 'stat')




#########################################################
 
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



###############################################################


    def run_err_stat_dyn_one_time(self, x ,group, time, error_lattice, 
                                  adjust_element_num, adjust_parameter_num, opti):
        
        if opti:
            x = list_one_two(list(x), adjust_parameter_num)
            # print(adjust_parameter_num)
            print('x', x)
            for i in range(len(adjust_element_num)):
                for j in range(len(adjust_parameter_num[i])):
                    for com in error_lattice:
                        if com[-1] == f'element_{adjust_element_num[i]}':
                            com[adjust_parameter_num[i][j]] = x[i][j]


        ####################
        #将静态的动态误差的开启结合起来
        new_err_beam_dyn_on = ['err_beam_dyn_on']
        for i in range(len(self.err_beam_stat_on)):
            if self.err_beam_stat_on[i] == 1 or self.err_beam_dyn_on[i] == 1:
                new_err_beam_dyn_on.append(1)
            else:
                new_err_beam_dyn_on.append(0)

        new_err_quad_dyn_on = ['err_quad_dyn_on']
        for i in range(len(self.err_quad_dyn_on)):
            if self.err_quad_dyn_on[i] == 1 or self.err_quad_stat_on[i] == 1:
                new_err_quad_dyn_on.append(1)
            else:
                new_err_quad_dyn_on.append(0)

        new_err_cav_dyn_on = ['err_cav_dyn_on']
        for i in range(len(self.err_cav_dyn_on)):
            if self.err_cav_dyn_on[i] == 1 or self.err_cav_stat_on[i] == 1:
                new_err_cav_dyn_on.append(1)
            else:
                new_err_cav_dyn_on.append(0)

        tmp_err_beam_stat = []
        tmp_err_beam_dyn = []
        new_err_beam_dyn = ['err_beam_dyn']

        
        for i in range(len(error_lattice)):
            # 处理双误差情况
            if error_lattice[i][0] in global_varible.long_element:
                if error_lattice[i - 1][0] in global_varible.error_elemment_command and \
                        error_lattice[i - 2][0] in global_varible.error_elemment_command:

                    for j in range(3, len(error_lattice[i - 2])):
                        error_lattice[i - 2][j] += error_lattice[i - 1][j]
                    error_lattice[i - 1].insert(0, False)

                    #若果i-2是静态误差变成动态误差
                    if error_lattice[i - 2][0] == global_varible.error_elemment_command_stat[0]:
                        error_lattice[i - 2][0] = global_varible.error_elemment_command_dyn[0]

                    elif error_lattice[i - 2][0] == global_varible.error_elemment_command_stat[1]:
                        error_lattice[i - 2][0] = global_varible.error_elemment_command_dyn[1]

                    # print(error_lattice)


                elif error_lattice[i - 1][0] in global_varible.error_elemment_command:
                    if error_lattice[i - 1][0] == global_varible.error_elemment_command_stat[0]:
                        error_lattice[i - 1][0] = global_varible.error_elemment_command_dyn[0]

                    elif error_lattice[i - 1][0] == global_varible.error_elemment_command_stat[1]:
                        error_lattice[i - 1][0] = global_varible.error_elemment_command_dyn[1]
            #把所有的开关关掉
            elif error_lattice[i][0] in global_varible.error_elemment_dyn_on or \
                    error_lattice[i][0] in global_varible.error_elemment_stat_on or \
                    error_lattice[i][0] in global_varible.error_beam_dyn_on or \
                    error_lattice[i][0] in global_varible.error_beam_stat_on:

                error_lattice[i].insert(0, False)

            elif error_lattice[i][0] == 'err_beam_stat':
                tmp_err_beam_stat = copy.deepcopy(error_lattice[i])
                error_lattice[i].insert(0, False)

            elif error_lattice[i][0] == 'err_beam_dyn':
                tmp_err_beam_dyn = copy.deepcopy(error_lattice[i])
                error_lattice[i].insert(0, False)

        # 插入元件开关命令
        if len(self.err_cav_stat_on) != 0 or len(self.err_cav_dyn_on) != 0:
            error_lattice.insert(2, new_err_cav_dyn_on)

        if len(self.err_quad_stat_on) != 0 or len(self.err_quad_dyn_on) != 0:
            error_lattice.insert(2, new_err_quad_dyn_on)

        # 插入beam动态误差
        if len(tmp_err_beam_stat) != 0 and len(tmp_err_beam_dyn) != 0:
            tmp_v = [float(tmp_err_beam_stat[i]) + float(tmp_err_beam_dyn[i]) for i in range(1, len(tmp_err_beam_stat))]
            new_err_beam_dyn = new_err_beam_dyn + tmp_v
        elif len(tmp_err_beam_dyn) != 0:
            tmp_v = [float(tmp_err_beam_dyn[i]) for i in range(1, len(tmp_err_beam_dyn))]
            new_err_beam_dyn = new_err_beam_dyn + tmp_v

        elif len(tmp_err_beam_stat) != 0:
            tmp_v = [float(tmp_err_beam_stat[i]) for i in range(1, len(tmp_err_beam_stat))]
            new_err_beam_dyn = new_err_beam_dyn + tmp_v

        if len(new_err_beam_dyn) != 1:
            error_lattice.insert(2, new_err_beam_dyn)

        # 插入beam误差开关：
        if len(new_err_beam_dyn) != 1:
            error_lattice.insert(2, new_err_beam_dyn_on)

        # 去掉编号后缀
        error_lattice = self.delete_element_end_index(error_lattice)
        error_lattice = [i for i in error_lattice if i[0] is not False]

#############################



        
        
        with open(self.lattice_path, 'w') as f:
            for i in error_lattice:
                f.write(' '.join(map(str, i)) + '\n')

        try:
            process = multiprocessing.Process(target=self.run_avas,
                                              args=(self.project_path, 'outputfile\error_middle'))

            process.start()  # 启动子进程
            process.join()  # 等待子进程运行结束

        except Exception as e:
            # 处理异常，如果需要
            print(f"An error occurred: {str(e)}")

        finally:
            # 无论是否发生异常都会执行这里的代码
            if process.is_alive():
                process.terminate()  # 终止子进程




        new_name = f'output_{group}_{time}'

        copy_directory(self.error_middle_output0_path, self.error_output_path , new_name)

        delete_directory(self.error_middle_output0_path)
        
###############################################################


    def run_err_stat_dyn_all_group(self, opti):
        """
        跑静态误差与动态误差， 应该分成两种情况，
        1. 需要优化
        2. 不需要优选
        :return:
        """
        self.stat_dyn = 1

        #第一种情况，需要优化
        if opti:
            self.optimize_all_group()
            
            correct_initial_value_path = os.path.join(self.output_path, 'stat_error_correct_res.txt')
            opti_res = read_txt(correct_initial_value_path, out='list')

            if os.path.exists(self.error_output_path):
                delete_directory(self.error_output_path)
            os.makedirs(self.error_output_path)

            self.get_group_time()
            self.generate_lattice_mulp_list()
            adjust_parameter_lattice_command, adjust_element_num, adjust_parameter_initial_value, adjust_parameter_num, adjust_parameter_range, \
            adjust_parameter_n, adjust_parameter_use_init = self.generate_adjust_parameter()

            stat_dyn_err_lattice_path = os.path.join(self.project_path, 'OutputFile', 'stat_dyn_err_lattice.txt')
            with open(stat_dyn_err_lattice_path, 'w') as f:
                for i in self.stat_dyn_err_lattice:
                    for j in i:
                        f.write(' '.join(map(str, j)) + '\n')
                    f.write('--------------------------------' + '\n')
                    f.write('--------------------------------' + '\n')
            
            # print(stat_dyn_err_lattice_path)

            for i in range(self.all_group):
                for j in range(self.all_time):
                    x = opti_res[i*self.all_time + j]
                    error_lattice = self.stat_dyn_err_lattice[i * self.all_time + j]

                    # 得到lattice的定位信息

                    self.run_err_stat_dyn_one_time(x, i, j, error_lattice,
                                                   adjust_element_num, adjust_parameter_num, True)
            
            

        # 第二种情况，不需要优化
        else:
            self.get_group_time()
            self.generate_lattice_mulp_list()
    
            for i in range(self.all_group):
                for j in range(self.all_time):
                    error_lattice = self.generate_error_lattice(i, j)

                    self.run_err_stat_dyn_one_time([], i, j, error_lattice, [], [], False)


    #没有误差只进行匹配
    def only_adjust(self):
        self.only_adjust_sign = 1

        lattice_mulp_path = os.path.join(self.project_path, 'InputFile', 'lattice_mulp.txt')
        input_lines = read_txt(lattice_mulp_path, out='list')
        index = 0
        for i in input_lines:
            if i[0] in global_varible.long_element:
                add_name = f'element_{index}'
                i.append(add_name)
                index += 1
        # for i in input_lines:
        #     print(i)

        self.lattice_mulp_list = copy.deepcopy(input_lines)


        adjust_parameter_lattice_command, adjust_element_num, adjust_parameter_initial_value, adjust_parameter_num, adjust_parameter_range, \
        adjust_parameter_n, adjust_parameter_use_init = self.generate_adjust_parameter()
        # print( adjust_element_num, adjust_parameter_initial_value, adjust_parameter_num, adjust_parameter_range, \
        # adjust_parameter_n, adjust_parameter_use_init)

        ini, loss = self.optimize_one_group(0, 0, self.lattice_mulp_list,
                                             adjust_element_num, adjust_parameter_initial_value, adjust_parameter_num, adjust_parameter_range, \
                                            adjust_parameter_n, adjust_parameter_use_init)
        corrected_result = ini


        #将结果保存到output文件中
        correct_initial_value_path = os.path.join(self.output_path, 'correct_res.txt')


        self.ini.append(ini)
        self.loss.append(loss)

        print(self.ini)


        with open(correct_initial_value_path, 'w') as f:
            for i in self.ini:
                f.write(' '.join(map(str, i)) + '\n')


        self.run_use_corrected_result(corrected_result, 0, 0, self.lattice_mulp_list ,
                                  adjust_element_num, adjust_parameter_num)



if __name__ == "__main__":
    # obj = ErrorStat(r'C:\Users\anxin\Desktop\test_control\test_error')
    # obj.read_lattice_parameter()
    # obj.generate_error_lattice(1)
    # obj.generate_adjust_parameter()
    # # obj.optimize_one_group(1)
    # obj.treat_diag()


    start = time.time()
    print("start", start)
    obj = ErrorAnalysis(r'C:\Users\anxin\Desktop\test_err_dyn')
    # obj.run_err_stat_dyn_all_group(False)
    # obj.optimize_all_group()
    obj.run_err_dyn_all_group()



