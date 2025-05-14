from utils.treat_directory import list_files_in_directory
from dataprovision.datasetparameter import DatasetParameter
import matplotlib.pyplot as plt
import numpy as np
import matplotlib

matplotlib.use("QtAgg")


if __name__ == '__main__':
    directory_path = r"C:\Users\anxin\Desktop\test_yaxin\data"
    all_dataset = list_files_in_directory(directory_path, sort_by="mtime")

    all_alpha_x = []
    all_beta_x = []
    all_loss = []
    all_center_x = []
    all_emit_x = []
    z = []

    data_range = [50, 150]

    # Collect data
    for path in all_dataset[data_range[0]: data_range[1]]:
        print(path)
        obj = DatasetParameter(path)
        obj.get_parameter()

        all_alpha_x.append(obj.alpha_x)
        all_beta_x.append(obj.beta_x)
        z.append(obj.z)
        all_loss.append(obj.loss)
        all_center_x.append(obj.x)
        all_emit_x.append(obj.emit_x)

    # Convert to proper units
    all_emit_x = [np.array(i1) * 10 ** 6 for i1 in all_emit_x]

    # Create subplots
    fig, axes = plt.subplots(2, 2, figsize=(16, 8))

    # Plot 1: alpha_x vs z
    for i in range(data_range[1] - data_range[0]):
        axes[0, 0].plot(z[i], all_alpha_x[i], label=f"Dataset {i}")
    axes[0, 0].set_xlabel("z")
    axes[0, 0].set_ylabel("alpha_x")
    axes[0, 0].set_title("Alpha_x over Z")
    axes[0, 0].legend(loc='upper right')

    # Plot 2: beta_x vs z
    for i in range(data_range[1] - data_range[0]):
        axes[0, 1].plot(z[i], all_beta_x[i], label=f"Dataset {i}")
    axes[0, 1].set_xlabel("z")
    axes[0, 1].set_ylabel("beta_x")
    axes[0, 1].set_title("Beta_x over Z")
    axes[0, 1].legend(loc='upper right')

    # Plot 3: emit_x vs z
    for i in range(data_range[1] - data_range[0]):
        axes[1, 0].plot(z[i], all_emit_x[i], label=f"Dataset {i}")
    axes[1, 0].set_xlabel("z")
    axes[1, 0].set_ylabel("emit_x (μm)")
    axes[1, 0].set_title("Emit_x over Z")
    axes[1, 0].legend(loc='upper right')

    for i in range(data_range[1] - data_range[0]):
        axes[1, 1].plot(z[i], all_loss[i], label=f"Dataset {i}")
    axes[1, 1].set_xlabel("z")
    axes[1, 1].set_ylabel("Loss")
    axes[1, 1].set_title("Loss over Z")
    axes[1, 1].legend(loc='upper right')


    plt.tight_layout()
    plt.show()
    # Plot 4: loss vs z






