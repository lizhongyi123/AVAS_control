from core.LinacOPTEngine import LinacOPTEngine
import math
# from sko.PSO import PSO
# from sko.GA import GA
import ctypes as C
import os
import shutil
import random
from scipy.optimize import minimize
from utils.readfile import read_txt
import time
from utils.myoptimize import gradient_descent_minimize
from apps.basicenv import BasicEnvSim
def mismatch( Twiss1, Twiss2):
    # ʧ��Ⱥ���
    alpha1 = Twiss1[0]
    beta1 = Twiss1[1]
    gamma1 = (1 + alpha1 * alpha1) / beta1

    alpha2 = Twiss2[0]
    beta2 = Twiss2[1]
    gamma2 = (1 + alpha2 * alpha2) / beta2

    # ������Э֮�ٶ�
    if beta2 < 0:
        return 100
    T = beta2 * gamma1 + beta1 * gamma2 - 2 * alpha1 * alpha2
    # ��ֵ���
    if T < 2:
        T = 2
    M = math.sqrt((T + math.sqrt(T * T - 4)) / 2) - 1
    return M

class MatchTwiss():
    """
    twiss����ƥ��(linacopt)
    """
    def __init__(self, project_path):
        self.project_path = project_path
        # self.lattice_test = os.path.join(self.self.project_path, lattice_test)
        self.LinacOPT_engine = LinacOPTEngine()
        self.mismatch = mismatch



    def matchfile(self, filename):
        # ���ڴ����ļ�����������ѭ����lattice
        lattice_file_name = f"InputFile\match_no_command.txt"
        lattice_file_name = os.path.join(self.project_path, lattice_file_name)
        fo_in = open(filename, "r")
        fname_out = open(lattice_file_name, "w+")
        fo_out = open(lattice_file_name, "w+")
        com_number = 1  # �ڼ���Ԫ������1��ʼ
        match_number = 0  # �ڼ�����¼����0��ʼ
        changeline = []  # �����change line �� �Ƿ���ڹ��������޹�
        constraint_eq = []  # ��ʽԼ���ĺ�������
        constraint_ueq = []  # ����Լ���ĺ�������
        name_line = []  # ����������
        tatch_line = []  # ����������� �ڼ���Ԫ�� �ڼ�������  ��������Ϊ0
        tatch_list = []  # ���ڱ��� �������ڼ���������com_number��,������ʽ k*para+b
        lb = []
        ub = []
        goal_twiss = []
        fo_out_list = []
        for line in fo_in.readlines():
            linelist = line.split()
            if linelist[0] == 'MATCHING':
                match_number += 1
                changeline.append(com_number)
                changeline.append(int(linelist[2]))  # �ڼ���������Ҫ�ı�
                changeline.append(0)  # ռλ��
                lb.append(float(linelist[3]))
                ub.append(float(linelist[4]))
                if len(linelist) == 6:
                    name_line.append(linelist[5])
                else:
                    name_line.append(f'PARAM_{com_number}_{int(linelist[2])}')
            elif linelist[0] == 'SETTWISS':
                goal_twiss.append(float(linelist[2]))
                goal_twiss.append(float(linelist[3]))
                goal_twiss.append(float(linelist[4]))
                goal_twiss.append(float(linelist[5]))
            elif linelist[0] == 'MATCH_LINK':
                # ������������

                idx = name_line.index(linelist[2])  # l1 ��g1
                # Ϊ�˱�����ʽ��һ���ԣ��Ӷ�������
                tatch_line.append(com_number)
                tatch_line.append(int(linelist[3]))  # �ڼ���������Ҫ�ı�
                tatch_line.append(0)  # ��֮�����Ĳ������ĸ�һ��
                tatch_list.append(idx)
                tatch_list.append(int(linelist[4]))
                tatch_list.append(int(linelist[5]))
            elif linelist[0] == 'MATCH_CONSTRAINTS':
                # ������ȡԼ������
                Number = len(linelist)  # �ж��ٸ���
                # Լ��������һ����������
                cond = 'lambda x:'
                for i in range(int((Number - 4) / 2)):
                    idx = name_line.index(linelist[2 * i + 4])
                    cond1 = f'x[{idx}]*{linelist[2 * i + 3]}+'
                    cond = cond + cond1
                cond2 = f'({linelist[-1]})'
                cond = cond + cond2
                if int(linelist[2]) == 0:
                    constraint_eq.append(eval(cond))
                else:
                    constraint_ueq.append(eval(cond))

            else:
                fo_out_list.append(line.split())
                fo_out.writelines(line)
                com_number += 1
        fo_out.close()
        fo_in.close()
        return changeline, tatch_line, tatch_list, lb, ub, goal_twiss, constraint_eq, constraint_ueq, fo_out_list

    def get_goal(self, changeline, tatch_line, tatch_list, goalTwiss):
        # ���ڵõ�Ŀ���Ż�����
        def goal(x):
            for i in range(int(len(changeline) / 3)):
                changeline[3 * i + 2] = x[i]
            for i in range(int(len(tatch_line) / 3)):
                tatch_line[3 * i + 2] = x[tatch_list[3 * i]] * tatch_list[3 * i + 1] + tatch_list[3 * i + 2]
            real_changeline = changeline + tatch_line
            change_line = (C.c_double * len(real_changeline))(*real_changeline)
            # for i in range(len(changeline)):
            #	print(change_line[i])


            out = (C.c_double * 6)()

            f1 = r'InputFile\input.txt'
            f2 = r'InputFile\match_no_command.txt'
            f3 = r'InputFile\beam.txt'

            f1 = bytes(os.path.join(self.project_path, f1), encoding='utf-8')
            f2 = bytes(os.path.join(self.project_path, f2), encoding='utf-8')
            f3 = bytes(os.path.join(self.project_path, f3), encoding='utf-8')

            str1 = C.c_char_p()
            str1.value = f1
            str2 = C.c_char_p()
            str2.value = f2
            str3 = C.c_char_p()
            str3.value = f3
            Number = C.c_int(int(len(change_line)/3))
            change_line_p = C.pointer(change_line)
            self.LinacOPT_engine.Trace_win_file_change(str1, str2, str3, change_line_p, Number, out)
            M1 = self.mismatch(goalTwiss[0:2], out[0:2])
            M2 = self.mismatch(goalTwiss[2:4], out[2:4])
            M = M1 + M2
            if math.isnan(M):
                M = 100000
            return M

        return goal

    def goal_lattice(self, changeline, tatch_line, tatch_list, best_x):
        lattice_file_name = f"InputFile\match_no_command.txt"
        goal_file_name = f"OutputFile\match_result.txt"

        lattice_file_name = os.path.join(self.project_path, lattice_file_name)
        goal_file_name = os.path.join(self.project_path, goal_file_name)
        goal = [[]]
        fo_out = open(lattice_file_name, "r")
        for line in fo_out.readlines():
            linelist = line.split()
            goal.append(linelist)
        for i in range(int(len(changeline) / 3)):
            goal[int(changeline[3 * i])][int(changeline[3 * i + 1])] = best_x[i]
        for i in range(int(len(tatch_line) / 3)):
            goal[int(tatch_line[3 * i])][int(tatch_line[3 * i + 1])] = best_x[tatch_list[3 * i]] * tatch_list[
                3 * i + 1] + \
                                                                       tatch_list[3 * i + 2]

        fo_out.close()
        with open(goal_file_name, 'w') as f:
            for i in goal:
                if i != []:
                    for j in i:
                        f.write(str(j))
                        f.write(' ')
                    f.write('\n')
        print("����latticeΪ��")
        with open(goal_file_name, 'r') as f:
            out = f.read()
            print(out)


    def re_run_one(self):
        obj = BasicEnvSim(self.project_path, r"OutputFile\match_result.txt")
        obj.run()
        # f1 = r'InputFile\input.txt'
        # f2 = r"OutputFile\match_result.txt"
        # f3 = r'InputFile\beam.txt'
        # f4 = r"OutputFile\env_output.txt"
        #
        #
        #
        # f1 = bytes(os.path.join(self.project_path, f1), encoding='utf-8')
        # f2 = bytes(os.path.join(self.project_path, f2), encoding='utf-8')
        # f3 = bytes(os.path.join(self.project_path, f3), encoding='utf-8')
        # f4 = bytes(os.path.join(self.project_path, f4), encoding='utf-8')
        #
        # print(196)
        # self.LinacOPT_engine.Trace_win_file(f1, f2, f3, f4)
        #
        # father_dir = os.path.dirname(os.path.abspath(__file__))
        # source_beam_out = os.path.join(father_dir, 'beam_out.txt')
        # destination_beam_out = os.path.join(project_path, 'OutputFile', 'beam_out.txt')
        # shutil.copyfile(source_beam_out, destination_beam_out)
        #
        # source_trm = os.path.join(father_dir, 'Tr_M.txt')
        # destination_trm = os.path.join(project_path, 'OutputFile', 'Tr_M.txt')
        # shutil.copyfile(source_trm, destination_trm)
        #
        # os.remove(source_beam_out)
        # os.remove(source_trm)
        #


    def match_twiss(self, filename, use_lattice_initial_value = 0):
        filename = os.path.join(self.project_path, 'InputFile', filename)
        changeline, tatch_line, tatch_list, m_lb, m_ub, goal_twiss, constraint_eq, constraint_ueq, fo_out_list = self.matchfile(
            filename)
        goal = self.get_goal(changeline, tatch_line, tatch_list, goal_twiss)
# #####################################################################################################
        options = {'maxiter': 100}

        constraints = []
        for i in constraint_eq:
            constraints.append({'type': 'eq', 'fun': i})

        for i in constraint_ueq:
            constraints.append({'type': 'ineq', 'fun': i})


#####################################################################################################
        result = None

        bounds = []
        for i in range(len(m_lb)):
            bounds.append([m_lb[i], m_ub[i]])

        if use_lattice_initial_value == 1:
            changeline_list = [changeline[i:i + 3] for i in range(0, len(changeline), 3)]
            # ��������Ľ��

            lattice_initial_value = []
            for i in range(len(changeline_list)):
                lattice_initial_value.append(float(fo_out_list[changeline_list[i][0]-1][changeline_list[i][1]]))

            result = minimize(fun=goal, x0=lattice_initial_value, constraints=constraints, bounds=bounds, method='SLSQP',
                              options=options)


##########################################################################

        if use_lattice_initial_value == 0:
            result = gradient_descent_minimize(goal, m_lb, m_ub, constraints, options)

        # �����Сfuncֵ��result
        self.goal_lattice(changeline, tatch_line, tatch_list, result.x)

        if result.fun < 0.05:
            print("�����ƥ��,Ŀ��λ����Ŀ��Twiss��ʧ���Ϊ:", result.fun)
        else:
            print("δ���ƥ��,Ŀ��λ����Ŀ��Twiss��ʧ���Ϊ:", result.fun)
            # print(pso.gbest_y)

        self.re_run_one()
        print(result)
        return result.fun

###############################################################################
        # pso=PSO(func=goal, dim=len(m_lb), pop=100, lb=m_lb, ub=m_ub, max_iter=100)
        # pso.run()
        #
        # best_x, best_y = pso.gbest_x, pso.gbest_y
        #
        # if best_y < 0.5:
        #     print("�����ƥ��,Ŀ��λ����Ŀ��Twiss��ʧ���Ϊ:")
        # else:
        #     print("δ���ƥ��,Ŀ��λ����Ŀ��Twiss��ʧ���Ϊ:")
        #
        # print(best_y)
        # self.goal_lattice(changeline, tatch_line, tatch_list, best_x)
        #
        # return best_y

#######################################################################################################
        # ga = GA(func=goal, n_dim=len(m_lb), size_pop=100, lb=m_lb, ub=m_ub, constraint_eq=constraint_eq,
        #         constraint_ueq=constraint_ueq, max_iter=100)
        # best_x, best_y = ga.run()
        #
        # if best_y < 0.5:
        #     print("�����ƥ��,Ŀ��λ����Ŀ��Twiss��ʧ���Ϊ:")
        # else:
        #     print("δ���ƥ��,Ŀ��λ����Ŀ��Twiss��ʧ���Ϊ:")
        #     # print(pso.gbest_y)
        # print(best_y)
        # # goal_lattice(changeline,pso.gbest_x)
        # self.goal_lattice(changeline, tatch_line, tatch_list, best_x)
        # return best_y
        # self.re_run_one()

####################################################################################################
if __name__ == '__main__':
    project_path = r"C:\Users\anxin\Desktop\test_env"

    match_twiss = MatchTwiss(project_path)
    res = match_twiss.match_twiss(f'lattice_env.txt')
    #
    # my_list = []
    #
    # for i in range(10):
    #     res = match_twiss.match_twiss(f'match_lattice.txt')
    #     my_list.append(res)
    # print(my_list)
    #
    # max_value = max(my_list)
    #
    # # ����Сֵ
    # min_value = min(my_list)
    #
    # # ��ƽ��ֵ
    # average_value = sum(my_list) / len(my_list)
    #
    # variance = sum((x - average_value) ** 2 for x in my_list) / (len(my_list) - 1)
    #
    # # ��ӡ���
    # print("���ֵ:", max_value)
    # print("��Сֵ:", min_value)
    # print("ƽ��ֵ:", average_value)
    # # ��ӡ���
    # print("����:", variance)


