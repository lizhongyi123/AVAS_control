

from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QToolBar, QVBoxLayout, QWidget, QPushButton, \
    QStackedWidget, QMenu, QLabel, QLineEdit, QTextEdit,  QGridLayout, QHBoxLayout,  QFrame, QFileDialog, QGroupBox, \
    QComboBox, QSizePolicy, QDialog, QCheckBox, QButtonGroup, QMessageBox

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt

from PyQt5.QtCore import pyqtSignal


class PictureDialog1(QDialog):
    resize_signal = pyqtSignal()  # 正确初始化自定义信号
    def __init__(self, ):
        super().__init__()
        self.fig_size = (6.4, 4.6)

        self.fig = Figure(figsize=self.fig_size)  # 创建figure对象

    def initUI(self):
        winflags = Qt.Dialog
        # 添加最小化按钮
        winflags |= Qt.WindowMinimizeButtonHint
        # 添加最大化按钮
        winflags |= Qt.WindowMaximizeButtonHint
        # 添加关闭按钮
        winflags |= Qt.WindowCloseButtonHint
        # 设置到窗体上
        self.setWindowFlags(winflags)

        # 创建一个容纳工具栏和图像的 QWidget
        self.setWindowTitle('弹出窗口')
        # self.setGeometry(200, 200, 640, 480)

################################
        self.canvas = FigureCanvas(self.fig)  # 创建figure画布
        self.figtoolbar = NavigationToolbar(self.canvas, self)  # 创建figure工具栏
###############################
        # container_widget = QWidget(self)

        layout = QVBoxLayout()
        # container_widget.setLayout(layout)

        toolbar = QToolBar()

        # refresh_action = QAction('刷新', self)
        # toolbar.addAction(refresh_action)
        ########################################

        layout.addWidget(toolbar)


        # self.image_label = QLabel(self)

        # self.image_label.setScaledContents(True)

        #############
        layout.addWidget(self.figtoolbar)  # 工具栏添加到窗口布局中
        layout.addWidget(self.canvas)  # 画布添加到窗口布局中
        # layout.addWidget(self.image_label)

        self.setLayout(layout)
        self.resize_signal.connect(self.on_resize)  # 连接信号和槽

    def resizeEvent(self, event):
        # 当窗口被拉伸时，发出自定义信号
        self.resize_signal.emit()
        return super().resizeEvent(event)


    def on_resize(self):
        self.fig.tight_layout()
        # self.fig.subplots_adjust(left=0.5 )

    def closeEvent(self, event):
        event.accept()



class PlotOnePicture1(PictureDialog1):
    # 只有一张图，接收参数为文件路径， 类， 图片类型
    def __init__(self, file_path, func, picture_type=None):
        super().__init__()
        self.picture_type = picture_type
        self.func = func
        self.file_path = file_path
    def plot_image(self, ):
        if self.picture_type:
            self.func(self.file_path, self.picture_type, show_=0, fig=self.fig)
        else:
            self.func(self.file_path, show_=0, fig=self.fig)
        # if self.picture_type:
        #     obj = self.cls(self.file_path, self.picture_type)
        # else:
        #     obj = self.cls(self.file_path)
        # obj.get_x_y()
        # obj.run( show_=0, fig=self.fig)