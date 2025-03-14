

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

#最普通的，只有一张图片

class CustomToolBar(QToolBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.actions = {}  # 存储按钮的名称和 QAction 对象

    def add_tool_button(self, name, callback):
        """
        添加一个工具栏按钮
        :param name: 按钮名称
        :param callback: 按钮点击后的回调函数
        """
        action = QAction(name, self)
        action.triggered.connect(callback)  # 绑定点击事件
        self.addAction(action)
        self.actions[name] = action  # 记录按钮
        return action

    def remove_tool_button(self, name):
        """移除指定的按钮"""
        if name in self.actions:
            action = self.actions.pop(name)
            self.removeAction(action)

    def clear_toolbar(self):
        """清空工具栏"""
        self.actions.clear()
        self.clear()

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

##############################
        self.toolbar = CustomToolBar(self)

        # 添加多个按钮，每个按钮绑定不同的槽函数
        self.toolbar.add_tool_button("刷新", self.refresh)
        self.toolbar.add_tool_button("打开", self.open_file)
        self.toolbar.add_tool_button("保存", self.save_file)
        #############




        layout.addWidget(self.toolbar)
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


    # 只有一张图，接收参数为文件路径， 函数， 图片类型1
    def plot_image1(self, file_path, func, picture_type=None):

        if picture_type:
            func(file_path, picture_type, show_=0, fig=self.fig)
        else:
            func(file_path, show_=0, fig=self.fig)

    def plot_image2(self, file_path, func, picture_type1=None, picture_type2=None):
        func(file_path, picture_type1, picture_type2, show_=0, fig=self.fig)

    def refresh(self):
        print("刷新按钮被点击！")

    def open_file(self):
        print("打开文件！")

    def save_file(self):
        print("保存文件！")



#这是一个带有右键的组件
class Picturewidgetrightkey(QWidget):
    resize_signal = pyqtSignal()  # 正确初始化自定义信号
    def __init__(self, project_path, func):
        super().__init__()
        self.func = func
        self.project_path = project_path
        self.picture_type = 'rms_x'

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
        self.setWindowTitle('弹出窗口')
        # self.setGeometry(200, 200, 400, 300)
################################
        self.canvas = FigureCanvas(self.fig)  # 创建figure画布
        self.figtoolbar = NavigationToolbar(self.canvas, self)  # 创建figure工具栏
###############################

        # 创建一个容纳工具栏和图像的 QWidget
        container_widget = QWidget(self)

        layout = QVBoxLayout()
        container_widget.setLayout(layout)

        toolbar = QToolBar()
        layout.addWidget(toolbar)


        # 将右键上下文菜单与 self.image_label 绑定
        container_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        container_widget.customContextMenuRequested.connect(self.contextMenuEvent)

        layout.addWidget(self.figtoolbar)  # 工具栏添加到窗口布局中
        layout.addWidget(self.canvas)  # 画布添加到窗口布局中

        self.setLayout(layout)
        self.plot_image()

    def plot_image(self):
        self.fig.clf()
        self.func(self.project_path, self.picture_type, show_=0, fig=self.fig)
        # obj = self.cls(self.file_path, self.picture_type,)
        # obj.get_x_y()
        # obj.run( show_=0, fig=self.fig)
        self.canvas.draw()

    def resizeEvent(self, event):
        # 当窗口被拉伸时，发出自定义信号
        self.resize_signal.emit()
        return super().resizeEvent(event)


    def on_resize(self):
        self.fig.tight_layout()
        # plt.subplots_adjust(top=0.8 )


    # def closeEvent(self, event):
    #     event.accept()

    # def contextMenuEvent(self, event):
    #     cmenu = QMenu(self)
    #
    #     menu_items = {
    #         "rms_x": cmenu.addAction("rms_x"),
    #         "rms_y": cmenu.addAction("rms_y"),
    #         "phi": cmenu.addAction("phi"),
    #         "rms_xy": cmenu.addAction("rms_xy"),
    #         "max_x": cmenu.addAction("max_x"),
    #         "max_y": cmenu.addAction("max_y"),
    #         "max_xy": cmenu.addAction("max_xy"),
    #         "beta_x": cmenu.addAction("beta_x"),
    #         "beta_y": cmenu.addAction("beta_y"),
    #         "beta_z": cmenu.addAction("beta_z"),
    #         "beta_xyz": cmenu.addAction("beta_xyz"),
    #     }
    #
    #     action = cmenu.exec_(self.mapToGlobal(event.pos()))
    #
    #     for item_name, menu_item in menu_items.items():
    #         if action == menu_item:
    #             self.picture_type = item_name
    #             break
    #     self.fig.clf()
    #     self.plot_image()


class MulpEnvelopeDialog(QDialog):
    def __init__(self, project_path, func, parent=None):
        super().__init__(parent)
        self.project_path = project_path
        self.func = func
    def initUI(self):
        self.setWindowTitle("Envelope Dialog")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()

        # 创建 Picturewidgetrightkey 组件
        self.picture_widget = Picturewidgetrightkey(self.project_path, self.func)
        # 绑定新的 contextMenuEvent 方法
        self.picture_widget.contextMenuEvent = self.custom_context_menu
        self.picture_widget.initUI()

        # # 监听 Picturewidgetrightkey 的 resize 信号
        # self.picture_widget.resize_signal.connect(self.on_picture_resize)

        # 添加到布局
        self.layout.addWidget(self.picture_widget)



        self.setLayout(self.layout)

    def on_picture_resize(self):
        """当 Picturewidgetrightkey 调整大小时更新布局"""
        self.picture_widget.fig.tight_layout()


    def custom_context_menu(self, event):
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
                self.picture_widget.picture_type = item_name
                break
        self.picture_widget.fig.clf()
        self.picture_widget.plot_image()

if __name__ == "__main__":
    obj = PictureDialog1()
    obj.initUI()
    obj.exec_()