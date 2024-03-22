import sys
# sys.path.append(r'C:\Users\anxin\Desktop\AVAS_control')

import time

from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QToolBar, QVBoxLayout, QWidget, QPushButton, \
    QStackedWidget, QMenu, QLabel, QLineEdit, QTextEdit,  QGridLayout, QHBoxLayout,  QFrame, QFileDialog, QGroupBox, \
    QComboBox, QSizePolicy, QDialog, QCheckBox, QButtonGroup, QMessageBox

from PyQt5.QtCore import Qt, QSize
from api import plot_cavity_syn_phase, plot_dataset,  plot_cavity_voltage,\
     plot_phase, plot_phase_advance, plot_error
from user.user_qt.user_defined import treat_err
from user.user_qt.page_analysis import MyPictureDialog, EnvelopeDialog



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
########################################################

class PageError(QWidget):
    def __init__(self, project_path):
        super().__init__()
        self.project_path = project_path
        self.lattice_path = self.project_path + r"\inputFile" + r'\lattice.txt'
        #相移meter和oeriod
        self.pahse_advance_mp = ''
        self.plot_error_type = 'average'

        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()

        group_box = QGroupBox("Analysis")
        group_box_layout = QHBoxLayout()


##############################################

        err_group_box = QGroupBox("Error")
        vbox_error = QVBoxLayout()
#####################################################
        err_type_group_box = QGroupBox()
        err_type_layout = QVBoxLayout()
        self.cb_average = QCheckBox('average', self)
        self.cb_average.stateChanged.connect(self.cb_average_change)

        self.cb_rms = QCheckBox('rms', self)
        # self.cb_period.setChecked(True)  # 将 cb_period 设置为选中状态
        self.cb_rms.stateChanged.connect(self.cb_rms_change)

        # 创建一个按钮组
        button_group_1 = QButtonGroup(self)
        button_group_1.addButton(self.cb_average)
        button_group_1.addButton(self.cb_rms)

        err_type_layout.addWidget(self.cb_average)
        err_type_layout.addWidget(self.cb_rms)

        err_type_group_box.setLayout(err_type_layout)
#######################################################

        err_picture_group_box = QGroupBox()
        err_picture_layout = QVBoxLayout()



        self.button_error_ek = QPushButton("Energy")
        self.button_error_ek.setStyleSheet("background-color: rgb(240, 240, 240); border: 1px solid black;")
        self.button_error_ek.clicked.connect(self.error_ek_dialog)

        self.button_error_envelope = QPushButton("Envelope")
        self.button_error_envelope.setStyleSheet("background-color: rgb(240, 240, 240); border: 1px solid black;")
        self.button_error_envelope.clicked.connect(self.error_envelope_dialog)


        err_picture_layout.addWidget(self.button_error_ek)
        err_picture_layout.addWidget(self.button_error_envelope)

        err_picture_group_box.setLayout(err_picture_layout)


        vbox_error.addWidget(err_type_group_box)
        vbox_error.addWidget(err_picture_group_box)
        vbox_error.addStretch(1)
        err_group_box.setLayout(vbox_error)
#############
#################################################

        group_box_layout.addWidget(err_group_box)


        group_box.setLayout(group_box_layout)

        layout.addWidget(group_box)
        self.setLayout(layout)


    @treat_err
###########errr
    def error_ek_dialog(self):

        func = plot_error
        self.dialog = ErrorEnergyDialog(self.project_path, func, self.plot_error_type)
        self.dialog.initUI()
        self.dialog.plot_image()
        self.dialog.show()

    @treat_err
    def error_envelope_dialog(self, ):
        func = plot_error
        self.dialog = ErrorEnvelopeDialog(self.project_path, func, self.plot_error_type)
        self.dialog.initUI()
        self.dialog.show()


    def cb_average_change(self, state):
        if state == Qt.Checked:
            self.plot_error_type = 'average'


    def cb_rms_change(self, state):
        if state == Qt.Checked:
            self.plot_error_type = 'rms'
            
    def updatePath(self, new_path):
        self.project_path = new_path


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     main_window = PageError(r'C:\Users\anxin\Desktop\test')
#     main_window.setGeometry(800, 500, 600, 650)
#     main_window.setStyleSheet("background-color: rgb(253, 253, 253);")
#     main_window.show()
#     sys.exit(app.exec_())


    # app = QApplication(sys.argv)
    # main_window = CavityVoltageDialog(r'C:\Users\anxin\Desktop\00000', plot_cavity_voltage )
    # main_window.initUI()
    # main_window.setGeometry(800, 500, 600, 650)
    # main_window.setStyleSheet("background-color: rgb(253, 253, 253);")
    # main_window.show()
    # sys.exit(app.exec_())