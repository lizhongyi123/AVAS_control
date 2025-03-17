from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QToolBar, QVBoxLayout, QWidget, QPushButton, \
    QStackedWidget, QMenu, QLabel, QLineEdit, QTextEdit,  QGridLayout, QHBoxLayout,  QFrame, QFileDialog, QGroupBox, \
    QComboBox, QSizePolicy, QDialog, QCheckBox, QButtonGroup, QMessageBox

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Qt5Agg")
from PyQt5.QtCore import pyqtSignal
from utils.readfile import read_lattice_mulp
import os
from user.user_qt.page_utils.picture_dialog import Picturewidgetrightkey
from apis.basic_api.api import plot_dataset
import sys
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

class PhaseEllipseWidget(Picturewidgetrightkey):
    resize_signal = pyqtSignal()  # 正确初始化自定义信号
    def __init__(self, project_path, func, ):
        super().__init__()

        self.fig_size = (6.4, 4.6)
        self.fig = Figure(figsize=self.fig_size)  # 创建figure对象

        self.func = func
        self.project_path = project_path
        self.picture_type = "rms_x"

    def plot_image(self):
        self.func(self.project_path, self.picture_type, show_=0, fig=self.fig)
        self.canvas.draw()


    def contextMenuEvent(self, event):
        cmenu = QMenu(self)

        menu_items = {
            "rms_x": cmenu.addAction("rms_x"),
            "rms_y": cmenu.addAction("rms_y"),
            "phi": cmenu.addAction("phi"),
            "rms_xy": cmenu.addAction("rms_xy"),
            "max_x": cmenu.addAction("max_x"),
            "max_y": cmenu.addAction("max_y"),
            "max_xy": cmenu.addAction("max_xy"),
            "beta_x": cmenu.addAction("beta_x"),
            "beta_y": cmenu.addAction("beta_y"),
            "beta_z": cmenu.addAction("beta_z"),
            "beta_xyz": cmenu.addAction("beta_xyz"),
        }

        action = cmenu.exec_(self.mapToGlobal(event.pos()))

        for item_name, menu_item in menu_items.items():
            if action == menu_item:
                self.picture_type = item_name
                break
        self.fig.clf()
        self.plot_image()




class FourPlotDialog(QDialog):
    def __init__(self, project_path, func):
        super().__init__()
        self.project_path = project_path
        self.func = func
        self.setWindowTitle("Picture Viewer")

        # 创建 4 个 Picturewidgetrightkey 实例
        self.widgets = [
            PhaseEllipseWidget(self.project_path, func),
            PhaseEllipseWidget(self.project_path, func),
            PhaseEllipseWidget(self.project_path, func),
            PhaseEllipseWidget(self.project_path, func),
        ]

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
    def plot_image(self, parameter):
        index = 0
        self.widgets[index].plot_image()



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
    dialog.initUI()
    dialog.exec_()