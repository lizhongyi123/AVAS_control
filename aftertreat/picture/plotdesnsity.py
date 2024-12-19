#用于将density中的图像可视化
from aftertreat.picture.initialplot import PicturePlot_2D, Picturedensity
from dataprovision.densityparameter import DensityParameter
import matplotlib.pyplot as plt
import numpy as np
class PlotDensity(Picturedensity):
    def __init__(self, path):
        super(PlotDensity, self).__init__()
        self.path = path
        self.bins = 300

    def get_data(self, picture_type):
        file_obj = DensityParameter(self.path)
        data = file_obj.get_parameter()
        # print(data["tab_lis"])
        type_lis = ['x', 'y', 'r', 'z']
        self.z = data["zg_lis"]

        index = type_lis.index(picture_type)

        self.y = []
        self.density = []
        for i in range(len(self.z)):
            v = [data["minb_lis"][i][index] * 1000, data["maxb_lis"][i][index] * 1000]
            self.y.append(v)
            this_density = np.array(data["tab_lis"][i][index])

            if index == 2:
                bin_edges = np.linspace(v[0], v[1], self.bins + 1)
                # 面积
                area = np.array([bin_edges[i] ** 2 - bin_edges[i - 1] ** 2 for i in range(1, len(bin_edges))])
                ration = this_density / area
                this_density = ration
            self.density.append(this_density)




        # print(self.y)
        self.xlabel = "Position(m)"

        if picture_type == 'x':
            self.ylabel = "X (mm)"
        elif picture_type == 'y':
            self.ylabel = "Y (mm)"
        elif picture_type == 'r':
            self.ylabel = "R (mm)"
        elif picture_type == 'z':
            self.ylabel = "Z (mm)"

        self.ylim = [-10, 10]

class PlotDensityLevel(PicturePlot_2D):
    def __init__(self, path):
        super().__init__()
        self.bins = 300
        self.path = path
    def get_x_y(self, picture_type):
        file_obj = DensityParameter(self.path)
        data = file_obj.get_parameter()
        # print(data["tab_lis"])
        type_lis = ['x', 'y', 'r', 'z']
        self.x = data["zg_lis"]

        index = type_lis.index(picture_type)
        edge_max = []
        edge_min = []
        if index != 2:
            for i in range(len(self.x)):
                v = [data["minb_lis"][i][index] * 1000, data["maxb_lis"][i][index] * 1000]
                density = data["tab_lis"][i][index]

                counts1 = np.array(density[150:])
                # 对前半部分取反
                counts2 = np.array(density[:150][::-1])

                bin_edges = np.linspace(v[0], v[1], self.bins+1)[:300]
                edge1 = bin_edges[150:]
                edge2 = bin_edges[0:150][::-1]

                ratio = counts1 + counts2

                # 归一化 ratio，使得总和为 1
                ratio_normalized = ratio / np.sum(ratio)

                # 计算归一化后的累积比例
                cumulative_ratio = np.cumsum(ratio_normalized)
                # print(cumulative_ratio)

                # 找到达到90%、99%、99.9%累积值的索引
                thresholds = [0.9, 0.99, 0.999, 0.9999]
                threshold_indices = [np.searchsorted(cumulative_ratio, threshold) for threshold in thresholds]
                # print(threshold_indices)

                # 获取对应边界的值
                # 上边界
                boundaries1 = [edge1[idx] for idx in threshold_indices]
                #下边界
                boundaries2 = [edge2[idx] for idx in threshold_indices]
                # print(boundaries1)
                # print(boundaries2)

                edge_max.append(boundaries1)
                edge_min.append(boundaries2)
                # breakpoint()

            edge_max_90 = [i[0] for i in edge_max]
            edge_max_99 = [i[1] for i in edge_max]
            edge_max_999 = [i[2] for i in edge_max]
            edge_max_9999 = [i[2] for i in edge_max]

            edge_min_90 = [i[0] for i in edge_min]
            edge_min_99 = [i[1] for i in edge_min]
            edge_min_999 = [i[2] for i in edge_min]
            edge_min_9999 = [i[2] for i in edge_min]

            self.y = [
                edge_max_90,
                edge_max_99,
                edge_max_999,
                edge_max_9999,
                edge_min_90,
                edge_min_99,
                edge_min_999,
                edge_min_9999,

            ]
        elif index ==2:
            for i in range(len(self.x)):
                v = [data["minb_lis"][i][index] * 1000, data["maxb_lis"][i][index] * 1000]

                density = data["tab_lis"][i][index]


                ratio = density

                # 归一化 ratio，使得总和为 1
                ratio_normalized = ratio / np.sum(ratio)

                # 计算归一化后的累积比例
                cumulative_ratio = np.cumsum(ratio_normalized)
                # print(cumulative_ratio)
                bin_edges = np.linspace(v[0], v[1], self.bins + 1)[:300]
                edge1 = bin_edges
                # 找到达到90%、99%、99.9%累积值的索引
                thresholds = [0.9, 0.99, 0.999, 0.9999]
                threshold_indices = [np.searchsorted(cumulative_ratio, threshold) for threshold in thresholds]
                # print(threshold_indices)

                # 获取对应边界的值
                # 上边界
                boundaries1 = [edge1[idx] for idx in threshold_indices]

                edge_max.append(boundaries1)

                # breakpoint()

                edge_max_90 = [i[0] for i in edge_max]
                edge_max_99 = [i[1] for i in edge_max]
                edge_max_999 = [i[2] for i in edge_max]
                edge_max_9999 = [i[2] for i in edge_max]



                self.y = [
                    edge_max_90,
                    edge_max_99,
                    edge_max_999,
                    edge_max_9999,
                ]
        # self.xlim = [0.5, 0.75]
        self.ylim = [-20, 20]
        self.colors = ['r', 'b', 'blueviolet', 'g'] * 2

        self.xlabel = "Position(m)"

        if picture_type == 'x':
            self.ylabel = "X Particle density probability (mm)"

        elif picture_type == 'y':
            self.ylabel = "Y Particle density probability (mm)"

        elif picture_type == 'r':
            self.ylabel = "R Particle density probability (mm)"

        elif picture_type == 'z':
            self.ylabel = "Z Particle density probability (mm)"

        labels = [r'$10^{-1}$', r'$10^{-2}$', r'$10^{-3}$', r'$10^{-4}$', None, None, None, None]
        self.labels = labels
        self.set_legend = True

        # print(len(self.x))
        # print(len(edge_max_90))


class PlotDensityProcess(PicturePlot_2D):
    """
    用来将density文件中其他数据可视化
    """
    def __init__(self, path):
        super().__init__()
        self.path = path
    def get_x_y(self, picture_name):
        file_obj = DensityParameter(self.path)
        data = file_obj.get_parameter()
        self.x = data["zg_lis"]
        emit = data["emit_lis"]
        if picture_name == 'emit_x':
            self.y = [i[0] *10**6  for i in emit]

            self.xlabel = "z(m)"
            self.ylabel = "Average Emit_x(pi*mm*mrad)"

        elif picture_name == 'lost':
            self.y = data["lost_lis"]


            self.xlabel = "z(m)"
            self.ylabel = "Average Loss(pi*mm*mrad)"


        elif picture_name == 'rms_x':
            rms_size_lis = data["rms_size_lis"]
            rmsx = [i[0]*10**3 for i in rms_size_lis]

            self.y = rmsx
            self.xlabel = "z(m)"
            self.ylabel = "Average Rms_x(mm)"

        elif picture_name == 'av_xy':
            moy_lis = data["moy_lis"]
            x = [i[0]*10**3 for i in moy_lis]
            y = [i[1]*10**3 for i in moy_lis]
            self.y = [x, y]
            self.labels = ['x', 'y',]
            self.xlabel = "z(m)"
            self.ylabel = "Average Position(mm)"
            self.set_legend = 1


        elif picture_name == 'rms_xy':
            rms_size_lis = data["rms_size_lis"]

            rmsx = [i[0]*10**3 for i in rms_size_lis]
            rmsy = [i[1]*10**3 for i in rms_size_lis]

            self.y = [rmsx, rmsy]
            self.xlabel = "z(m)"
            self.ylabel = "Average Rms size(mm)"
            self.labels = ['x', 'y',]
            self.set_legend = 1
if __name__ == "__main__":
    # path1 = r"C:\Users\shliu\Desktop\testz\OutputFile\density_par_2_2.dat"
    # path2 = r"C:\Users\shliu\Desktop\testz\OutputFile\density_tot_par_2.dat"
    # path3 = r"C:\Users\shliu\Desktop\testz\OutputFile\density_tot_par.dat"

    # path1 = r"C:\Users\shliu\Desktop\test_yiman3\AVAS1\OutputFile\density_par_1_98.dat"
    path1 = r"C:\Users\shliu\Desktop\test_yiman3\AVAS1\save\density_par_0_0.dat"
    # v = PlotDensity(path1)
    # v.get_data('x')
    # v.ylim = [-50, 50]
    # v.run(show_=1, fig=None)


    v = PlotDensityLevel(path1)
    v.get_x_y(picture_type='r')
    v.ylim = [0, 50]
    v.run(show_=1, fig=None)
    # v = PlotDensityProcess(path1)
    # v.get_x_y('rms_xy')
    # v.run(show_=1, fig=None)