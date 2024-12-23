import os.path
import sys
# sys.path.append(r'C:\Users\anxin\Desktop\AVAS_control')

import time

from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QToolBar, QVBoxLayout, QWidget, QPushButton, \
    QStackedWidget, QMenu, QLabel, QLineEdit, QTextEdit, QGridLayout, QHBoxLayout, QFrame, QFileDialog, QGroupBox, \
    QComboBox, QSizePolicy, QDialog, QCheckBox, QButtonGroup, QMessageBox

from PyQt5.QtCore import Qt, QSize, pyqtSignal
from api import plot_error_out, plot_error_emit_loss
from user.user_qt.user_defined import treat_err
from user.user_qt.page_analysis import MyPictureDialog, EnvelopeDialog
from user.user_qt.page_utils.picture_dialog import PictureDialog1

from user.user_qt.user_defined import MyQLineEdit
from utils.iniconfig import IniConfig
class ErrorEnergyDialog(MyPictureDialog):
    def __init__(self, project_path, func, picture_type):
        super().__init__(project_path, func, )
        self.picture_name = 'energy'
        self.picture_type = picture_type

    def plot_image(self, ):
        self.func(self.project_path, self.picture_name, self.picture_type, show_=0)


class ErrorEnvelopeDialog(EnvelopeDialog):
    def __init__(self, project_path, func, picture_type):
        super().__init__(project_path, func)
        self.picture_name = 'x'
        self.picture_type = picture_type

    def contextMenuEvent(self, event):
        cmenu = QMenu(self)

        menu_items = {
            "x": cmenu.addAction("x"),
            "y": cmenu.addAction("y"),
            "rms_x": cmenu.addAction("rms_x"),
            "rms_y": cmenu.addAction("rms_y"),
        }

        action = cmenu.exec_(self.mapToGlobal(event.pos()))

        for item_name, menu_item in menu_items.items():
            if action == menu_item:
                self.picture_name = item_name
                break
        self.fig.clf()
        self.plot_image()

    def plot_image(self):
        print(self.picture_name)
        self.func(self.project_path, self.picture_name, self.picture_type, show_=0)
        self.canvas.draw()


class EmitLossDialog(PictureDialog1):
    def __init__(self, project_path, func, picture_type):
        super().__init__(project_path, func, )
        self.picture_type = picture_type

    def plot_image(self, ):
        self.func(self.project_path, self.picture_type, 0, self.fig)


class Plotoutput(PictureDialog1):
    def __init__(self, project_path, func, picture_type):
        super().__init__(project_path, func, )
        self.picture_type = picture_type

    def plot_image(self, ):
        self.func(self.project_path, self.picture_type, show_=0, )



########################################################

class PageError(QWidget):
    error_signal = pyqtSignal(dict)
    def __init__(self, project_path):
        super().__init__()
        self.project_path = project_path
        self.lattice_path = self.project_path + r"\inputFile" + r'\lattice.txt'

        # 相移meter和oeriod
        self.pahse_advance_mp = ''
        self.output_plot_type = 'average'

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        group_box = QGroupBox("")
        group_box_layout = QVBoxLayout()

        ##############################################

        err_type_group_box = QGroupBox("")
        hbox_error_type = QHBoxLayout()

        self.cb_stat_error = QCheckBox("Static error")
        self.cb_stat_error.stateChanged.connect(self.cb_error_change)

        self.cb_dyn_error = QCheckBox("Dynamic error")
        self.cb_dyn_error.stateChanged.connect(self.cb_error_change)

        self.cb_stat_dyn_error = QCheckBox("Static error & Dynamic error")
        self.cb_stat_dyn_error.stateChanged.connect(self.cb_error_change)

        hbox_error_type.addWidget(self.cb_stat_error)
        hbox_error_type.addWidget(self.cb_dyn_error)
        hbox_error_type.addWidget(self.cb_stat_dyn_error)

        err_type_group_box.setLayout(hbox_error_type)
        ##############################################
        group_box_seed = QGroupBox("")
        layout_seed = QHBoxLayout()
        label_seed = QLabel("seed")
        label_seed.setFixedSize(180, 12)  # 设置宽度和高度
        # label_charge.setAlignment(Qt.AlignCenter)  # 设置水平和垂直居中

        self.text_seed = MyQLineEdit("50")

        self.text_seed.textChanged.connect(self.text_seed_change)

        layout_seed.addWidget(label_seed)
        layout_seed.addWidget(self.text_seed)
        group_box_seed.setLayout(layout_seed)

        ##############################################
        group_box_output = QGroupBox("")
        layout1 = QVBoxLayout()

        layout10 = QHBoxLayout()
        self.button_select_error_par = QPushButton(QApplication.style().standardIcon(32),"")
        self.button_select_error_par.clicked.connect(self.select_error_par)
        self.text_error_par  = MyQLineEdit(" ")

        layout10.addWidget(self.button_select_error_par)
        layout10.addWidget(self.text_error_par)



        layout11 = QHBoxLayout()
        self.button_emit_loss = QPushButton("Emit growth && Loss")
        self.button_emit_loss.clicked.connect(self.plot_error_emit_loss_this)

        self.cb_average = QCheckBox('average', self)
        self.cb_average.stateChanged.connect(self.cb_average_change)

        self.cb_rms = QCheckBox('rms', self)
        # self.cb_period.setChecked(True)  # 将 cb_period 设置为选中状态
        self.cb_rms.stateChanged.connect(self.cb_rms_change)

        # 创建一个按钮组
        button_group_1 = QButtonGroup(self)
        button_group_1.addButton(self.cb_average)
        button_group_1.addButton(self.cb_rms)

        layout11.addWidget(self.button_emit_loss)
        layout11.addWidget(self.cb_average)
        layout11.addWidget(self.cb_rms)

        layout12 = QHBoxLayout()
        self.button_output_xy = QPushButton("X && Y")
        self.button_output_xy.clicked.connect(self.plot_output_xy)

        self.button_output_x1y1 = QPushButton("X' && Y'")
        self.button_output_x1y1.clicked.connect(self.plot_output_x1y1)

        self.button_output_rmsxy = QPushButton("rms(X) && rms(Y)")
        self.button_output_rmsxy.clicked.connect(self.plot_output_rmsxy)

        self.button_output_rmsx1y1 = QPushButton("rms(X') && rms(Y')")
        self.button_output_rmsx1y1.clicked.connect(self.plot_output_rmsx1y1)

        self.button_output_energy_change = QPushButton("Energy change")
        self.button_output_energy_change.clicked.connect(self.plot_output_energy_change)


        layout12.addWidget(self.button_output_xy)
        layout12.addWidget(self.button_output_x1y1)
        layout12.addWidget(self.button_output_rmsxy)
        layout12.addWidget(self.button_output_rmsx1y1)
        layout12.addWidget(self.button_output_energy_change)

        layout1.addLayout(layout10)
        layout1.addLayout(layout11)
        layout1.addLayout(layout12)

        group_box_output.setLayout(layout1)

        #######################################################

        # picture_type_group_box = QGroupBox()
        # picture_type_layout = QVBoxLayout()
        #
        # self.button_error_ek = QPushButton("Energy")
        # self.button_error_ek.setStyleSheet("background-color: rgb(240, 240, 240); border: 1px solid black;")
        # self.button_error_ek.clicked.connect(self.error_ek_dialog)
        #
        # self.button_error_envelope = QPushButton("Envelope")
        # self.button_error_envelope.setStyleSheet("background-color: rgb(240, 240, 240); border: 1px solid black;")
        # self.button_error_envelope.clicked.connect(self.error_envelope_dialog)
        #
        # picture_type_layout.addWidget(self.button_error_ek)
        # picture_type_layout.addWidget(self.button_error_envelope)
        #
        # picture_type_group_box.setLayout(picture_type_layout)
        #
        # picture_layout.addWidget(picture_ar_group_box)
        # picture_layout.addWidget(picture_type_group_box)
        # picture_group_box.setLayout(picture_layout)
        #############
        #################################################
        group_box_layout.addWidget(err_type_group_box)
        group_box_layout.addWidget(group_box_seed)
        group_box_layout.addWidget(group_box_output)


        group_box_layout.addStretch(1)

        group_box.setLayout(group_box_layout)

        layout.addWidget(group_box)
        self.setLayout(layout)

    # @treat_err
    # ###########errr
    # def error_ek_dialog(self):
    #     func = plot_error
    #     self.dialog = ErrorEnergyDialog(self.project_path, func, self.plot_error_type)
    #     self.dialog.initUI()
    #     self.dialog.plot_image()
    #     self.dialog.show()
    #
    # @treat_err
    # def error_envelope_dialog(self, ):
    #     func = plot_error
    #     self.dialog = ErrorEnvelopeDialog(self.project_path, func, self.plot_error_type)
    #     self.dialog.initUI()
    #     self.dialog.show()

    @treat_err
    def plot_error_emit_loss_this(self, ):
        func = plot_error_emit_loss
        self.dialog = EmitLossDialog(self.project_path, func, 'par')

        self.dialog.initUI()
        self.dialog.plot_image()
        self.dialog.show()


    def text_seed_change(self):
        if self.text_seed.text():
            seed_value = int(self.text_seed.text())
        else:
            seed_value = 0

        error_dic = self.get_state_dict()
        self.error_signal.emit(error_dic)




    @treat_err
    def plot_output_xy(self, ):
        func = plot_error_out
        if self.output_plot_type == 'average':
            picture_type = 'av_xy'
        elif self.output_plot_type == 'rms':
            picture_type = 'rms_xy'

        self.xy_dialog = Plotoutput(self.project_path, func, picture_type)

        self.xy_dialog.initUI()
        self.xy_dialog.plot_image()
        self.xy_dialog.show()

    @treat_err
    def plot_output_x1y1(self, ):
        func = plot_error_out
        if self.output_plot_type == 'average':
            picture_type = 'av_x1y1'
        elif self.output_plot_type == 'rms':
            picture_type = 'rms_x1y1'
        self.x1y1_dialog = Plotoutput(self.project_path, func, picture_type)

        self.x1y1_dialog.initUI()
        self.x1y1_dialog.plot_image()
        self.x1y1_dialog.show()

    @treat_err

    def plot_output_rmsxy(self, ):
        func = plot_error_out
        if self.output_plot_type == 'average':
            picture_type = 'av_rms_xy'
        elif self.output_plot_type == 'rms':
            picture_type = 'rms_rms_xy'
        self.rms_xy_dialog = Plotoutput(self.project_path, func, picture_type)

        self.rms_xy_dialog.initUI()
        self.rms_xy_dialog.plot_image()
        self.rms_xy_dialog.show()

    @treat_err

    def plot_output_rmsx1y1(self, ):
        func = plot_error_out
        if self.output_plot_type == 'average':
            picture_type = 'av_rms_x1y1'
        elif self.output_plot_type == 'rms':
            picture_type = 'rms_rms_x1y1'
        self.rms_x1y1_dialog = Plotoutput(self.project_path, func, picture_type)

        self.rms_x1y1_dialog.initUI()
        self.rms_x1y1_dialog.plot_image()
        self.rms_x1y1_dialog.show()


    @treat_err

    def plot_output_energy_change(self, ):
        func = plot_error_out
        if self.output_plot_type == 'average':
            picture_type = 'av_ek'
        elif self.output_plot_type == 'rms':
            picture_type = 'rms_ek'
        self.ek_dialog = Plotoutput(self.project_path, func, picture_type)

        self.ek_dialog.initUI()
        self.ek_dialog.plot_image()
        self.ek_dialog.show()

    def cb_average_change(self, state):
        if state == Qt.Checked:
            self.output_plot_type = 'average'

    def cb_rms_change(self, state):
        if state == Qt.Checked:
            self.output_plot_type = 'rms'

    def updatePath(self, new_path):
        self.project_path = new_path
        self.ini_path = os.path.join(self.project_path, "InputFile", 'ini.ini')
        self.ini_obj = IniConfig()

    def cb_error_change(self, state):
        sender_checkbox = self.sender()  # 获取发送信号的复选框对象

        if sender_checkbox == self.cb_stat_error:
            if sender_checkbox.isChecked():
                self.cb_dyn_error.setChecked(False)
                self.cb_stat_dyn_error.setChecked(False)

        elif sender_checkbox == self.cb_dyn_error:
            if sender_checkbox.isChecked():
                self.cb_stat_error.setChecked(False)
                self.cb_stat_dyn_error.setChecked(False)

        elif sender_checkbox == self.cb_stat_dyn_error:
            if sender_checkbox.isChecked():
                self.cb_stat_error.setChecked(False)
                self.cb_dyn_error.setChecked(False)


        error_dic = self.get_state_dict()
        self.error_signal.emit(error_dic)



    def fill_parameter(self):
        item = {"projectPath": self.project_path}
        ini_dict = self.ini_obj.create_from_file(item)
        print(380, ini_dict)
        if ini_dict['code'] == -1:
            raise Exception(ini_dict['data']['msg'])

        ini_dict = ini_dict["data"]['iniParams']

        if ini_dict['error']['error_type'] == 'stat':
            self.cb_stat_error.setChecked(True)
        elif ini_dict['error']['error_type'] == 'dyn':
            self.cb_dyn_error.setChecked(True)
        elif ini_dict['error']['error_type'] == 'stat_dyn':
            self.cb_stat_error.setChecked(True)

        self.text_seed.setText(str(ini_dict['error']['seed']))

    def get_state_dict(self):
        dic = {"error_type": "undefined", "seed": 0, "if_normal": 1}
        if self.cb_stat_error.isChecked():
            dic['error_type'] = 'stat'
        elif self.cb_dyn_error.isChecked():
            dic['error_type'] = 'dyn'
        elif self.cb_stat_dyn_error.isChecked():
            dic['error_type'] = 'stat_dyn'
        else:
            dic['error_type'] = "undefined"

        dic["seed"] = int(self.text_seed.text())
        return dic
    def select_error_par(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        default_directory = os.path.join(self.project_path, "OutputFile")
        error_par_path, _ = QFileDialog.getOpenFileName(self, "Select dst File", directory=default_directory,
                                                       options=options)

        if error_par_path:
            self.text_error_par.setText(error_par_path)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = PageError(r'C:\Users\shliu\Desktop\test_new_avas\test913')
    main_window.setGeometry(800, 500, 600, 650)
    main_window.setStyleSheet("background-color: rgb(253, 253, 253);")
    main_window.show()
    main_window.updatePath(r'C:\Users\shliu\Desktop\test_avas_qt\avaserr2')
    sys.exit(app.exec_())


# app = QApplication(sys.argv)
# main_window = CavityVoltageDialog(r'C:\Users\anxin\Desktop\00000', plot_cavity_voltage )
# main_window.initUI()
# main_window.setGeometry(800, 500, 600, 650)
# main_window.setStyleSheet("background-color: rgb(253, 253, 253);")
# main_window.show()
# sys.exit(app.exec_())