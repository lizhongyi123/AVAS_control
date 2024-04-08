import sys
import time

from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QToolBar, QVBoxLayout, QWidget, QPushButton, \
    QStackedWidget, QMenu, QLabel, QLineEdit, QTextEdit,  QGridLayout, QHBoxLayout,  QFrame, QFileDialog, QGroupBox, \
    QComboBox, QSizePolicy, QDialog, QCheckBox, QButtonGroup, QMessageBox

import os
from utils.readfile import read_txt, read_dst
from PyQt5.QtCore import Qt, QSize
from api import plot_cavity_syn_phase, plot_dataset,  plot_cavity_voltage,\
     plot_phase, plot_phase_advance, plot_error
from user.user_qt.user_defined import treat_err

from matplotlib.backends.backend_qtagg import FigureCanvas, NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtCore import pyqtSignal  # 注意这里使用 PyQt5
from api import plot_env_beam_out

from aftertreat.dataanalysis.plttodst import Plttodst

class MyPictureDialog(QDialog):
    resize_signal = pyqtSignal()  # 正确初始化自定义信号
    def __init__(self, project_path, func):
        super().__init__()
        self.func = func
        self.project_path = project_path
        self.figsize = (6.4, 4.6)

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
        self.fig = plt.figure(figsize=self.figsize)  # 创建figure对象
        self.canvas = FigureCanvas(self.fig)  # 创建figure画布
        self.figtoolbar = NavigationToolbar(self.canvas, self)  # 创建figure工具栏
###############################
        container_widget = QWidget(self)

        layout = QVBoxLayout()
        container_widget.setLayout(layout)

        toolbar = QToolBar()
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

    @treat_err
    def on_resize(self):

        self.fig.tight_layout()
        # self.fig.subplots_adjust(left=0.5 )




    def closeEvent(self, event):
        event.accept()







class SyncPhaseDialog(MyPictureDialog):
    def __init__(self, project_path, func):
        super().__init__(project_path, func)
        pass


    def plot_image(self):
        self.func(self.project_path, show_=0)






class PhaseDialog(MyPictureDialog):
    def __init__(self, project_path, func, dst_path):
        super().__init__(project_path, func)
        self.dst_path = dst_path
        self.figsize=(6.4*2, 4.6*2)


    def plot_image(self):
        self.func(self.dst_path, show_=0)






class LossDialog(MyPictureDialog):
    def __init__(self, project_path, func):
        super().__init__(project_path, func)
        self.picture_name = 'loss'


    def plot_image(self, ):
        self.func(self.project_path, self.picture_name, show_=0)

class EnergyDialog(MyPictureDialog):
    def __init__(self, project_path, func):
        super().__init__(project_path, func)
        self.picture_name = 'energy'

    def plot_image(self, ):
        self.func(self.project_path, self.picture_name, show_=0)


class BeamPahseAdvanceDialog(MyPictureDialog):
    def __init__(self, project_path, func, pm):
        super().__init__(project_path, func)
        self.pm = pm

    def plot_image(self):

        self.func(self.project_path, self.pm, show_=0)
        self.canvas.draw()


class EnvelopeDialog(QDialog):
    resize_signal = pyqtSignal()  # 正确初始化自定义信号
    def __init__(self, project_path, func):
        super().__init__()
        self.func = func
        self.project_path = project_path
        self.picture_name = 'rms_x'

        self.fig_size = (6.4,4.6)


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
        self.fig = plt.figure(figsize=self.fig_size)  # 创建figure对象
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
        print(self.picture_name)
        # self.fig.clf()
        self.func(self.project_path, self.picture_name, show_=0)
        self.canvas.draw()

    def resizeEvent(self, event):
        # 当窗口被拉伸时，发出自定义信号
        self.resize_signal.emit()
        return super().resizeEvent(event)


    def on_resize(self):
        self.fig.tight_layout()
        # plt.subplots_adjust(top=0.8 )


    def closeEvent(self, event):
        event.accept()

    def contextMenuEvent(self, event):
        cmenu = QMenu(self)

        menu_items = {
            "rms_x": cmenu.addAction("rms_x"),
            "rms_y": cmenu.addAction("rms_y"),
            "rms_z": cmenu.addAction("rms_z"),
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
                self.picture_name = item_name
                break
        self.fig.clf()
        self.plot_image()





class EmittanceDialog(EnvelopeDialog):
    def __init__(self, project_path, func):
        super().__init__(project_path, func)
        self.picture_name = 'emittance_x'

    def contextMenuEvent(self, event):
        cmenu = QMenu(self)

        menu_items = {
            "emittance_x": cmenu.addAction("emittance_x"),
            "emittance_y": cmenu.addAction("emittance_y"),
            "emittance_z": cmenu.addAction("emittance_z"),
        }

        action = cmenu.exec_(self.mapToGlobal(event.pos()))

        for item_name, menu_item in menu_items.items():
            if action == menu_item:
                self.picture_name = item_name
                break

        self.fig.clf()
        self.plot_image()


class CavityVoltageDialog(QDialog):
    resize_signal = pyqtSignal()  # 正确初始化自定义信号
    def __init__(self, project_path, func):
        super().__init__()
        self.func = func
        self.project_path = project_path
        self.ratio = {}
        self.field_num = 0

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

################################
        self.fig = plt.figure(figsize=(6.4, 4.6))  # 创建figure对象
        self.canvas = FigureCanvas(self.fig)  # 创建figure画布
        self.figtoolbar = NavigationToolbar(self.canvas, self)  # 创建figure工具栏
###############################

        self.ratio_dialog = None
        container_widget = QWidget(self)

        layout = QVBoxLayout()
        container_widget.setLayout(layout)

        toolbar = QToolBar()
        layout.addWidget(toolbar)



        refresh_action = QAction('刷新', self)
        refresh_action.triggered.connect(self.refresh_trigger)
        toolbar.addAction(refresh_action)
########################################
        self.get_feld()
        vbox_field = QVBoxLayout()
        i = 0
        for k, v in self.ratio.items():
            label = QLabel(k)
            edit = QLineEdit(str(v))
            label.setObjectName(f"label_{i}")
            edit.setObjectName(f"edit_{i}")
            vbox_field.addWidget(label)
            vbox_field.addWidget(edit)
            i = i + 1

        self.field_name = i


        field_group_box = QGroupBox()
        field_layout = QVBoxLayout()
        field_layout.addLayout(vbox_field)
        field_group_box.setLayout(field_layout)



##############################################
        hbox_field_image = QHBoxLayout()
        hbox_field_image.addWidget(field_group_box)
        hbox_field_image.addWidget(self.canvas)

        field_image_group_box = QGroupBox()

        field_image_group_box.setLayout(hbox_field_image)
################################################

        layout.addWidget(self.figtoolbar)

        layout.addWidget(field_image_group_box)

        self.setLayout(layout)


    def plot_image(self):
        self.func(self.project_path, self.ratio, show_=0)
        self.canvas.draw()


    def closeEvent(self, event):
        event.accept()

    def get_feld(self):
        lattice_path = os.path.join(self.project_path, "InputFile", "lattice.txt")
        all_info = read_txt(lattice_path, out='list')

        for i in all_info:
            if i[0] == 'field' and float(i[4]) == 1:
                self.ratio[i[9]] = 1

    def refresh_trigger(self):
        label_edit_widgets = {}
        for i in range(0, self.field_name):
            label_name = f"label_{i}"
            edit_name = f"edit_{i}"

            label = self.findChild(QLabel, label_name)
            edit = self.findChild(QLineEdit, edit_name)

            if label and edit:
                label_edit_widgets[label.text()] =float(edit.text())

        # 现在 label_edit_widgets 包含了每个 label 对应的 edit
        self.ratio = label_edit_widgets
        self.plot_image()




    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.resize_signal.emit()
        return super().resizeEvent(event)

    def on_resize(self):
        self.fig.tight_layout()

#################################################################

class EnvBeamOutDialog(MyPictureDialog):

    def __init__(self, project_path, func, picture_name):
        super().__init__(project_path, func, )
        self.picture_name = picture_name

    def plot_image(self, ):
        self.func(self.project_path, self.picture_name, show_=0)

class EnvAlphaDialog(EnvelopeDialog):
    def __init__(self, project_path, func):
        super().__init__(project_path, func)
        self.picture_name = 'alpha_x'

    def contextMenuEvent(self, event):
        cmenu = QMenu(self)

        menu_items = {
            "alpha_x": cmenu.addAction("alpha_x"),
            "alpha_y": cmenu.addAction("alpha_y"),
            "alpha_z": cmenu.addAction("alpha_z"),
        }

        action = cmenu.exec_(self.mapToGlobal(event.pos()))

        for item_name, menu_item in menu_items.items():
            if action == menu_item:
                self.picture_name = item_name
                break
        self.fig.clf()
        self.plot_image()

class EnvBetaTwissDialog(EnvelopeDialog):
    def __init__(self, project_path, func):
        super().__init__(project_path, func)
        self.picture_name = 'beta_x'

    def contextMenuEvent(self, event):
        cmenu = QMenu(self)

        menu_items = {
            "beta_x": cmenu.addAction("beta_x"),
            "beta_y": cmenu.addAction("beta_y"),
            "beta_z": cmenu.addAction("beta_z"),
        }

        action = cmenu.exec_(self.mapToGlobal(event.pos()))

        for item_name, menu_item in menu_items.items():
            if action == menu_item:
                self.picture_name = item_name
                break

        self.fig.clf()
        self.plot_image()
class EnvEmitDialog(EnvelopeDialog):
    def __init__(self, project_path, func):
        super().__init__(project_path, func)
        self.picture_name = 'emit_x'

    def contextMenuEvent(self, event):
        cmenu = QMenu(self)

        menu_items = {
            "emit_x": cmenu.addAction("emit_x"),
            "emit_y": cmenu.addAction("emit_y"),
            "emit_z": cmenu.addAction("emit_z"),
        }

        action = cmenu.exec_(self.mapToGlobal(event.pos()))

        for item_name, menu_item in menu_items.items():
            if action == menu_item:
                self.picture_name = item_name
                break

        self.fig.clf()
        self.plot_image()
class PageAnalysis(QWidget):
    def __init__(self, project_path):
        super().__init__()
        self.project_path = project_path
        self.lattice_path = self.project_path + r"\inputFile" + r'\lattice.txt'
        #相移meter和oeriod
        self.pahse_advance_mp = ''

        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()

        group_box = QGroupBox("Analysis")
        group_box_layout = QHBoxLayout()


##############################################

        env_picture_group_box = QGroupBox("Env")
        vbox_env = QVBoxLayout()


        self.button_env_gamma= QPushButton("Gamma")
        self.button_env_gamma.setStyleSheet("background-color: rgb(240, 240, 240); border: 1px solid black;")
        self.button_env_gamma.clicked.connect(self.env_gamma_dialog)

        self.button_env_beta= QPushButton("Beta")
        self.button_env_beta.setStyleSheet("background-color: rgb(240, 240, 240); border: 1px solid black;")
        self.button_env_beta.clicked.connect(self.env_beta_dialog)

        self.button_env_alpha= QPushButton("Alpha")
        self.button_env_alpha.setStyleSheet("background-color: rgb(240, 240, 240); border: 1px solid black;")
        self.button_env_alpha.clicked.connect(self.env_alpha_dialog)

        self.button_env_twiss_beta= QPushButton("Beta(twiss)")
        self.button_env_twiss_beta.setStyleSheet("background-color: rgb(240, 240, 240); border: 1px solid black;")
        self.button_env_twiss_beta.clicked.connect(self.env_twiss_beta_dialog)

        self.button_env_emit= QPushButton("Emittance")
        self.button_env_emit.setStyleSheet("background-color: rgb(240, 240, 240); border: 1px solid black;")
        self.button_env_emit.clicked.connect(self.env_emit_dialog)

        vbox_env.addWidget(self.button_env_gamma)
        vbox_env.addWidget(self.button_env_beta)
        vbox_env.addWidget(self.button_env_alpha)
        vbox_env.addWidget(self.button_env_twiss_beta)
        vbox_env.addWidget(self.button_env_emit)



        vbox_env.addStretch(1)
        env_picture_group_box.setLayout(vbox_env)

#############
#################################################
        vbox_phase_advance = QVBoxLayout()
        self.cb_meter = QCheckBox('Meter', self)
        self.cb_meter.stateChanged.connect(self.meter_change)

        self.cb_period = QCheckBox('Period', self)
        # self.cb_period.setChecked(True)  # 将 cb_period 设置为选中状态
        self.cb_period.stateChanged.connect(self.period_change)

        # 创建一个按钮组
        button_group = QButtonGroup(self)
        button_group.addButton(self.cb_meter)
        button_group.addButton(self.cb_period)



        vbox_phase_advance.addWidget(self.cb_meter)
        vbox_phase_advance.addWidget(self.cb_period)

        phase_advance_group_box = QGroupBox("Pha Advance")
        phase_advance_group_box.setLayout(vbox_phase_advance)


########################################################
        vbox_picture = QVBoxLayout()

        self.button_beam_pahse_advance = QPushButton("Beam pha advance")
        self.button_beam_pahse_advance.setStyleSheet("background-color: rgb(240, 240, 240); border: 1px solid black;")
        self.button_beam_pahse_advance.clicked.connect(self.beam_pahse_advance_dialog)

        self.button_sync_phase = QPushButton("Syn Phase")
        self.button_sync_phase.setStyleSheet("background-color: rgb(240, 240, 240); border: 1px solid black;")
        self.button_sync_phase.clicked.connect(self.sync_phase_dialog)  # 连接按钮的点击事件到绘图函数

        self.button_envelope = QPushButton("Envelope")
        self.button_envelope.setStyleSheet("background-color: rgb(240, 240, 240); border: 1px solid black;")
        self.button_envelope.clicked.connect(self.envelope_dialog)

        self.button_loss = QPushButton("loss")
        self.button_loss.setStyleSheet("background-color: rgb(240, 240, 240); border: 1px solid black;")
        self.button_loss.clicked.connect(self.loss_dialog)

        self.button_energy = QPushButton("Energy")
        self.button_energy.setStyleSheet("background-color: rgb(240, 240, 240); border: 1px solid black;")
        self.button_energy.clicked.connect(self.energy_dialog)

        self.button_emittance = QPushButton("Emittance")
        self.button_emittance.setStyleSheet("background-color: rgb(240, 240, 240); border: 1px solid black;")
        self.button_emittance.clicked.connect(self.emittance_dialog)

        self.button_cavity_voltage= QPushButton("cavity_voltage")
        self.button_cavity_voltage.setStyleSheet("background-color: rgb(240, 240, 240); border: 1px solid black;")
        self.button_cavity_voltage.clicked.connect(self.cavity_voltage_dialog)
        vbox_picture.addWidget(phase_advance_group_box)
        vbox_picture.addWidget(self.button_beam_pahse_advance)
        vbox_picture.addWidget(self.button_sync_phase)
        vbox_picture.addWidget(self.button_envelope)
        vbox_picture.addWidget(self.button_loss)
        vbox_picture.addWidget(self.button_energy)
        vbox_picture.addWidget(self.button_emittance)
        vbox_picture.addWidget(self.button_cavity_voltage)
        vbox_picture.addStretch(1)

        picture_group_box = QGroupBox("Mulp")
        picture_group_box.setLayout(vbox_picture)

  #######################################################################
        group_box_1 = QGroupBox()
        gb1_layout = QVBoxLayout()

        plt_to_dst_group_box = QGroupBox()
        plt_to_dst_layout = QVBoxLayout()
        label_plt_to_dst = QLabel("Convert plt to dst (num)")
        
        self.step_of_plt_line = QLineEdit("")
        self.button_convert_plt = QPushButton("convert")
        self.button_convert_plt.clicked.connect(self.convert_plt_to_dst)
        
        hbox_plt_to_dst = QHBoxLayout()
        hbox_plt_to_dst.addWidget(self.step_of_plt_line)
        hbox_plt_to_dst.addWidget(self.button_convert_plt)


        plt_to_dst_layout.addWidget(label_plt_to_dst)
        plt_to_dst_layout.addLayout(hbox_plt_to_dst)
        plt_to_dst_group_box.setLayout(plt_to_dst_layout)
####

        vbox_phase = QVBoxLayout()

        self.button_import_dst_file = QPushButton("Import dst File")
        self.button_import_dst_file.clicked.connect(self.select_dst_file)

        self.text_phase_path =QLineEdit()

        self.button_phase = QPushButton("Phase")
        self.button_phase.setStyleSheet("background-color: rgb(240, 240, 240); border: 1px solid black;")
        # self.button_phase.clicked.connect(self.phase_dialog)  # 连接按钮的点击事件到绘图函数

        vbox_phase.addWidget(self.button_import_dst_file)
        vbox_phase.addWidget(self.text_phase_path)
        vbox_phase.addWidget(self.button_phase)

        phase_group_box = QGroupBox()
        phase_group_box.setLayout(vbox_phase)

        gb1_layout.addWidget(plt_to_dst_group_box)
        gb1_layout.addWidget(phase_group_box)
        gb1_layout.addStretch(1)

        group_box_1.setLayout(gb1_layout)

################################################################

        group_box_layout.addWidget(group_box_1)
        group_box_layout.addWidget(env_picture_group_box)
        group_box_layout.addWidget(picture_group_box)


        group_box.setLayout(group_box_layout)

        layout.addWidget(group_box)
        self.setLayout(layout)



###########errr
    @treat_err
    def convert_plt_to_dst(self):
        beamset_path = os.path.join(self.project_path, "OutputFile", "BeamSet.plt")
        obj = Plttodst(beamset_path)
        obj.to_dst_variable_z(int(self.step_of_plt_line.text()))

    @treat_err
    def env_gamma_dialog(self):
        picture_name = 'gamma'
        func = plot_env_beam_out
        self.dialog = EnvBeamOutDialog(self.project_path, func, picture_name)
        self.dialog.initUI()
        self.dialog.plot_image()
        self.dialog.show()

    @treat_err
    def env_beta_dialog(self):
        picture_name = 'beta'
        func = plot_env_beam_out
        self.dialog = EnvBeamOutDialog(self.project_path, func, picture_name)
        self.dialog.initUI()
        self.dialog.plot_image()
        self.dialog.show()
    @treat_err
    def env_alpha_dialog(self):
        func = plot_env_beam_out
        self.dialog = EnvAlphaDialog(self.project_path, func)
        self.dialog.initUI()
        self.dialog.plot_image()
        self.dialog.show()

    @treat_err
    def env_twiss_beta_dialog(self):
        func = plot_env_beam_out
        self.dialog = EnvBetaTwissDialog(self.project_path, func)
        self.dialog.initUI()
        self.dialog.plot_image()
        self.dialog.show()

    @treat_err
    def env_emit_dialog(self):
        func = plot_env_beam_out
        self.dialog = EnvEmitDialog(self.project_path, func)
        self.dialog.initUI()
        self.dialog.plot_image()
        self.dialog.show()


    @treat_err
    def sync_phase_dialog(self):
        func = plot_cavity_syn_phase
        self.dialog = SyncPhaseDialog(self.project_path, func)
        self.dialog.initUI()
        self.dialog.plot_image()
        self.dialog.show()

    @treat_err
    def phase_dialog(self):
        if self.text_phase_path.text() == '':
            # print('ddd')
            return 0

        func = plot_phase
        self.phase_dialog = PhaseDialog(self.project_path, func, self.text_phase_path.text())
        self.phase_dialog.initUI()
        self.phase_dialog.plot_image()
        self.phase_dialog.show()

    @treat_err
    def loss_dialog(self ):
        func = plot_dataset

        self.loss_dialog = LossDialog(self.project_path, func)
        self.loss_dialog.initUI()
        self.loss_dialog.plot_image()
        self.loss_dialog.show()

    @treat_err
    def energy_dialog(self):

        func = plot_dataset
        self.energy_dialog = EnergyDialog(self.project_path, func)
        self.energy_dialog.initUI()
        self.energy_dialog.plot_image()
        self.energy_dialog.show()

    @treat_err
    def emittance_dialog(self):

        func = plot_dataset
        self.emittance_dialog = EmittanceDialog(self.project_path, func)
        self.emittance_dialog.initUI()
        self.emittance_dialog.plot_image()
        self.emittance_dialog.show()

    @treat_err
    def cavity_voltage_dialog(self):
        func = plot_cavity_voltage
        self.cavity_voltage_dialog = CavityVoltageDialog(self.project_path, func)
        self.cavity_voltage_dialog.initUI()
        self.cavity_voltage_dialog.plot_image()
        self.cavity_voltage_dialog.show()

    @treat_err
    def envelope_dialog(self):

        func = plot_dataset
        self.envelope_dialog = EnvelopeDialog(self.project_path, func)
        self.envelope_dialog.fig_size = (12.8, 6.4)
        self.envelope_dialog.initUI()
        self.envelope_dialog.show()

    def updatePath(self, new_path):
        self.project_path = new_path

    def meter_change(self, state):

        if state == Qt.Checked:
            self.pahse_advance_mp = 'Meter'


    def period_change(self, state):
        if state == Qt.Checked:
            self.pahse_advance_mp = 'Period'


    @treat_err
    def beam_pahse_advance_dialog(self):
        func = plot_phase_advance

        self.cavity_voltage_dialog = BeamPahseAdvanceDialog(self.project_path, func, self.pahse_advance_mp)
        self.cavity_voltage_dialog.initUI()
        self.cavity_voltage_dialog.plot_image()
        self.cavity_voltage_dialog.show()

    def select_dst_file(self):

        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        dst_file_path, _ = QFileDialog.getOpenFileName(self, "Select dst File", options=options)

        if dst_file_path:
            # print(dst_file_path)
            self.text_phase_path.setText(dst_file_path)





if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = PageAnalysis(r'C:\Users\anxin\Desktop\test2')
    main_window.setGeometry(800, 500, 600, 650)
    main_window.setStyleSheet("background-color: rgb(253, 253, 253);")
    main_window.show()
    sys.exit(app.exec_())


    # app = QApplication(sys.argv)
    # main_window = CavityVoltageDialog(r'C:\Users\anxin\Desktop\00000', plot_cavity_voltage )
    # main_window.initUI()
    # main_window.setGeometry(800, 500, 600, 650)
    # main_window.setStyleSheet("background-color: rgb(253, 253, 253);")
    # main_window.show()
    # sys.exit(app.exec_())