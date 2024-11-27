
# 工作流程：
#    generate_adjust_parameter：根据lattice_mulp记录需要adjust的元件及参数位置，这里的位置是整个
#    lattice_mulp中所有的内容转换成list

#    get_goal：修改参数，添加end，然后写入lattice
#    根据诊断命令，计算loss
import sys
sys.path.append(r'C:\Users\anxin\Desktop\AVAS_control')
from scipy.optimize import minimize

import numpy as np

from dataprovision.latticeparameter import LatticeParameter
from dataprovision.datasetparameter import DatasetParameter

from utils.readfile import read_txt
from utils.treatlist import flatten_list, list_one_two
from utils.treatfile import copy_file, split_file
from utils.tool import write_to_txt, calculate_mean, calculate_rms, add_to_txt

import os


import random
from core.MultiParticle import MultiParticle
from utils.treat_directory import list_files_in_directory, copy_directory, delete_directory
import multiprocessing

import global_varible
import copy

from utils.tolattice import write_mulp_to_lattice_only_sim
from aftertreat.dataanalysis.plttodensity import PlttoDensity, MergeDensityData
class Error():
    """
    该类为误差分析
    """
    def __init__(self, project_path, seed=50, if_normal=0):
        random.seed(seed)
        self.project_path = project_path
        self.if_normal = if_normal
        self.lattice_mulp_path = os.path.join(self.project_path, 'InputFile', 'lattice_mulp.txt')
        self.lattice_path = os.path.join(self.project_path, 'InputFile', 'lattice.txt')

        self.input_path = os.path.join(self.project_path, 'InputFile')
        self.output_path = os.path.join(self.project_path, 'OutputFile')

        self.error_middle_path = os.path.join(self.project_path, 'OutputFile', 'error_middle')
        self.error_middle_output0_path = os.path.join(self.project_path, 'OutputFile', 'error_middle', 'output_0')
        self.error_output_path = os.path.join(self.project_path, 'OutputFile', 'error_output')
        self.normal_out_path = os.path.join(self.error_output_path, 'output_0_0')

        self.errors_par_tot_path = os.path.join(self.output_path, "errors_par_tot.txt")
        self.errors_par_path = os.path.join(self.output_path, "errors_par.txt")

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
        self.errors_par_tot_list_first = []
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


        self.decimal = 5  # 小数点保留多少位

        self.result_queue = multiprocessing.Queue()
        if os.path.exists(self.error_middle_path):
            delete_directory(self.error_middle_path)
        os.makedirs(self.error_middle_path)

        # midlle_output_0_path = os.path.join(self.error_middle_path, 'output_0')
        # os.makedirs(midlle_output_0_path)

        if os.path.exists(self.error_output_path):
            delete_directory(self.error_output_path)
        os.makedirs(self.error_output_path)

        v = LatticeParameter(self.lattice_mulp_path)
        v.get_parameter()
        self.lattice_total_length = v.total_length

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
            if input_lines[i][0] in global_varible.error_elemment_command and N == -1 and input_lines[i][-1] is False:
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
                    if command[0] in (
                            global_varible.error_elemment_command_quad + global_varible.error_elemment_command_quad_cpl):
                        res[i].append(command)

                # 在叠加场添加高频腔原件误差
                if input_lines[i][0] == 'field' and input_lines[i][4] == '1':
                    if command[0] in (global_varible.error_elemment_command_cav + global_varible.error_elemment_command_cav_cpl):
                        res[i].append(command)

                N -= 1

    def get_dimension(self, lst):
        if not isinstance(lst, list):
            return 0  # 不是列表，维度为 0
        else:
            return 1 + max(self.get_dimension(item) for item in lst)

    def judge_command_on_element(self, lattice, command):
        #返回一个命令对应的是哪个元件
        lattice = copy.deepcopy(lattice)

        command_index = lattice.index(command)
        command_on_element = None
        for i in range(command_index, len(lattice)):
            if lattice[i][0] in global_varible.long_element:
                command_on_element = int(lattice[i][-1].split("_")[1])
                break
        return command_on_element

    def set_error_to_lattice(self, lattice):
        # for i in lattice:
        #     print(i)
        lattice = copy.deepcopy(lattice)

        index = 0
        #为元件增加编号
        for i in lattice:
            if i[0] in global_varible.long_element:
                add_name = f'element_{index}'
                i.append(add_name)
                index += 1


        #为每个误差命令添加一个编号
        err_command = []
        index = 0
        for i in lattice:
            if i[0] in global_varible.error_elemment_command:
                i.append(f"err_{index}")
                index += 1
                err_command.append(i)

        # for i in err_command:
        #     print(i)
        # breakpoint()
        #每一个误差命令的作用范围
        err_command_action_scope = []
        for i in err_command:
            #误差命令的索引
            err_index = lattice.index(i)
            #作用元件数量
            N = int(lattice[err_index][1])
            #判断误差命令在哪个元件上
            command_on_element = self.judge_command_on_element(lattice, i)
            if command_on_element is not None:
                err_command_action_scope.append(list(range(command_on_element, command_on_element + N)))
            else:
                err_command_action_scope.append([])
        # for i in err_command:
        #     print(i)

        #根据命令和作用域向lattice插入
        for i in range(len(err_command)):
            if err_command[i][0] in ['err_quad_ncpl_stat', 'err_quad_cpl_stat',
                                      'err_quad_ncpl_dyn', 'err_quad_cpl_dyn', ]:

                for j in lattice:
                    if j[0] == 'field' and j[4] == '3':
                        if int(j[-1].split("_")[-1]) in err_command_action_scope[i]:
                            j.insert(-1, err_command[i])


            elif err_command[i][0] in ['err_cav_ncpl_stat', 'err_cav_cpl_stat',
                                      'err_cav_ncpl_dyn', 'err_cav_cpl_dyn', ]:

                for j in lattice:
                    if j[0] == 'field' and j[4] == '1':
                        if int(j[-1].split("_")[-1]) in err_command_action_scope[i]:
                            j.insert(-1, err_command[i])

        lattice = self.delete_element_end_index(lattice)
        # for i in lattice:
        #     print(i)
        return lattice


    def generate_lattice_mulp_list(self, group):

        input_lines = read_txt(self.lattice_mulp_path, out='list')

        #为cpl生成误差，如果是cpl，直接生成对应的误差
        input_lines_copy = self.generate_error(input_lines, group, 'cpl')

        #将误差命令添加到每个元件上，加到每个元件的结尾
        lattice = self.set_error_to_lattice(input_lines_copy)
        # for i in lattice:
        #     print(i)
        # breakpoint()


        #去掉误差命令
        lattice = [i for i in lattice if i[0] not in global_varible.error_elemment_command]

        res_treat = []

        error_commands_map = {
            'err_quad_stat': ['err_quad_ncpl_stat', 'err_quad_cpl_stat'],
            'err_quad_dyn': ['err_quad_ncpl_dyn', 'err_quad_cpl_dyn'],
            'err_cav_stat': ['err_cav_ncpl_stat', 'err_cav_cpl_stat'],
            'err_cav_dyn': ['err_cav_ncpl_dyn', 'err_cav_cpl_dyn']
        }

        for i in lattice:
            if self.get_dimension(i) == 1:
                res_treat.append(i)

            elif self.get_dimension(i) != 1:
                lis = []
                err_command_exist = []

                i_copy = copy.deepcopy(i)

                for j in i[::-1]:
                    if isinstance(j, list) and j[0] not in err_command_exist:
                        lis.append(j)

                        if j[0] in error_commands_map["err_quad_stat"]:
                            err_command_exist.extend(error_commands_map["err_quad_stat"])

                        elif j[0] in error_commands_map["err_quad_dyn"]:
                            err_command_exist.extend(error_commands_map["err_quad_dyn"])

                        elif j[0] in error_commands_map["err_cav_stat"]:
                            err_command_exist.extend(error_commands_map["err_cav_stat"])

                        elif j[0] in error_commands_map["err_cav_dyn"]:
                            err_command_exist.extend(error_commands_map["err_cav_dyn"])

                        # if j[0] in ['err_quad_ncpl_stat', 'err_quad_cpl_stat']:
                        #     err_command_exist.append('err_quad_ncpl_stat')
                        #     err_command_exist.append('err_quad_cpl_stat')
                        #
                        # elif j[0] in ['err_cav_ncpl_stat', 'err_cav_cpl_stat']:
                        #     err_command_exist.append('err_cav_ncpl_stat')
                        #     err_command_exist.append('err_cav_cpl_stat')
                        #
                        # elif j[0] in ['err_quad_ncpl_dyn', 'err_quad_cpl_dyn']:
                        #     err_command_exist.append('err_quad_ncpl_dyn')
                        #     err_command_exist.append('err_quad_cpl_dyn')
                        #
                        # elif j[0] in ['err_cav_ncpl_dyn', 'err_cav_cpl_dyn']:
                        #     err_command_exist.append('err_cav_ncpl_dyn')
                        #     err_command_exist.append('err_cav_cpl_dyn')

                        # err_command_exist.append(j[0])
                        i_copy.pop()
                    # 如果已经出现过
                    elif isinstance(j, list) and j[0] in err_command_exist:
                        i_copy.pop()

                    else:
                        lis.append(i_copy)
                        break

                for k in lis:
                    k1 = copy.deepcopy(k)
                    res_treat.append(k1)

        for i in res_treat:
            if i[0] in global_varible.error_elemment_command:
                i.pop()


        #对ncpl误差进行生成
        res_treat = self.generate_error(res_treat, group, 'ncpl')

        for i in res_treat:
            if i[0] == "err_cav_cpl_dyn":
                i[0] = "err_cav_ncpl_dyn"

            elif i[0] == "err_cav_cpl_stat":
                i[0] = "err_cav_ncpl_stat"

            elif i[0] == "err_quad_cpl_dyn":
                i[0] = "err_quad_ncpl_dyn"

            elif i[0] == "err_quad_cpl_stat":
                i[0] = "err_quad_ncpl_stat"

        for i in res_treat:
            if i[0] in global_varible.error_elemment_command:
                i[1] = 1

        # for i in res_treat:
        #     print(i)
        index = 0
        for i in res_treat:
            if i[0] in global_varible.long_element:
                add_name = f'element_{index}'
                i.append(add_name)
                index += 1

        self.lattice_mulp_list = res_treat

        # for i in self.lattice_mulp_list:
        #     print(i)
        # sys.exit()
        #返回值后面带了一个元件索引
        return self.lattice_mulp_list

        # for i in self.lattice_mulp_list:
        #     print(i)
        #
        # sys.exit(0)

    def generate_error_base(self, input, group):
        """
        根据每一个error命令产生对应的error
        :param input:
        :param group:
        :return:
        """
        input = copy.deepcopy(input)


        target = None
        if input[0] in global_varible.error_elemment_command:
            for i in range(3, len(input)):
                input[i] = float(input[i])

            input = input + [0] * (10 - len(input))
            target = input

            if int(input[2]) == 0:
                target = input

            elif int(input[2]) == 1:
                for i in range(3, len(input) - 1):
                    dx = float(input[i]) / self.all_group
                    target[i] = round(random.uniform(-1 * dx * (group), dx * (group)), self.decimal)
                target[2] = 0

            elif int(input[2]) == 2:
                for i in range(3, len(input) - 1):
                    dx = float(input[i]) / self.all_group
                    target[i] = round(random.gauss(0, dx * (group)), self.decimal)
                target[2] = 0

            elif int(input[2]) == -1:
                for i in range(3, len(input) - 1):
                    dx = float(input[i]) / self.all_group
                    target[i] = dx * (group)
                target[2] = 0

        if input[0] in self.error_beam_command:
            for i in range(2, len(input)):
                input[i] = float(input[i])
            input = input + [0] * (27 - len(input))

            target = input

            if int(input[1]) == 0:
                target = input

            elif int(input[1]) == 1:
                for i in range(2, len(input)):
                    dx = float(input[i]) / self.all_group
                    target[i] = round(random.uniform(-1 * dx * group, dx * group), self.decimal)
                target[1] = 0


            elif int(input[1]) == 2:
                for i in range(2, len(input)):
                    dx = float(input[i]) / self.all_group
                    target[i] = round(random.gauss(0, dx * group), self.decimal)
                target[1] = 0

            elif int(input[1]) == -1:
                for i in range(2, len(input)):
                    dx = float(input[i]) / self.all_group
                    target[i] = dx * (group + 1)
                target[1] = 0

        if input[0] == 'err_quad_ncpl_stat' or 'err_quad_cpl_stat':
            for i in range(len(self.err_quad_stat_on)):
                if int(self.err_quad_stat_on[i]) == 0:
                    target[i + 3] = 0

        elif input[0] == 'err_quad_ncpl_dyn' or 'err_quad_cpl_dyn':
            for i in range(len(self.err_quad_dyn_on)):
                if int(self.err_quad_dyn_on[i]) == 0:
                    target[i + 3] = 0

        elif input[0] == 'err_cav_ncpl_stat' or 'err_cav_cpl_stat':
            for i in range(len(self.err_cav_stat_on)):
                if int(self.err_cav_stat_on[i]) == 0:
                    target[i + 3] = 0

        elif input[0] == 'err_cav_ncpl_dyn' or 'err_cav_cpl_dyn':
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

    def generate_error(self, input_lines, group, kind):
        """
        将lattice_mulp写进新的lattice，将误差变成AVAS后端需要的情况
        :param group:
        :return:
        """

        input_lines = copy.deepcopy(input_lines)

        if kind == 'ncpl':
            for i in range(len(input_lines)):
                if len(input_lines[i]) == 0:
                    continue

                elif input_lines[i][0] == 'err_step':
                    input_lines[i] = ['err_step', '1', '1']


                elif input_lines[i][0] in self.error_elemment_command or \
                        input_lines[i][0] in self.error_beam_command:

                    input_lines[i] = self.generate_error_base(input_lines[i], group)

        elif kind == 'cpl':
            for i in range(len(input_lines)):
                if len(input_lines[i]) == 0:
                    continue

                elif input_lines[i][0] in global_varible.error_elemment_command_stat_cpl or \
                        input_lines[i][0] in global_varible.error_elemment_command_dyn_cpl:
                    input_lines[i] = self.generate_error_base(input_lines[i], group)

        return input_lines


    def run_multiparticle(self, p_path, out_putfile_):
        multiparticle_obj = MultiParticle(p_path)
        res = multiparticle_obj.run(output_file=out_putfile_)


    def run_normal(self):
        os.makedirs(self.normal_out_path)
        #模拟没有误差的情况
        write_mulp_to_lattice_only_sim(self.lattice_mulp_path, self.lattice_path)

        ouput = os.path.normpath(os.path.join(self.project_path, 'OutputFile/error_middle/output_0'))
        os.mkdir(ouput)

        process = multiprocessing.Process(target=self.run_multiparticle,
                                          args=(self.project_path, 'OutputFile/error_middle/output_0'))

        process.start()  # 启动子进程
        process.join()  # 等待子进程运行结束

        self.write_density_every_time(0, 0)

        copy_file(self.lattice_path, self.normal_out_path)

        new_name = f'output_0_0'


        copy_directory(self.error_middle_output0_path, self.error_output_path, new_name)

        delete_directory(self.error_middle_output0_path)

    # def get_normal_data(self):
    #     path = os.path.join(self.error_output_path, "output_-1_-1")
    #     dataset_path = os.path.join(path, "DataSet.txt")
    #     print(dataset_path)
    #     dataset_obj = DatasetParameter(dataset_path, self.project_path)
    #     dataset_obj.get_parameter()
    #
    #     normal_data = [0,
    #                    dataset_obj.num_of_particle,  # 总粒子数
    #                    dataset_obj.emit_x[0],  # m, rad
    #                    dataset_obj.emit_y[0],  # m, rad
    #                    dataset_obj.emit_z[0],  # m, rad
    #                    dataset_obj.x[-1],  # m
    #                    dataset_obj.y[-1],  # m
    #                    dataset_obj.x_1[-1],
    #                    dataset_obj.y_1[-1],
    #                    dataset_obj.rms_x[-1],
    #                    dataset_obj.rms_y[-1],
    #                    dataset_obj.rms_x1[-1],
    #                    dataset_obj.rms_y1[-1],
    #                    dataset_obj.ek[-1],  # MeV
    #                    dataset_obj.phi[-1],  # deg
    #
    #                    ]
    #     self.normal_data = normal_data
    #     return normal_data


    def write_err_par_tot_title(self):
        errors_par_tot_title = [[
        "step_err",     #组 0
        "ratio_loss", #束流损失率，1- 存在粒子/总粒子 or 损失粒子 / 总粒子
        "emit_x_increase", #,x, y z方向发射度增长， x/x0 - 1
        "emit_y_increase",
        "emit_z_increase",

        "x_center(m)", #中心位置 5
        "y_center(m)",
        "x_'(rad)",
        "y_'(rad)",

        "rms_x(m)",
        "rms_y(m)",
        "rms_x'(rad)",   #11
        "rms_y'(rad)",   #12

        "delat_energy(MeV)", #能量变化  13

        ]]
        write_to_txt(self.errors_par_tot_path, errors_par_tot_title)


    def write_err_par_title(self):
        # errors_par_title = [
        #     [
        #         "step_err",  # 组 0
        #         "ave(ratio_loss)",  # 束流损失率，1- 存在粒子/总粒子 or 损失粒子 / 总粒子
        #         "ave(emit_x_increase)",  # ,x, y z方向发射度增长， x/x0 - 1
        #         "ave(emit_y_increase)",
        #         "ave(emit_z_increase)",
        #         "rms(x_center(m))",  # 中心位置 5
        #         "rms(y_center(m))",#6
        #         "rms(x_'(rad))",  #7
        #         "rms(y_'(rad))",  #8
        #         "ave(rms_x(m))",  #9
        #         "ave(rms_y(m))", #10
        #         "ave(rms_x'(rad))",  # 11
        #         "ave(rms_y'(rad))",  # 12
        #
        #         "ave(delat_energy)",  # 能量变化  13
        #
        #         "ave(x_center(m))",  # 中心位置 14
        #         "ave(y_center(m))",
        #         "ave(x_'(rad))",
        #         "ave(y_'(rad))",
        #
        #         "rms(delat_energy(MeV))",  # 能量变化  18
        #
        #         "rms(rms_x(m))",  #19
        #         "rms(rms_y(m))",  # 20
        #         "rms(rms_x'(rad))",  # 21
        #         "rms(rms_y'(rad))",  # 22
        #     ]
        # ]
        errors_par_title = [
            [
                "step_err",  # 组 0
                "ave(ratio_loss)",  # 束流损失率，1- 存在粒子/总粒子 or 损失粒子 / 总粒子
                "ave(emit_x_increase)",  # ,x, y z方向发射度增长， x/x0 - 1
                "ave(emit_y_increase)",
                "ave(emit_z_increase)",

                "ave(x_center(m))",  # 中心位置 5
                "ave(y_center(m))",
                "ave(x_'(rad))",
                "ave(y_'(rad))",

                "ave(rms_x(m))",  # 9
                "ave(rms_y(m))",  # 10
                "ave(rms_x'(rad))",  # 11
                "ave(rms_y'(rad))",  # 12

                "ave(delat_energy)",  # 能量变化  13

                "rms(x_center(m))",  # 中心位置 14
                "rms(y_center(m))",#15
                "rms(x_'(rad))",  #16
                "rms(y_'(rad))",  #17


                "rms(rms_x(m))",  #18
                "rms(rms_y(m))",  # 19
                "rms(rms_x'(rad))",  # 20
                "rms(rms_y'(rad))",  # 21

                "rms(delat_energy(MeV))",  # 能量变化  22

            ]
        ]
        write_to_txt(self.errors_par_path, errors_par_title)

    def write_err_par_every_time(self, group, time):
        #误差模拟完毕后对文件进行后处理
        #1.解析dataset文件


        if time == 0:
            output = self.normal_out_path
        else:
            output = os.path.join(self.error_output_path, f"output_{group}_{time}")


        #解析正常的情况
        if self.if_normal == 1:
            dataset_path = os.path.join(self.normal_out_path, "DataSet.txt")

            dataset_obj = DatasetParameter(dataset_path, self.project_path)
            dataset_obj.get_parameter()

            normal_ek = dataset_obj.ek[-1]
        if self.if_normal == 0:
            normal_ek = 0


        dataset_path = os.path.join(output, "DataSet.txt")
        dataset_obj = DatasetParameter(dataset_path, self.project_path)

        v1 = dataset_obj.get_parameter()
        if v1 is False:
            errors_par_tot_list = [f"{group}_{time}"] + [1] + [0]*12
        elif dataset_obj.z[-1] < (self.lattice_total_length-0.01):
            errors_par_tot_list = [f"{group}_{time}"] + [1] + [0]*12
        else:
            errors_par_tot_list = [
            f"{group}_{time}",
            dataset_obj.loss[-1] / dataset_obj.num_of_particle,
            dataset_obj.emit_x[-1]/dataset_obj.emit_x[0] - 1,
            dataset_obj.emit_y[-1]/dataset_obj.emit_y[0] - 1,
            dataset_obj.emit_z[-1]/dataset_obj.emit_z[0] - 1,
            dataset_obj.x[-1],  # m
            dataset_obj.y[-1],  # m
            dataset_obj.x_1[-1],
            dataset_obj.y_1[-1],
            dataset_obj.rms_x[-1],
            dataset_obj.rms_y[-1],
            dataset_obj.rms_x1[-1],
            dataset_obj.rms_y1[-1],
            dataset_obj.ek[-1] - normal_ek,  # MeV
            # dataset_obj.phi[-1] - normal_data[14],  # deg
            ]


        #写入到errors_par_tot
        for i in range(1, len(errors_par_tot_list)):
            errors_par_tot_list[i] = "{:.5e}".format(errors_par_tot_list[i])
        add_to_txt(self.errors_par_tot_path, [errors_par_tot_list])

        #写入到errors_par
        if time == 0:
            t1_lis = errors_par_tot_list + [0] * 9
            t1_lis[0] = 0

            add_to_txt(self.errors_par_path, [t1_lis])

        elif time == self.all_time:
            errors_par_tot_list = read_txt(self.errors_par_tot_path, out = "list")

            t_lis = [j for j in errors_par_tot_list[1:] if int(j[0].split("_")[0]) == group]

            t1_lis = [0] * 23
            if len(t_lis) == 1:
                t1_lis = t_lis[0] + [0] * 9
                t1_lis[0] = group
                t1_lis = [float(i) for i in t1_lis]




            elif len(t_lis) > 1:
                t1_lis[0] = group
                t1_lis[1] = calculate_mean([float(j[1]) for j in t_lis])
                t1_lis[2] = calculate_mean([float(j[2]) for j in t_lis])
                t1_lis[3] = calculate_mean([float(j[3]) for j in t_lis])
                t1_lis[4] = calculate_mean([float(j[4]) for j in t_lis])

                t1_lis[5] = calculate_mean([float(j[5]) for j in t_lis])
                t1_lis[6] = calculate_mean([float(j[6]) for j in t_lis])
                t1_lis[7] = calculate_mean([float(j[7]) for j in t_lis])
                t1_lis[8] = calculate_mean([float(j[8]) for j in t_lis])

                t1_lis[9] = calculate_mean([float(j[9]) for j in t_lis])
                t1_lis[10] = calculate_mean([float(j[10]) for j in t_lis])
                t1_lis[11] = calculate_mean([float(j[11]) for j in t_lis])
                t1_lis[12] = calculate_mean([float(j[12]) for j in t_lis])

                t1_lis[13] = calculate_mean([float(j[13]) for j in t_lis])

                t1_lis[14] = calculate_rms([float(j[5]) for j in t_lis])
                t1_lis[15] = calculate_rms([float(j[6]) for j in t_lis])
                t1_lis[16] = calculate_rms([float(j[7]) for j in t_lis])
                t1_lis[17] = calculate_rms([float(j[8]) for j in t_lis])

                t1_lis[18] = calculate_rms([float(j[9]) for j in t_lis])
                t1_lis[19] = calculate_rms([float(j[10]) for j in t_lis])
                t1_lis[20] = calculate_rms([float(j[11]) for j in t_lis])
                t1_lis[21] = calculate_rms([float(j[12]) for j in t_lis])

                t1_lis[22] = calculate_rms([float(j[13]) for j in t_lis])


            for i in range(1, len(t1_lis)):
                t1_lis[i] = "{:.5e}".format(t1_lis[i])
            add_to_txt(self.errors_par_path, [t1_lis])


    def write_density_every_time(self, group, time):
        return 0
        is_normal = 0
        if group == 0:
            is_normal = 1

        beamset_path = os.path.join(self.error_middle_output0_path, "BeamSet.plt")

        dataset_path = os.path.join(self.error_middle_output0_path, "DataSet.txt")
        target_density_path = os.path.join(self.output_path,  f"density_par_{group}_{time}.dat")
        # print(dataset_path)
        # sys.exit()
        if is_normal == 1:
            # print(802)
            # print(dataset_path)
            # print(target_density_path)
            density_obj = PlttoDensity(beamset_path,  dataset_path, target_density_path)
            density_obj.generate_density_file_onestep(is_normal)

        elif is_normal == 0:
            #如果不是正常模拟
            normal_density_path = os.path.join(self.output_path,  f"density_par_{0}_{0}.dat")
            density_obj = PlttoDensity(beamset_path, dataset_path, target_density_path, normal_density_path, self.project_path)
            density_obj.generate_density_file_onestep(is_normal)

        os.remove(beamset_path)

        if time == self.all_time:
            #到了某一组的最后一次模拟
            all_file = list_files_in_directory(self.output_path)

            filtered_files = [path for path in all_file if f'density_par_{group}' in path]
            target_density_path = os.path.join(self.output_path, f"density_tot_par_{group}.dat")

            merge_obj = MergeDensityData(filtered_files, target_density_path)
            merge_obj.generate_density_file()

        if group == self.all_group and time == self.all_time:
            #到了所有组的最后一次模拟
            all_file = list_files_in_directory(self.output_path)

            filtered_files = [path for path in all_file if f'density_tot_par' in path]
            target_density_path = os.path.join(self.output_path, f"density_tot_par.dat")

            merge_obj = MergeDensityData(filtered_files, target_density_path)
            merge_obj.generate_density_file()

    def write_err_datas(self, group, time):

        err_datas_path = os.path.join(self.output_path, f"Error_Datas_{group}_{time}.txt")
        lattice_path = self.lattice_path
        input = read_txt(lattice_path, out="list")
        # print(input)
        # 为每个元件加编号
        index = 0
        for i in input:
            if i[0] in global_varible.long_element:
                add_name = f'element_{index}'
                i.append(add_name)
                index += 1

        res = []
        for i in range(len(input)):
            if input[i][0] == global_varible.error_elemment_command_dyn[1]:
                #quad
                index = input[i+1][-1].split('_')[-1]
                err_name = f"CAV_ERROR[{index}]"
                t_lis = [err_name] + input[i][3:]
                res.append(t_lis)
            elif input[i][0] == global_varible.error_elemment_command_dyn[0]:
                # quad
                index = input[i + 1][-1].split('_')[-1]
                err_name = f"QUAD_ERROR[{index}]"
                t_lis = [err_name] + input[i][3:]
                res.append(t_lis)
        write_to_txt(err_datas_path, res)

class ErrorDyn(Error):
    def __init__(self, project_path, seed, if_normal):
        super().__init__(project_path, seed, if_normal)


    def run_one_time(self, group, time, lattice_mulp_list):
        """
        动态误差
        :param group:
        :param time:
        :return:
        """


        #去掉末尾编号
        error_lattice = self.delete_element_end_index(lattice_mulp_list)


        for i in error_lattice:
            # 静态误差注释掉
            if i[0] in self.error_elemment_stat or i[0] in self.error_beam_stat:
                i[0] = "!" + i[0]

            # 开关 静态误差注释掉
            elif i[0] in global_varible.error_elemment_stat_on or i[0] == 'err_beam_stat_on':
                i[0] = "!" + i[0]

        error_lattice = [i for i in error_lattice if i[0] in global_varible.err_write_command]

        for i in error_lattice:
            print(i)

        sys.exit()
        with open(self.lattice_path, 'w') as f:
            for i in error_lattice:
                if not i[0].startswith("!"):
                    f.write(' '.join(map(str, i)) + '\n')

        #进行模拟
        if os.path.exists(self.error_middle_output0_path):
            delete_directory(self.error_middle_output0_path)
        # os.makedirs(self.error_middle_output0_path)
        process = multiprocessing.Process(target=self.run_multiparticle,
                                          args=(self.project_path, 'OutputFile/error_middle'))

        process.start()  # 启动子进程
        process.join()  # 等待子进程运行结束

        self.write_density_every_time(group, time)

        copy_file(self.lattice_path, self.error_middle_output0_path)

        new_name = f'output_{group}_{time}'


        copy_directory(self.error_middle_output0_path, self.error_output_path, new_name)

        delete_directory(self.error_middle_output0_path)

    def run(self):
        """
        跑动态误差
        return:
        """
        self.write_err_par_title()
        self.write_err_par_tot_title()

        if self.if_normal == 1:
            self.run_normal()
            self.write_err_par_every_time(0,0)

        self.get_group_time()

        for i in range(1, self.all_group + 1):
            for j in range(1, self.all_time + 1):
                print(i, j)
                lattice_mulp_list = self.generate_lattice_mulp_list(i)
                self.run_one_time(i, j, lattice_mulp_list)
                self.write_err_datas(i, j)
                self.write_err_par_every_time(i, j)

class Errorstat(Error):
    def __init__(self, project_path, seed, if_normal):
        super().__init__(project_path, seed, if_normal)
        self.all_error_lattice = []
        # 只优化
        # self.only_adjust_sign = 0
        self.err_type = 'stat'
        self.diag_every = {}



    def generate_adjust_parameter(self, input_lines):
        """
        产生定位信息, adjust命令中哪些参数需要修改
        """
        adjust_parameter_lattice_command = [] #原来的命令
        adjust_element_num = [] #第几个元件要改
        adjust_parameter_num = [] #第几个参数要改
        adjust_parameter_range = []#参数的范围
        adjust_parameter_n = [] #具有一样的值
        adjust_parameter_use_init = []#是否使用初值
        adjust_parameter_initial_value = []




        adjust_parameter_num_per = []
        adjust_parameter_range_per = []
        adjust_parameter_n_per = []
        adjust_parameter_use_init_per = []
        index = -1

        index = 0
        #为adjust命令增加编号
        lattice = copy.deepcopy(input_lines)
        for i in lattice:
            if i[0] == "adjust":
                add_name = f'adjust_{index}'
                i.append(add_name)
                index += 1


        #为每个调整命令增加作用元件数
        for i in lattice:
            if i[0] == "adjust":
                adjust_on_element = self.judge_command_on_element(lattice, i)
                i.append(adjust_on_element)
                if adjust_on_element not in adjust_element_num:
                    adjust_element_num.append(adjust_on_element)

        #[['adjust', '0', '1', '0', '0', '0.3', '0', 'adjust_0', 2]]
        all_adjust_command = []
        for i in lattice:
            if i[0] == "adjust":
                all_adjust_command.append(copy.deepcopy(i))



        adjust_parameter_num = [[] for _ in range(len(adjust_element_num))]
        adjust_parameter_range = [[] for _ in range(len(adjust_element_num))]
        adjust_parameter_n = [[] for _ in range(len(adjust_element_num))]
        adjust_parameter_use_init = [[] for _ in range(len(adjust_element_num))]

        for i in lattice:
            if i[0] == "adjust":
                index = adjust_element_num.index(i[-1])
                adjust_parameter_num[index].append(int(i[2]))
                adjust_parameter_range[index].append([float(i[4]), float(i[5])])
                adjust_parameter_n[index].append(int(i[3]))
                adjust_parameter_use_init[index].append(int(i[6]))


        adjust_parameter_initial_value = [[] for _ in range(len(adjust_element_num))]
        for i in range(len(adjust_element_num)):
            for j in lattice:
                if j[0] in global_varible.long_element and int(j[-1].split("_")[-1]) == adjust_element_num[i]:
                    for k in adjust_parameter_num[i]:
                        adjust_parameter_initial_value[i].append(float(j[k]))

        return adjust_element_num, adjust_parameter_initial_value, adjust_parameter_num, adjust_parameter_range, \
               adjust_parameter_n, adjust_parameter_use_init
        # print(adjust_element_num)
        # print(adjust_parameter_num)
        # print(adjust_parameter_range)
        # print(adjust_parameter_n)
        # print(adjust_parameter_use_init)
        # print(adjust_parameter_initial_value)
        # sys.exit(0)
        #
        # for i in range(len(input_lines)):
        #     if input_lines[i][0] in global_varible.long_element:
        #         index += 1
        #
        #
        #     if input_lines[i][0] == 'adjust':
        #         adjust_parameter_num_per.append(int(input_lines[i][2]))
        #         adjust_parameter_range_per.append([float(input_lines[i][4]), float(input_lines[i][5])])
        #         adjust_parameter_n_per.append(int(input_lines[i][3]))
        #         adjust_parameter_use_init_per.append(int(input_lines[i][6]))
        #
        #         tmp_index = index + 1
        #
        #         if tmp_index not in adjust_element_num:
        #             adjust_element_num.append(tmp_index)
        #     elif input_lines[i][0] != 'adjust' and input_lines[i-1][0] == 'adjust':
        #
        #         adjust_parameter_lattice_command.append(input_lines[i])
        #
        #         adjust_parameter_num.append(copy.deepcopy(adjust_parameter_num_per))
        #
        #         adjust_parameter_initial_value_per = [float(input_lines[i][j]) for j in adjust_parameter_num_per]
        #         adjust_parameter_initial_value.append(adjust_parameter_initial_value_per)
        #
        #         adjust_parameter_num_per.clear()
        #
        #
        #
        #         adjust_parameter_range.append(copy.deepcopy(adjust_parameter_range_per))
        #         adjust_parameter_range_per.clear()
        #
        #         adjust_parameter_n.append(copy.deepcopy(adjust_parameter_n_per))
        #         adjust_parameter_n_per.clear()
        #
        #
        #         adjust_parameter_use_init.append(copy.deepcopy(adjust_parameter_use_init_per))
        #         adjust_parameter_use_init_per.clear()
        #
        # print(1108, adjust_parameter_lattice_command, adjust_element_num, adjust_parameter_initial_value, adjust_parameter_num, adjust_parameter_range, \
        # adjust_parameter_n, adjust_parameter_use_init)
        # sys.exit(0)
        # return adjust_parameter_lattice_command, adjust_element_num, adjust_parameter_initial_value, adjust_parameter_num, adjust_parameter_range, \
        #        adjust_parameter_n, adjust_parameter_use_init

    def treat_diag(self, group, time, error_lattice):

        """
        得到loss
        :return:
        """
        diag_every_location = []
        # 读取新的lattice信息


        input_lines = error_lattice

        # 产生每一个diag针对的位置
        lattice_obj = LatticeParameter(self.lattice_mulp_path)
        lattice_obj.get_parameter()


        lattice_copy = copy.deepcopy(input_lines)
        index = 0
        #为diag添加diag_0
        for i in lattice_copy:
            if i[0].startswith("diag"):
                add_name = f'diag_{index}'
                i.append(add_name)
                index += 1

        index = 0
        for i in lattice_copy:
            if i[0] in global_varible.long_element:
                add_name = f'element_{index}'
                i.append(add_name)
                index += 1

        all_diag_command = []
        for i in lattice_copy:
            if i[0].startswith("diag"):
                all_diag_command.append(i)

        diag_index = []
        diag_command_list = []
        for i in all_diag_command:
            adjust_on_element = self.judge_command_on_element(lattice_copy, i)
            if adjust_on_element is not None:
                diag_index.append(adjust_on_element - 1)
            else:
                diag_index.append(-1)

            diag_command_list.append(i[:5])

        diag = []

        for i in range(len(diag_index)):
            dic = {}
            dic['diag_command'] = diag_command_list[i]
            dic['diag_order'] = i
            dic['position'] = lattice_obj.v_start[diag_index[i]] + lattice_obj.v_len[diag_index[i]]
            diag.append(dic)

        # print(diag_index)
        # print(diag)
        # sys.exit()

        dataset_path = os.path.join(self.error_middle_output0_path, 'dataset.txt')

        dataset_obj = DatasetParameter(dataset_path)
        dataset_obj.get_parameter()

        z_ = dataset_obj.z


        loss_type = []
        loss_list = []

        target_energy_list = []
        target_position_list = []
        target_size_list = []


        for i in diag:
            position = i['position']
            print("position", position)
            index_of_position = 0
            for index, i1 in enumerate(z_):
                if i1 > position:
                    index_of_position = index - 1
                    break



            center_x = dataset_obj.x[index_of_position] * 1000    #mm
            center_y = dataset_obj.y[index_of_position] * 1000    #mm

            rms_x = dataset_obj.rms_x[index_of_position] * 1000   #mm
            rms_y = dataset_obj.rms_y[index_of_position] * 1000   #mm

            energy = dataset_obj.ek[index_of_position]

            v = [position, center_x, center_y, rms_x, rms_y, energy]
            diag_every_location.append(v)
            if i['diag_command'][0] == 'diag_position':

                target_x, target_y = float(i['diag_command'][2]), float(i['diag_command'][3])
                accuracy = float(i['diag_command'][4])
                loss = ((center_x - target_x) ** 2) + ((center_y - target_y) ** 2)

                target_position_list.append(target_x)
                loss_list.append(loss)
                loss_type.append('diag_position')

            if i['diag_command'][0] == 'diag_size':


                target_x, target_y = float(i['diag_command'][2]), float(i['diag_command'][3])

                accuracy = float(i['diag_command'][4])

                print(target_x, rms_x, ((rms_x - target_x) ** 2) )
                print(target_y, rms_y, ((rms_y - target_y) ** 2) )

                target_size_list.append(target_x)
                loss = ((rms_x - target_x) ** 2) + ((rms_y - target_y) ** 2)
                loss_list.append(loss)

                loss_type.append('diag_size')

            if i['diag_command'][0] == 'diag_energy':
                target_energy = float(i['diag_command'][2])

                print('target_energy', target_energy)
                print('res_energy', energy)

                accuracy = float(i['diag_command'][3])

                loss = ((energy - target_energy) ** 2)

                target_energy_list.append(target_energy)
                loss_list.append(loss)
                loss_type.append('diag_energy')



        self.diag_every[f"{group}_{time}"] = diag_every_location

        all_loss = 0
        for i in loss_list:
            all_loss += i

        return all_loss
    def get_goal(self, error_lattice, adjust_element_num, adjust_parameter_num, group, time):
        def goal(x):
            print("--------------------")
            print('x', x)

            self.ini_this.append(x)

            x = list_one_two(list(x), adjust_parameter_num)


            for i in range(len(adjust_element_num)):
                for j in range(len(adjust_parameter_num[i])):
                    for com in error_lattice:
                        if com[-1] == f'element_{adjust_element_num[i]}':
                            com[adjust_parameter_num[i][j]] = x[i][j]
                            break

            error_lattice_no_index = self.delete_element_end_index(error_lattice)



            error_lattice_write = copy.deepcopy(error_lattice_no_index)


            for index, i in enumerate(error_lattice[::-1]):
                index = -1 * index - 1
                if index == -1 and i[0].startswith("diag"):
                    break

                if index == -2 and i[0].startswith("diag"):
                    break

                if i[0].startswith("diag"):
                    error_lattice_write.insert(index + 1, ['end'])
                    break


            for i in error_lattice_write:

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
                elif i[0] in global_varible.error_elemment_dyn_on:
                    i[0] = "!" + i[0]

                elif i[0] == global_varible.error_elemment_stat_on[0]:
                    i[0] = global_varible.error_elemment_dyn_on[0]

                elif i[0] == global_varible.error_elemment_stat_on[1]:
                    i[0] = global_varible.error_elemment_dyn_on[1]

                #     print(4)
                # print(2, i)
            error_lattice_write = [i for i in error_lattice_write if i[0] in global_varible.err_write_command]

            with open(self.lattice_path, 'w') as f:
                for i in error_lattice_write:
                    f.write(' '.join(map(str, i)) + '\n')

            try:
                if os.path.exists(self.error_middle_output0_path):
                    delete_directory(self.error_middle_output0_path)

                # if self.only_adjust_sign == 1:
                if self.err_type == 'only_adjust':
                    os.makedirs(self.error_middle_output0_path)
                    process = multiprocessing.Process(target=self.run_multiparticle,
                                                      args=(self.project_path, 'OutputFile/error_middle/output_0'))
                else:
                    process = multiprocessing.Process(target=self.run_multiparticle,
                                                      args=(self.project_path, 'OutputFile/error_middle'))

                process.start()  # 启动子进程
                process.join()  # 等待子进程运行结束
                process.terminate()  # 终止子进程

                loss = self.treat_diag(group, time, error_lattice_no_index)

            except Exception as e:
                # 处理异常，如果需要
                print(f"An error occurred: {str(e)}")
                loss = 1

            finally:
                if process.is_alive():
                    process.terminate()  # 终止子进程

            delete_directory(self.error_middle_output0_path)

            print(loss)
            self.loss_this.append(loss)
            print("--------------------")

            if loss < 0.05:
                raise Exception('已小于0.05')

            return loss

        return goal

    def optimize_one_group(self, group, time, error_lattice,
                           adjust_element_num, adjust_parameter_initial_value, adjust_parameter_num,
                           adjust_parameter_range, \
                           adjust_parameter_n, adjust_parameter_use_init):

        error_lattice = copy.deepcopy(error_lattice)

        # lattice中原本的初值
        # lattice_initial_value =np.array(adjust_parameter_initial_value).reshape(-1)

        lattice_initial_value = flatten_list(adjust_parameter_initial_value)

        # print('lattice_initial_value', lattice_initial_value)

        # 范围
        parameter_range = np.array(flatten_list(adjust_parameter_range)).reshape(-1, 2)
        # print('parameter_range', parameter_range)

        # 随机初值
        random_initial_value = [random.uniform(i[0], i[1]) for i in parameter_range]

        # 是否使用初值
        # use_initial_value = np.array(adjust_parameter_use_init).reshape(-1)
        use_initial_value = np.hstack(adjust_parameter_use_init)

        # 最终初值
        initial_value = random_initial_value
        for i in range(len(initial_value)):
            if use_initial_value[i] == 1:
                initial_value[i] = lattice_initial_value[i]

        print('initial_value', initial_value)

        # 是否使用相同的值
        # n_ = np.array(adjust_parameter_n).reshape(-1)
        n_ = flatten_list(adjust_parameter_n)
        # print('n_', n_)

        unique_elements, unique_indices = np.unique(n_, return_index=True)
        print(unique_elements, unique_indices)

        indiaces = []

        for i in range(len(unique_elements)):
            if unique_elements[i] != 0:
                indiaces.append([index for index, element in enumerate(n_) if element == unique_elements[i]])


        constraints = []
        for i in indiaces:
            if len(i) == 1:
                continue
            for j in range(1, len(i)):
                # print([i[j]], i[0])
                initial_value[i[j]] = initial_value[i[0]]
                constraints.append({'type': 'eq', 'fun': lambda x: x[i[j]] - x[i[0]]})


        # for constraint in constraints:
        #     print('约束条件函数结果:', constraint)

        goal = self.get_goal(error_lattice, adjust_element_num, adjust_parameter_num, group, time)

        options = {'maxiter': 100, 'eps': 10**-1, 'ftol': 10**-4}

        self.ini_this = []
        self.loss_this = []

        try:
            result = minimize(fun=goal, x0=initial_value, constraints=constraints, bounds=parameter_range,
                              method='SLSQP', options=options)

            return result.x, result.fun

        except Exception:
            return self.ini_this[-1], self.loss_this[-1]

    def run_use_corrected_result(self, corrected_result, group, time, error_lattice,
                                 adjust_element_num, adjust_parameter_num):

        # x =np.array(corrected_result).reshape(np.array(adjust_parameter_num).shape)
        error_lattice = copy.deepcopy(error_lattice)


        if self.opti:
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

        error_lattice = [i for i in error_lattice if i[0] in global_varible.err_write_command]
        with open(self.lattice_path, 'w') as f:
            for i in error_lattice:
                f.write(' '.join(map(str, i)) + '\n')




        if os.path.exists(self.error_middle_output0_path):
            delete_directory(self.error_middle_output0_path)

        # if self.only_adjust_sign == 1:
        if self.err_type == 'only_adjust':
            os.makedirs(self.error_middle_output0_path)

            process = multiprocessing.Process(target=self.run_multiparticle, args=(self.project_path, 'OutputFile/error_middle/output_0'))
        else:
            process = multiprocessing.Process(target=self.run_multiparticle, args=(self.project_path, 'OutputFile/error_middle'))

        process.start()  # 启动子进程
        process.join()  # 等待子进程运行结束

        self.write_density_every_time(group, time)

        copy_file(self.lattice_path, self.error_middle_output0_path)

        new_name = f'output_{group}_{time}'

        copy_directory(self.error_middle_output0_path, self.error_output_path, new_name)

        delete_directory(self.error_middle_output0_path)

    def run_one_time_opti(self, group, time, lattice_mulp_list):
        self.diag_every.clear()
        """
        静态误差完整跑一次, 需要矫正

        :param group:
        :param time:
        :return:
        """

        # 得到lattice的定位信息
        adjust_element_num, adjust_parameter_initial_value, adjust_parameter_num, adjust_parameter_range, \
        adjust_parameter_n, adjust_parameter_use_init = self.generate_adjust_parameter(lattice_mulp_list)

        # print( adjust_element_num, adjust_parameter_initial_value, adjust_parameter_num, adjust_parameter_range, \
        # adjust_parameter_n, adjust_parameter_use_init)
        # sys.exit()
        #进行优化
        opti_res_this, loss_this = self.optimize_one_group(group, time, lattice_mulp_list,
                                            adjust_element_num, adjust_parameter_initial_value, adjust_parameter_num,
                                            adjust_parameter_range, \
                                            adjust_parameter_n, adjust_parameter_use_init)
        #
        self.opti_res.append(opti_res_this)
        self.loss.append(loss_this)
        print("本组优化结束")
        print(self.opti_res)
        #将优化参数写入到文件
        self.write_adjust_datas(group, time, adjust_element_num, adjust_parameter_num, opti_res_this)

        print(self.diag_every)
        self.write_diag_datas(self.diag_every)

        if self.err_type == 'stat':
            #使用优化后的结果运行一次
            self.run_use_corrected_result(opti_res_this, group, time, lattice_mulp_list,
                                          adjust_element_num, adjust_parameter_num)
        elif self.err_type == 'stat_dyn':
            pass
        breakpoint()
    def write_diag_datas(self, diag_every):
        k = list(diag_every.keys())[0]
        v = list(diag_every.values())[0]

        diag_datas_path = os.path.join(self.output_path, f"Diag_Datas_{k}.txt")
        diag_lis = []
        for index, i in enumerate(v):
            v = [round(j, 3) for j in i]

            t_lis = [f"diag_command_{index}" + "\n",
                    f"postion  {v[0]}" + "\n",
                      f"center  {v[1]}  {v[2]}" + "\n",
                      f"rms_size {v[3]} {v[4]}" + "\n",
                      f"energy {v[5]}" + "\n",
            ]
            diag_lis.append(t_lis)
        write_to_txt(diag_datas_path, diag_lis)

    def write_adjust_datas(self, group, time, adjust_element_num, adjust_parameter_num, opti_res_this):
        opti_res_this = [round(i, 3) for i in opti_res_this]
        opti_res_this = list_one_two(list(opti_res_this), adjust_parameter_num)

        adjust_datas_path = os.path.join(self.output_path, f"Adjust_Datas_{group}_{time}.txt")
        #
        res = []
        for i, index in enumerate(adjust_element_num):
            err_name = f"element_adjust[{index}]"
            t_lis = [err_name] + opti_res_this[i]
            res.append(t_lis)

        write_to_txt(adjust_datas_path, res)
    def judge_opti(self):
        "判断是否需要优化"
        res = read_txt(self.lattice_mulp_path, out='list')

        sign = []
        # 判断是否需要矫正
        for i in res:
            if i[0] == 'adjust':
                sign.append('adjust')
            elif i[0].startswith('diag'):
                sign.append('diag')

        # 如果这两个都包含,
        if 'adjust' in sign and 'diag' in sign:
            return 1
        else:
            return 0

    def run(self):
        self.write_err_par_title()
        self.write_err_par_tot_title()
        if self.if_normal == 1:
            self.run_normal()
            self.write_err_par_every_time(0, 0)

        self.get_group_time()
        self.opti = self.judge_opti()

        if self.opti:
            for i in range(1, self.all_group+1):
                for j in range(1, self.all_time + 1):
                    print(i, j)
                    lattice_mulp_list = self.generate_lattice_mulp_list(i)
                    self.all_error_lattice.append(lattice_mulp_list)
                    self.run_one_time_opti(i, j, lattice_mulp_list)
                    self.write_err_datas(i, j)
                    self.write_err_par_every_time(i, j)

        else:
            for i in range(1, self.all_group+1):
                for j in range(1, self.all_time+1):
                    print(i, j)
                    lattice_mulp_list = self.generate_lattice_mulp_list(i)
                    self.run_use_corrected_result(0, i, j, lattice_mulp_list, 0, 0)
                    self.write_err_datas(i, j)
                    self.write_err_par_every_time(i, j)


class Errorstatdyn(Errorstat):
    def __init__(self, project_path, seed, if_normal):
        super().__init__(project_path, seed, if_normal)
        self.err_type = 'stat_dyn'


    def run_stat_dyn_one_time(self, x, group, time, error_lattice,
                                  adjust_element_num, adjust_parameter_num, opti):
        error_lattice = copy.deepcopy(error_lattice)
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
        # 将静态的动态误差的开启结合起来
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
            tmp_v = [float(tmp_err_beam_stat[i]) + float(tmp_err_beam_dyn[i]) for i in
                     range(1, len(tmp_err_beam_stat))]
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

        error_lattice = [i for i in error_lattice if i[0] in global_varible.err_write_command]
        with open(self.lattice_path, 'w') as f:
            for i in error_lattice:
                f.write(' '.join(map(str, i)) + '\n')

        try:
            process = multiprocessing.Process(target=self.run_multiparticle,
                                              args=(self.project_path, 'OutputFile/error_middle'))

            process.start()  # 启动子进程
            process.join()  # 等待子进程运行结束

        except Exception as e:
            # 处理异常，如果需要
            print(f"An error occurred: {str(e)}")

        finally:
            # 无论是否发生异常都会执行这里的代码
            if process.is_alive():
                process.terminate()  # 终止子进程

        copy_file(self.lattice_path, self.error_middle_output0_path)

        self.write_density_every_time(group, time)

        new_name = f'output_{group}_{time}'

        copy_directory(self.error_middle_output0_path, self.error_output_path, new_name)

        delete_directory(self.error_middle_output0_path)
    def run(self):
        """
        跑静态误差与动态误差， 应该分成两种情况，
        1. 需要优化
        2. 不需要优选
        :return:
        """
        self.write_err_par_title()
        self.write_err_par_tot_title()


        self.opti = self.judge_opti()

        # 第一种情况，需要优化
        if self.opti:
            #进行优化

            #动态误差静态误差一起跑
            self.get_group_time()

            for i in range(1, self.all_group+1):
                for j in range(1, self.all_time+1):
                    print(i, j)
                    lattice_mulp_list = self.generate_lattice_mulp_list(i)
                    self.all_error_lattice.append(lattice_mulp_list)
                    self.run_one_time_opti(i, j, lattice_mulp_list)

            #将优化的结果进行保存
            # new_name = f'opti_output'
            # copy_directory(self.error_output_path,  self.output_path, new_name)

            #
            # if os.path.exists(self.error_middle_path):
            #     delete_directory(self.error_middle_path)
            # os.makedirs(self.error_middle_path)
            #
            # if os.path.exists(self.error_output_path):
            #     delete_directory(self.error_output_path)
            # os.makedirs(self.error_output_path)

            if self.if_normal == 1:
                self.run_normal()
                self.write_err_par_every_time(0, 0)

            lattice_mulp_list = self.generate_lattice_mulp_list(0)

            adjust_element_num, adjust_parameter_initial_value, adjust_parameter_num, adjust_parameter_range, \
            adjust_parameter_n, adjust_parameter_use_init = self.generate_adjust_parameter(lattice_mulp_list)


            for i in range(1, self.all_group+1):
                for j in range(1, self.all_time+1):
                    x = self.opti_res[(i-1) * self.all_time + (j-1)]
                    error_lattice_index = self.all_error_lattice[(i-1) * self.all_time + (j-1)]

                    # 得到lattice的定位信息
                    self.run_stat_dyn_one_time(x, i, j, error_lattice_index,
                                                   adjust_element_num, adjust_parameter_num, True)

                    self.write_err_datas(i, j)
                    self.write_err_par_every_time(i, j)

        # 第二种情况，不需要优化
        else:
            if self.if_normal == 1:
                self.run_normal()
                self.write_err_par_every_time(0, 0)

            self.get_group_time()

            for i in range(1, self.all_group+1):
                for j in range(1, self.all_time+1):
                    error_lattice_index = self.generate_lattice_mulp_list(i)
                    self.all_error_lattice.append(error_lattice_index)
                    self.run_stat_dyn_one_time([], i, j, error_lattice_index, [], [], False)
                    self.write_err_datas(i, j)
                    self.write_err_par_every_time(i, j)


class OnlyAdjust(Errorstat):
    def __init__(self, project_path, seed):
        super().__init__(project_path, seed)

    def run(self):
        self.run_normal()

        # self.only_adjust_sign = 1
        self.err_type = 'only_adjust'
        input_lines = read_txt(self.lattice_mulp_path, out='list')
        index = 0
        for i in input_lines:
            if i[0] in global_varible.long_element:
                add_name = f'element_{index}'
                i.append(add_name)
                index += 1


        self.lattice_mulp_list = copy.deepcopy(input_lines)


        # adjust_parameter_lattice_command, adjust_element_num, adjust_parameter_initial_value, adjust_parameter_num, adjust_parameter_range, \
        # adjust_parameter_n, adjust_parameter_use_init = self.generate_adjust_parameter()
        #
        #
        # opti_res, loss = self.optimize_one_group(0, 0, self.lattice_mulp_list,
        #                                      adjust_element_num, adjust_parameter_initial_value, adjust_parameter_num, adjust_parameter_range, \
        #                                     adjust_parameter_n, adjust_parameter_use_init)
        #
        # self.opti = 1
        # self.run_use_corrected_result(opti_res, 0, 0, self.lattice_mulp_list ,
        #                           adjust_element_num, adjust_parameter_num)
        self.opti = 1
        self.run_one_time_opti(0,0)

if __name__ == "__main__":
    # obj = ErrorStat(r'C:\Users\anxin\Desktop\test_control\test_error')
    # obj.read_lattice_parameter()
    # obj.generate_error_lattice(1)
    # obj.generate_adjust_parameter()
    # # obj.optimize_one_group(1)
    # obj.treat_diag()

    # start = time.time()
    # print("start", start)
    obj = ErrorDyn(r"C:\Users\shliu\Desktop\test1120",
                    50, 0)

    obj.run()
    # obj.treat_diag()
    # a = [1, 2]
    # b = [[8], [7, 8]]
    # c = [10, 11, 12]
    # obj.write_adjust_datas(1, 1, a, b, c)


    # obj = Errorstat(r'C:\Users\anxin\Desktop\test_err_stat')
    # obj.run()

    # obj = OnlyAdjust(r'C:\Users\anxin\Desktop\only_adjust')
    # obj.run()

    # obj = Errorstatdyn(r'C:\Users\anxin\Desktop\test_err_stat_dyn')
    # obj.run_stat_dyn()
    # obj = Error(r"C:\Users\anxin\Desktop\test_err_dyn")
    # obj.get_normal_data()
    # obj.get_group_time()
    # obj.write_err_par_every_time(1, 1)