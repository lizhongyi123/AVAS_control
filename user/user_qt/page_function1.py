import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QToolBar, QVBoxLayout, QWidget, QPushButton, \
    QStackedWidget, QMenu, QLabel, QLineEdit, QTextEdit, QGridLayout, QHBoxLayout, QFrame, QFileDialog, QGroupBox, \
    QComboBox, QSizePolicy, QCheckBox, QButtonGroup, QTreeWidget, QTreeWidgetItem, QSpacerItem, QSizePolicy

import os

from PyQt5.QtCore import QStandardPaths, QCoreApplication, pyqtSignal, QTimer

from PyQt5.QtCore import Qt

from api import AVAS_simulation, match_twiss, change_particle_number, circle_match
import multiprocessing


class PageFunction(QWidget):
    run_choose = pyqtSignal(str)

    def __init__(self, project_path):
        super().__init__()
        self.project_path = project_path
        self.match_choose = ''
        self.use_initial_value = 0
        self.initUI()

    def initUI(self):
        # print(self.project_path)
        self.setStyleSheet("background-color: rgb(250, 250, 250);")

        layout = QHBoxLayout()

        # 创建一个垂直组合框
        vertical_group_box_main = QGroupBox("Function")

        vertical_layout_main = QVBoxLayout()
        ##########################################################################

        group_box_simulation = QGroupBox()

        hbox_simulation = QHBoxLayout()

        self.button_simulation = QPushButton("Simualation")
        self.button_simulation.clicked.connect(self.func_simulation)

        self.button_stop_simulation = QPushButton("Stop simualation")
        self.button_stop_simulation.clicked.connect(self.func_stop_simulation)

        hbox_simulation.addWidget(self.button_simulation)
        hbox_simulation.addWidget(self.button_stop_simulation)

        group_box_simulation.setLayout(hbox_simulation)

        ##########################################################################

        group_box_match = QGroupBox()
        group_box_match.setFixedHeight(200)  # 设置高度为200像素
        hbox_match = QHBoxLayout()

        group_box_match_1 = QGroupBox()
        hbox_match_1 = QVBoxLayout()
        self.button_match = QPushButton("Match")
        self.button_match.clicked.connect(self.func_match)

        self.button_stop_match = QPushButton("Stop match")
        self.button_stop_match.clicked.connect(self.func_stop_match)

        hbox_match_1.addWidget(self.button_match)
        hbox_match_1.addWidget(self.button_stop_match)
        group_box_match_1.setLayout(hbox_match_1)

        group_box_match_2 = QGroupBox()
        hbox_match_2 = QVBoxLayout()

        self.cb_input_twiss = QCheckBox('Calculate input twiss parameter', self)
        self.cb_input_twiss.stateChanged.connect(self.input_twiss_change)

        self.cb_match_twiss = QCheckBox('Match with twiss command', self)

        self.cb_match_twiss.stateChanged.connect(self.match_twiss_change)

        # 创建一个包装布局
        wrapper_layout = QHBoxLayout()

        self.cb_use_initial_value = QCheckBox('Use initial value')
        self.cb_use_initial_value.stateChanged.connect(self.cb_use_initial_value_change)

        # 添加一个占位符小部件到包装布局以增加左边距
        spacer = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        wrapper_layout.addItem(spacer)

        wrapper_layout.addWidget(self.cb_use_initial_value)
        # self.cb_use_initial_value.setVisible(False)

        # 创建一个按钮组
        button_group_match = QButtonGroup(self)
        button_group_match.addButton(self.cb_input_twiss)
        button_group_match.addButton(self.cb_match_twiss)

        # 添加包装布局到 hbox_match_2 布局
        hbox_match_2.addWidget(self.cb_input_twiss)
        hbox_match_2.addStretch(1)
        hbox_match_2.addWidget(self.cb_match_twiss)
        hbox_match_2.addStretch(1)
        hbox_match_2.addLayout(wrapper_layout)

        group_box_match_2.setLayout(hbox_match_2)

        hbox_match.addWidget(group_box_match_1)
        hbox_match.addWidget(group_box_match_2)

        group_box_match.setLayout(hbox_match)
        self.cb_use_initial_value.setEnabled(False)

        ##########################################################################

        ##########################################################
        group_box_change_number = QGroupBox()
        hbox_change_number = QHBoxLayout()

        ######################################
        button_change_number = QPushButton("change Number")
        button_stop_change = QPushButton("Stop")

        button_change_number.clicked.connect(self.func_change)
        button_stop_change.clicked.connect(self.func_stop_change)
        group_box_change = QGroupBox()
        vbox_chang = QVBoxLayout()
        vbox_chang.addWidget(button_change_number)
        vbox_chang.addWidget(button_stop_change)
        group_box_change.setLayout(vbox_chang)

        #############################
        button_dst_path = QPushButton("Import dst file")
        button_dst_path.clicked.connect(self.select_dst_file)

        self.text_phase_path = QLineEdit()

        label_change_number = QLabel("Particle number expansion multiple")
        self.text_change_number = QLineEdit()

        group_box_change_info = QGroupBox()
        vbox_change_info = QVBoxLayout()

        vbox_change_info.addWidget(button_dst_path)
        vbox_change_info.addWidget(self.text_phase_path)

        vbox_change_info.addWidget(label_change_number)
        vbox_change_info.addWidget(self.text_change_number)

        group_box_change_info.setLayout(vbox_change_info)

        #########################################################

        hbox_change_number.addWidget(group_box_change)
        hbox_change_number.addWidget(group_box_change_info)

        group_box_change_number.setLayout(hbox_change_number)

        ########################################################
        vertical_layout_main.addWidget(group_box_simulation)
        vertical_layout_main.addWidget(group_box_match)
        vertical_layout_main.addWidget(group_box_change_number)

        vertical_group_box_main.setLayout(vertical_layout_main)
        #########################################################################################

        layout.addWidget(vertical_group_box_main)

        self.setLayout(layout)

        self.simulation_process = None
        self.match_process = None
        self.change_num_process = None

        # 创建一个定时器，每隔一段时间检查self.match_process的状态
        self.match_timer = QTimer(self)
        self.match_timer.timeout.connect(self.check_match_process_status)

        self.simulation_timer = QTimer(self)
        self.simulation_timer.timeout.connect(self.check_simulation_process_status)

    def updatePath(self, new_path):
        self.project_path = new_path

    def refreshUI(self):
        self.initUI()  # Call initUI to refresh the UI

    def func_simulation(self):
        print("start simulation")
        if self.simulation_process is None or not self.simulation_process.is_alive():
            self.simulation_process = multiprocessing.Process(target=AVAS_simulation, args=(self.project_path,))
            self.simulation_process.start()

            self.simulation_timer.start(1000)  # 1秒检查一次

    def check_simulation_process_status(self):
        if self.simulation_process is not None:
            if self.simulation_process.is_alive():
                # 进程仍在运行
                self.button_simulation.setEnabled(False)  # 禁用按钮
            else:
                # 进程已结束
                self.button_simulation.setEnabled(True)  # 启用按钮
                # 停止监测器
                self.simulation_timer.stop()

    def func_stop_simulation(self):
        if self.simulation_process is not None and self.simulation_process.is_alive():
            self.simulation_process.terminate()
            self.simulation_process.join()

        print("stop simulation")

    def func_match(self):
        print(self.match_choose)
        print("start match")
        if self.match_process is None or not self.match_process.is_alive():

            if self.match_choose == 0:
                # 周期匹配
                target = circle_match
                args = (self.project_path,)


            elif self.match_choose == 1:
                # twiss command匹配
                target = match_twiss
                print(self.use_initial_value)
                args = (self.project_path, self.use_initial_value)
            else:
                return 0

            self.match_process = multiprocessing.Process(target=target, args=args)
            self.match_process.start()
            # 启用监测器，开始检查进程状态
            self.match_timer.start(1000)  # 1秒检查一次

    def check_match_process_status(self):
        if self.match_process is not None:
            if self.match_process.is_alive():
                # 进程仍在运行
                self.button_match.setEnabled(False)  # 禁用按钮
            else:
                # 进程已结束
                self.button_match.setEnabled(True)  # 启用按钮
                # 停止监测器
                self.match_timer.stop()

    def func_stop_match(self):
        if self.match_process is not None and self.match_process.is_alive():
            self.match_process.terminate()
            self.match_process.join()
        print('stop match')
        # 重新启用按钮
        self.button_match.setEnabled(True)
        print('stop match')

    def select_dst_file(self):
        # desktop_path = QStandardPaths.writableLocation(QStandardPaths.DesktopLocation)
        # default_folder_path = desktop_path
        #
        # folder_path, _ = QFileDialog.getOpenFileName(self, "Create New Folder", default_folder_path,
        #                                                  filter="Folders (*)")
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        dst_file_path, _ = QFileDialog.getOpenFileName(self, "Select dst File", options=options)

        if dst_file_path:
            # print(dst_file_path)
            self.text_phase_path.setText(dst_file_path)

    def func_change(self, ):
        infile_path = self.text_phase_path.text()
        if infile_path == '':
            return 0

        print('start change')
        outfile_path = os.path.join(self.project_path, 'OutputFile', 'change_num_result.dst')
        ratio = int(self.text_change_number.text())
        if self.change_num_process is None or not self.change_num_process.is_alive():
            self.change_num_process = multiprocessing.Process(target=change_particle_number,
                                                              args=(infile_path, outfile_path, ratio,))
            self.change_num_process.start()

    def func_stop_change(self):
        if self.change_num_process is not None and self.change_num_process.is_alive():
            self.change_num_process.terminate()
            self.change_num_process.join()

        print('stop change')

    def input_twiss_change(self, state):

        if state == Qt.Checked:
            self.match_choose = 0

    def match_twiss_change(self, state):
        if state == Qt.Checked:
            self.match_choose = 1

        if state == Qt.Checked:
            self.cb_use_initial_value.setEnabled(True)
        else:
            self.cb_use_initial_value.setEnabled(False)

    def cb_use_initial_value_change(self, state):
        if state == Qt.Checked:
            self.use_initial_value = 1


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     main_window = PageFunction(r'C:\Users\anxin\Desktop\00000')
#     main_window.setGeometry(800, 500, 600, 650)
#     main_window.setStyleSheet("background-color: rgb(253, 253, 253);")
#     main_window.show()
#     sys.exit(app.exec_())