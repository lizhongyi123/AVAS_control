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