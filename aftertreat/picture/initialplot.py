"""改文件定义了图像的初始类"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
import numpy as np
class PicturelBar_2D():
    """
    二维柱状图，父类
    """
    def __init__(self):
        self.title = ''
        self.xlabel = ''
        self.ylabel = ''
        self.fontsize = 14
        self.x = []
        self.y = []
        self.color = 'red'



    def get_x_y(self, file_path):
        self.x = []
        self.y = []
        return self.x, self.y

    def run(self, show_):
        if show_:
            plt.figure()
        # 创建柱状图
        plt.bar(self.x, self.y, color = self.color)

        # plt.xlim(0, max(self.x) + 1)
        # plt.ylim(0, max(self.y) + 1)

        # 添加标题和标签
        # plt.title('Bar Chart Example')
        plt.xlabel(self.xlabel, fontsize=self.fontsize)
        plt.ylabel(self.ylabel, fontsize=self.fontsize)
        if show_:
            plt.show()
            return None

        else:
            return None

        # 设置小坐标是朝内还是朝外
        # plt.rcParams['xtick.direction'] = 'in'
        # plt.rcParams['ytick.direction'] = 'in'

        # plt.xticks(fontsize=30)  # 设置x轴刻度标签的大小
        # plt.yticks(fontsize=30)  # 设置y轴刻度标签的大小

        # font = {'size': 15}
        # plt.legend(prop=font)
        #
        # bwith = 1.5  # 边框宽度设置为
        # TK = plt.gca()  # 获取边框
        # TK.spines['bottom'].set_linewidth(bwith)  # 图框下边
        # TK.spines['left'].set_linewidth(bwith)  # 图框左边
        # TK.spines['top'].set_linewidth(bwith)  # 图框上边
        # TK.spines['right'].set_linewidth(bwith)  # 图框右边

        # 设置小坐标的大小
        # plt.tick_params(axis='both', direction='in', labelsize=12.5)
        # plt.tick_params(which='major', width=1.5, length=6)
        # plt.tick_params(which='minor', width=1, length=3)

        # x_major_locator = MultipleLocator(0.2)
        # # 把x轴的刻度间隔设置为1，并存在变量里
        # xminorLocator = MultipleLocator(0.05)  # 将x轴次刻度标签设置为n的倍数
        #
        # y_major_locator = MultipleLocator(20)
        # # 把y轴的刻度间隔设置为10，并存在变量里
        # y_minor_locator = MultipleLocator(5)
        # # 把y轴的刻度间隔设置为10，并存在变量里
        #
        # ax = plt.gca()
        # # ax为两条坐标轴的实例
        # ax.xaxis.set_major_locator(x_major_locator)
        # ax.xaxis.set_minor_locator(xminorLocator)
        # # 把x轴的主刻度设置为1的倍数
        #
        # ax.yaxis.set_major_locator(y_major_locator)
        # ax.yaxis.set_minor_locator(y_minor_locator)

        # 显示图像

class PicturePlot_2D():
    """
    二维散点图，折线图，父类
    """
    def __init__(self):
        self.title = ''
        self.xlabel = ''
        self.ylabel = ''
        self.fontsize = 14
        self.fig_size = (6.4 , 4.8)
        self.x = []
        self.y = []
        self.colors = ['r', 'b', 'g']
        self.markers = [None] * 10
        self.labels = [None] * 10
        self.xlim = []
        self.ylim = []
        self.set_legend = 0
        self.patch_list=None

    def get_x_y(self):
        self.x = []
        self.y = []
        return self.x, self.y

    def run(self, show_, ):
        if show_:
            plt.figure(figsize=self.fig_size)
        # 创建柱状图
        if len(self.y) == 0:
            print("The ordinate is empty")
        elif isinstance(self.y[0], list):
            for i in range(len(self.y)):
                plt.plot(self.x, self.y[i], color=self.colors[i], marker=self.markers[i], label=self.labels[i])

        elif isinstance(self.y[0], int) or isinstance(self.y[0], float):
            plt.plot(self.x, self.y, color=self.colors[0], marker=self.markers[0])


        # 添加标题和标签
        # plt.title('Bar Chart Example')

        plt.xlabel(self.xlabel, fontsize=self.fontsize)
        plt.ylabel(self.ylabel, fontsize=self.fontsize)

        if len(self.xlim) == 2:
            plt.xlim(self.xlim[0], self.xlim[1])


        if len(self.ylim) == 2:
            plt.ylim(self.ylim[0], self.ylim[1])

        if self.set_legend == 1:
            plt.legend()


        if self.patch_list:
            for shapes in self.patch_list:
                for shape in shapes:
                    plt.gca().add_patch(shape)

        plt.grid()

        if show_:
            plt.show()
            return None

        else:
            return None


class CompoundShape():
    def __init__(self, ):
        pass

    def create_shapes(self, square_origin, length, height, element):
        facecolor = ""
        if element == "sol":
            facecolor = "lime"
        elif element == "cav":
            facecolor = "yellow"

        shapes = []

        # 创建正方形
        square = patches.Rectangle(square_origin, length, height, linewidth=1, edgecolor="black", facecolor=facecolor)

        shapes.append(square)
        ratio = 0.9
        points_inside_square_1 = [
            (square_origin[0], square_origin[1] + ratio * height),
            (square_origin[0] + 1 / 3 * length, square_origin[1] + (1 - ratio) * height),
            (square_origin[0] + 2 / 3 * length, square_origin[1] + ratio * height),
            (square_origin[0] + 1 * length, square_origin[1] + (1 - ratio) * height),

        ]

        curve_codes_1 = [Path.MOVETO] + [Path.LINETO] * 3
        curve_path_1 = Path(points_inside_square_1, curve_codes_1)

        # 创建曲线
        curve_patch_1 = patches.PathPatch(curve_path_1, linewidth=1, facecolor='none')
        shapes.append(curve_patch_1)

        points_inside_square_2 = [
            (square_origin[0], square_origin[1] + (1 - ratio) * height),
            (square_origin[0] + 1 / 3 * length, square_origin[1] + ratio * height),
            (square_origin[0] + 2 / 3 * length, square_origin[1] + (1 - ratio) * height),
            (square_origin[0] + 1 * length, square_origin[1] + ratio * height),

        ]

        curve_codes_2 = [Path.MOVETO] + [Path.LINETO] * 3
        curve_path_2 = Path(points_inside_square_2, curve_codes_2)

        # 创建曲线
        curve_patch_2 = patches.PathPatch(curve_path_2, linewidth=1, facecolor='none')
        shapes.append(curve_patch_2)

        # 创建圆形

        return shapes

# if __name__ == "__main__":
#     v = PicturelBar_2D()
#     v.run()