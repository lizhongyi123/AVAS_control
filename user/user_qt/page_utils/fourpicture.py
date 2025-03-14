import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QGridLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from apis.basic_api.api import plot_dataset

from user.user_qt.page_utils.picture_dialog import Picturewidgetrightkey
# class FourPlotDialog(QDialog):
#     """ 主窗口（QDialog），包含四个散点图 """
#
#     def __init__(self):
#         super().__init__()
#
#     def initUI(self):
#         self.setWindowTitle("弹出窗口 - 显示四个散点图")
#         self.setGeometry(300, 200, 800, 600)  # 调整窗口大小
#
#         layout = QVBoxLayout()
#
#         # 创建 Matplotlib 画布
#         self.figures = [plt.figure(figsize=(4, 3)) for _ in range(4)]
#         self.canvases = [FigureCanvas(fig) for fig in self.figures]
#
#         self.figtoolbar = NavigationToolbar(self.canvases[0], self)  # 创建figure工具栏
#
#         # 创建网格布局
#         grid_layout = QGridLayout()
#
#         # 填充四个子图
#         for i, canvas in enumerate(self.canvases):
#             row, col = divmod(i, 2)  # 计算行列索引
#             grid_layout.addWidget(canvas, row, col)  # 添加到网格布局
#         # self.plot_data(0)  # 画图
#
#         layout.addWidget(self.figtoolbar)
#
#         layout.addLayout(grid_layout)
#         self.setLayout(layout)
#
#
#     def plot_image1(self, file_path, func, picture_type1=None, index=0):
#         #只有一个图像类型
#         project_path = r"C:\Users\anxin\Desktop\test_ini"
#         func(file_path, picture_type1, show_=0, fig=self.figures[index])



class FourPlotDialog(QDialog):
    def __init__(self, project_path, func, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Picture Viewer")

        # 创建 4 个 Picturewidgetrightkey 实例
        self.widgets = [
            Picturewidgetrightkey(project_path, func),
            Picturewidgetrightkey(project_path, func),
            Picturewidgetrightkey(project_path, func),
            Picturewidgetrightkey(project_path, func),
        ]

        # 初始化 UI
        self.initUI()

    def initUI(self):
        layout = QGridLayout()

        # 在网格布局中添加 4 个 Picturewidgetrightkey
        layout.addWidget(self.widgets[0], 0, 0)  # 第一行第一列
        layout.addWidget(self.widgets[1], 0, 1)  # 第一行第二列
        layout.addWidget(self.widgets[2], 1, 0)  # 第二行第一列
        layout.addWidget(self.widgets[3], 1, 1)  # 第二行第二列

        # 初始化所有 widget
        for widget in self.widgets:
            widget.initUI()

        self.setLayout(layout)


if __name__ == "__main__":
    project_path = r"C:\Users\anxin\Desktop\test_ini"

    # app = QApplication(sys.argv)
    # main_dialog = FourPlotDialog()
    # main_dialog.initUI()
    # main_dialog.plot_image1(project_path, plot_dataset, "loss", 0)
    # main_dialog.plot_image1(project_path, plot_dataset, "loss", 3)
    # main_dialog.exec_()  # 以模态方式打开

    app = QApplication(sys.argv)

    # 传入 project_path 和 func 作为参数
    dialog = FourPlotDialog(project_path=project_path, func=plot_dataset)
    dialog.show()