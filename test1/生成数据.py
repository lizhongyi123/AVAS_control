import copy
import os.path
import sys

from utils.readfile import read_txt
import numpy as np
from core.MultiParticle import MultiParticle
import shutil
if __name__ == "__main__":
    project_path = r"C:\Users\anxin\Desktop\test_yaxin"

    lattice_mulp_path = os.path.join(project_path, "InputFile", "lattice_mulp.txt")
    lattice_path = os.path.join(project_path, "InputFile", "lattice.txt")


    lattice_mulp_lis = read_txt(lattice_mulp_path, out='list', readdall=True)

    # print(lattice_mulp_lis)

    orig_data = np.array([289.543, -276.219, 209.933, -147.316, 209.068, -156.973])
    # orig_data_min = orig_data - [30, 30, 30, 30, 30, 30]
    # orig_data_max = orig_data + [30, 30, 30, 30, 30, 30]
    
    orig_data_min = orig_data - [30, 30, 30, 30, 30, 30]
    orig_data_max = orig_data + [30, 30, 30, 30, 30, 30]
    
    for i in range(0, 10000):
        new_lis = []
        random_num = [round(np.random.uniform(orig_data_min[i], orig_data_max[i]), 5) for i in range(6)]
        # random_num = [307.68163, -246.67161, 180.10864, -122.10816, 204.09585, -131.3486]
        new_lis = []

        index = 0
        for j in lattice_mulp_lis:
            if len(j) > 0 and j[0] == "fieldx":
                v = copy.deepcopy(j)
                v[0] = 'field'
                v[-2] = random_num[index]
                new_lis.append(v)
                index += 1

            else:
                new_lis.append(j)

        with open(lattice_path, 'w') as f:
            for k in new_lis:
                f.write(' '.join(map(str, k)) + '\n')

        #随机数保存
        suiji = os.path.join(project_path, "suiji.txt")

        random_num.insert(0, i)
        with open(suiji, 'a') as f:
            f.write(' '.join(map(str, random_num)) + '\n')


        item = {"project_path": project_path}
        #模拟
        obj = MultiParticle(item)
        obj.run()

        #dataset复制
        orig_dataset = os.path.join(project_path, "OutputFile", "DataSet.txt")
        destination_folder = os.path.join(project_path, "data", f"dataset_{i}.txt")

        shutil.copy(orig_dataset, destination_folder)
