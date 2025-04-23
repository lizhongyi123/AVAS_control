from utils.treat_directory import list_files_in_directory
from dataprovision.datasetparameter import DatasetParameter
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
if __name__ == '__main__':
    directory_path = r"E:\using\hu\saomiao_mebt\data"
    all_dataset = list_files_in_directory(directory_path)
    all_alpha_x = []
    all_loss = []
    all_center_x = []
    all_emit_x = []
    z = []

    for path in all_dataset:
        obj = DatasetParameter(path)
        obj.get_parameter()
        all_alpha_x.append(obj.alpha_x)
        z.append(obj.z)
        all_loss.append(obj.loss)
        all_center_x.append(obj.x)
        all_emit_x.append(obj.emit_x)


    all_emit_x = [np.array(i1) * 10 ** 6 for i1 in all_emit_x]

    fig, axes = plt.subplots(1, 2, figsize=(16, 8))

    # 绘制第一张图 (all_emit_x)
    for i in range(10):
        axes[0].plot(z[i], all_emit_x[i], label=str(i))
    axes[0].set_xlabel("z")
    axes[0].set_ylabel("all_emit_x")
    axes[0].set_title("Emission X over Z")
    axes[0].legend()

    # 绘制第二张图 (all_alpha_x)
    for i in range(10):
        axes[1].plot(z[i], all_loss[i], label=str(i))
    axes[1].set_xlabel("z")
    axes[1].set_ylabel("all_loss")
    axes[1].set_title("all_loss")
    axes[1].legend()

    # 调整布局并显示
    plt.tight_layout()
    plt.show()





