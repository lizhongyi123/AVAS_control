from utils.treat_directory import list_files_in_directory
from dataprovision.datasetparameter import DatasetParameter
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import os
import shutil
from utils.readfile import read_txt
if __name__ == '__main__':
    directory_path = r"E:\using\hu\saomiao_mebt\data"
    all_dataset = list_files_in_directory(directory_path)
    all_alpha_x = []
    all_loss = []
    all_center_x = []
    all_emit_x = []
    z = []

    v_path_list = []
    for path in all_dataset:
        obj = DatasetParameter(path)
        obj.get_parameter()
        all_alpha_x.append(obj.alpha_x)
        z.append(obj.z)
        all_loss.append(obj.loss)
        all_center_x.append(obj.x)
        all_emit_x.append(obj.emit_x)

        #筛选dataset
        if obj.loss[-1] < 1:
            # print(25, path)
            v_path_list.append(path)

    #把选出来的dataset复制到一个荻港
    for i in v_path_list:
        orig_dataset = i
        new_data_path = r"E:\using\hu\saomiao_mebt\data_0"

        destination_folder = os.path.join(new_data_path, i.split('/')[-1])
        shutil.copy(orig_dataset, destination_folder)


    #找出dataset的索引
    index_list = []
    for i in v_path_list:
        index = i.split('/')[-1].split('_')[-1].split('.')[0]
        index_list.append(index)
    print(index_list)




    #将随机数复制出来
    suiji_path = r"E:\using\hu\saomiao_mebt\suiji.txt"
    suiji_res = read_txt(suiji_path, out="list")

    new_suiji_res = [i for i in suiji_res if i[0] in index_list]

    new_suiji_path = os.path.join(r"E:\using\hu\saomiao_mebt\data_0", "suiji.txt")
    with open(new_suiji_path, 'w') as f:
        for i in new_suiji_res:
            f.write(' '.join(map(str, i)) + '\n')

    # all_emit_x = [np.array(i1) * 10 ** 6 for i1 in all_emit_x]
    #
    # fig, axes = plt.subplots(1, 2, figsize=(8, 12))
    #
    # # 绘制第一张图 (all_emit_x)
    # for i in range(30):
    #     axes[0].plot(z[i], all_emit_x[i], label=str(i))
    # axes[0].set_xlabel("z")
    # axes[0].set_ylabel("all_emit_x")
    # axes[0].set_title("Emission X over Z")
    # axes[0].legend()
    #
    # # 绘制第二张图 (all_alpha_x)
    # for i in range(30):
    #     axes[1].plot(z[i], all_loss[i], label=str(i))
    # axes[1].set_xlabel("z")
    # axes[1].set_ylabel("all_loss")
    # axes[1].set_title("all_loss")
    # axes[1].legend()
    #
    # # 调整布局并显示
    # plt.tight_layout()
    # plt.show()