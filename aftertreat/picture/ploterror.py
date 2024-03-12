import sys
sys.path.append(r'C:\Users\anxin\Desktop\AVAS_control')

from aftertreat.picture.initialplot import PicturePlot_2D
import os
import time
from dataprovision.datasetparameter import DatasetParameter
import re
import numpy as np

class PlotError(PicturePlot_2D):
    """
    误差分析结果可视化
    """
    def __init__(self, project_path):
        super().__init__()
        self.project_path = project_path


        self.lattice_mulp_path = os.path.join(self.project_path, 'InputFile', 'lattice_mulp.txt')
        self.lattice_path = os.path.join(self.project_path, 'InputFile', 'lattice.txt')
        self.loss = []
        self.ini = []
        self.error_elemment_command = ['err_quad_ncpl_stat', 'err_quad_ncpl_dyn', 'err_cav_ncpl_stat',
                                       'err_cav_ncpl_dyn', ]
        self.error_beam_command = ['err_beam_stat', 'err_beam_dyn']

        self.all_group = 1
        self.all_time = 1
        self.xlabel = 'group'

        self.stat_error_output = os.path.join(self.project_path, 'OutputFile', 'error_output')
    def get_group_time(self):
        """
        得到group和time
        :return:
        """
        input_lines = []
        with open(self.lattice_mulp_path, encoding='utf-8') as file_object:
            for line in file_object:
                input_lines.append(line)

        input_lines = [i.split() for i in input_lines if i.strip()]
        for i in input_lines:
            if i[0] == 'err_step':
                self.all_group = int(i[1])
                self.all_time = int(i[2])
        print(self.all_group, self.all_time)

    def get_dataset_obj(self):
        dic = {}
        for i in range(self.all_group):
            for j in range(self.all_time):
                file_name = f'output_{i}_{j}'
                path = os.path.join(self.stat_error_output, file_name, 'DataSet.txt')

                obj = DatasetParameter(path)
                obj.get_parameter()
                dic[file_name] = obj

        return dic

    def get_x_y(self, picture_name, picture_type='average'):
        self.get_group_time()
        self.get_dataset_obj()

        dataset_obj = self.get_dataset_obj()
        self.x = []
        self.y = []
        dic = {}

        for i in range(self.all_group):
            self.x.append(i)
            pattern = re.compile(f'^output_{i}.*')  # 定义匹配模式
            if picture_name == 'energy':
                output_i_value = [value.ek[-1] for key, value in dataset_obj.items() if pattern.findall(key)]
                dic[i] = np.array(output_i_value)
                self.ylabel = 'Ek(MeV)'

            elif picture_name == 'x':
                output_i_value = [value.x[-1] * 1000 for key, value in dataset_obj.items() if pattern.findall(key)]
                dic[i] = np.array(output_i_value)
                self.ylabel = 'x(mm)'

            elif picture_name == 'y':
                output_i_value = [value.y[-1] *1000 for key, value in dataset_obj.items() if pattern.findall(key)]
                dic[i] = np.array(output_i_value)
                self.ylabel = 'y(mm)'


            elif picture_name == 'rms_x':
                output_i_value = [value.rms_x[-1] * 1000 for key, value in dataset_obj.items() if pattern.findall(key)]
                dic[i] = np.array(output_i_value)
                self.ylabel = 'rms_x(mm)'

            elif picture_name == 'rms_y':
                output_i_value = [value.rms_y[-1] * 1000 for key, value in dataset_obj.items() if pattern.findall(key)]
                dic[i] = np.array(output_i_value)
                self.ylabel = 'rms_y(mm)'

        self.markers = ['o']
        def get_rms(x):
            return np.sqrt(np.sum([(i - np.mean(x)) ** 2 for i in x]) / len(x))

        print(dic)
        if picture_type == 'average':
            self.y = [np.mean(value) for key, value in dic.items()]
        if picture_type == 'rms':

            self.y = [get_rms(value) for key, value in dic.items()]
        print(self.y)



if __name__ == "__main__":

    start = time.time()
    print("start", start)
    obj = PlotError(r'C:\Users\anxin\Desktop\test')


    obj.get_x_y('y', 'average')
    obj.run(show_=1)
    end = time.time()
    print("end", end)




