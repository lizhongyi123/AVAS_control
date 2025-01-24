
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

from apps.error_base_function import judge_command_on_element
class Adjust_Error():
    """
    应该接收一个列表
    但是返回优化结果和
    """
    def __init__(self, project_path):
        self.diag_res = {}
        self.project_path = project_path
        self.lattice_mulp_path = os.ath.join(self.project_path, "InputFile", "lattice_mulp.txt")
        self.lattice_path = os.ath.join(self.project_path, "InputFile", "lattice_mulp.txt")

    def generate_adjust_parameter(self, input_lines):
        """
        产生定位信息, adjust命令中哪些参数需要修改
        """
        adjust_parameter_lattice_command = []  # 原来的命令
        adjust_element_num = []  # 第几个元件要改
        adjust_parameter_num = []  # 第几个参数要改
        adjust_parameter_range = []  # 参数的范围
        adjust_parameter_n = []  # 具有一样的值
        adjust_parameter_use_init = []  # 是否使用初值
        adjust_parameter_initial_value = []

        adjust_parameter_num_per = []
        adjust_parameter_range_per = []
        adjust_parameter_n_per = []
        adjust_parameter_use_init_per = []
        index = -1

        index = 0
        # 为adjust命令增加编号
        lattice = copy.deepcopy(input_lines)
        for i in lattice:
            if i[0] == "adjust":
                add_name = f'adjust_{index}'
                i.append(add_name)
                index += 1

        # 为每个调整命令增加作用元件数
        for i in lattice:
            if i[0] == "adjust":
                adjust_on_element = judge_command_on_element(lattice, i)
                i.append(adjust_on_element)
                if adjust_on_element not in adjust_element_num:
                    adjust_element_num.append(adjust_on_element)

        # [['adjust', '0', '1', '0', '0', '0.3', '0', 'adjust_0', 2]]
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
        #返回 哪些元件需要修改， 优化的初始初始值， 哪些参数需要修改， ,每个参数的范围，关联值n，是否使用初值
        return adjust_element_num, adjust_parameter_initial_value, adjust_parameter_num, adjust_parameter_range, \
            adjust_parameter_n, adjust_parameter_use_init

        #[15, 16] [[-38.0], [-0.3, 0.3]] [[6], [5, 4]] [[[-0.5, 0.5]], [[-0.5, 0.5], [-0.5, 0.5]]] [[0], [0, 0]] [[1], [1, 0]]

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

        options = {'maxiter': 100, 'eps': 10 ** -1, 'ftol': 10 ** -4}


        try:
            result = minimize(fun=goal, x0=initial_value, constraints=constraints, bounds=parameter_range,
                              method='SLSQP', options=options)

            return result.x, result.fun

        except Exception:
            return self.ini_this[-1], self.loss_this[-1]

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



        self.diag_res[f"{group}_{time}"] = diag_every_location

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



            # delete_directory(self.error_middle_output0_path)

            self.run_multiparticle(self.project_path, 'OutputFile/error_middle')
            loss = self.treat_diag(group, time, error_lattice_no_index)


            print("loss", loss)
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

    def opti_one_time(self, group, time, lattice_mulp_list):
        """
        静态误差完整跑一次, 需要矫正

        :param group:
        :param time:hg
        :return:
        """

        # 得到lattice的定位信息
        adjust_element_num, adjust_parameter_initial_value, adjust_parameter_num, adjust_parameter_range, \
            adjust_parameter_n, adjust_parameter_use_init = self.generate_adjust_parameter(lattice_mulp_list)

        opti_res_this, loss_this = self.optimize_one_group(group, time, lattice_mulp_list,
                                                           adjust_element_num, adjust_parameter_initial_value,
                                                           adjust_parameter_num,
                                                           adjust_parameter_range, \
                                                           adjust_parameter_n, adjust_parameter_use_init)

        adjust_info = [adjust_element_num, adjust_parameter_initial_value, adjust_parameter_num, adjust_parameter_range, \
            adjust_parameter_n, adjust_parameter_use_init]

        #返回矫正参数信息, 这一次优化的结果， 只一次优化的损失， 束诊结果
        return adjust_info, opti_res_this, loss_this, self.diag_res