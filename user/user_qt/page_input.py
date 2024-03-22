import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QToolBar, QVBoxLayout, QWidget, QPushButton, \
    QStackedWidget, QMenu, QLabel, QLineEdit, QTextEdit, QGridLayout, QHBoxLayout, QFrame, QFileDialog, QGroupBox, \
    QComboBox, QSizePolicy, QCheckBox, QMessageBox

import os

from PyQt5.QtCore import Qt, pyqtSignal
from utils.readfile import read_txt, read_dst
from user.user_qt.user_defined import treat_err, treat_err2, gray240


class PageInput(QWidget):
    basic_signal = pyqtSignal(str)

    def __init__(self, project_path):
        super().__init__()
        self.project_path = project_path
        self.multithreading_num = -1

        self.initUI()

    def initUI(self):
        # print(self.project_path)
        self.setStyleSheet("background-color: rgb(250, 250, 250);")

        layout = QHBoxLayout()

        # 创建一个垂直组合框
        vertical_group_box_main = QGroupBox("Operation setting")

        vertical_layout_main = QVBoxLayout()
##########################################################################
        group_box_mulp_env = QGroupBox()

        hbox_mulp_env = QHBoxLayout()

        self.cb_mulp = QCheckBox('Multi_particles', self)
        self.cb_mulp.stateChanged.connect(self.cb_basic_change)

        self.cb_env = QCheckBox('Envelope', self)
        self.cb_env.stateChanged.connect(self.cb_basic_change)



        hbox_mulp_env.addWidget(self.cb_mulp)
        hbox_mulp_env.addWidget(self.cb_env)

        group_box_mulp_env.setLayout(hbox_mulp_env)


##########################################################
        group_box_sc_method = QGroupBox()
        sc_method_layout = QVBoxLayout()

###############fft
        fft_layout = QHBoxLayout()

        self.cb_fft = QCheckBox('FFT', self)
        self.cb_fft.setFixedWidth(70)

        fft_grid_layout = QVBoxLayout()
        
        fft_numofgrid_layout = QHBoxLayout()
        fft_numofgrid_label = QLabel("Numofgrid")
        fft_numofgrid_label.setMinimumWidth(84)
        self.fft_numofgrid_x_text = QLineEdit('64')
        self.fft_numofgrid_y_text = QLineEdit('64')
        self.fft_numofgrid_z_text = QLineEdit('64')

        fft_numofgrid_layout.addWidget(fft_numofgrid_label)
        fft_numofgrid_layout.addWidget(self.fft_numofgrid_x_text)
        fft_numofgrid_layout.addWidget(self.fft_numofgrid_y_text)
        fft_numofgrid_layout.addWidget(self.fft_numofgrid_z_text)


        #############
        fft_meshrms_layout = QHBoxLayout()
        fft_meshrms_label = QLabel("MeshRms")
        fft_meshrms_label.setMinimumWidth(84)
        self.fft_meshrms_x_text = QLineEdit('6.5')
        self.fft_meshrms_y_text = QLineEdit('6.5')
        self.fft_meshrms_z_text = QLineEdit('6.5')

        fft_meshrms_layout.addWidget(fft_meshrms_label)
        fft_meshrms_layout.addWidget(self.fft_meshrms_x_text)
        fft_meshrms_layout.addWidget(self.fft_meshrms_y_text)
        fft_meshrms_layout.addWidget(self.fft_meshrms_z_text)


        fft_grid_layout.addLayout(fft_numofgrid_layout)
        fft_grid_layout.addLayout(fft_meshrms_layout)
        
        fft_layout.addWidget(self.cb_fft)
        fft_layout.addLayout(fft_grid_layout)
########################
        picnic_layout = QHBoxLayout()

        self.cb_picnic = QCheckBox('PICNIC', self)
        self.cb_picnic.setFixedWidth(70)
        picnic_grid_layout = QVBoxLayout()

        picnic_numofgrid_layout = QHBoxLayout()
        picnic_numofgrid_label = QLabel("Numofgrid")
        picnic_numofgrid_label.setMinimumWidth(84)
        self.picnic_numofgrid_x_text = QLineEdit("18")
        self.picnic_numofgrid_y_text = QLineEdit("18")
        self.picnic_numofgrid_z_text = QLineEdit("18")

        picnic_numofgrid_layout.addWidget(picnic_numofgrid_label)
        picnic_numofgrid_layout.addWidget(self.picnic_numofgrid_x_text)
        picnic_numofgrid_layout.addWidget(self.picnic_numofgrid_y_text)
        picnic_numofgrid_layout.addWidget(self.picnic_numofgrid_z_text)

        #############
        picnic_meshrms_layout = QHBoxLayout()
        picnic_meshrms_label = QLabel("MeshRms")
        picnic_meshrms_label.setMinimumWidth(84)
        self.picnic_meshrms_x_text = QLineEdit("3.5")
        self.picnic_meshrms_y_text = QLineEdit("3.5")
        self.picnic_meshrms_z_text = QLineEdit("3.5")

        picnic_meshrms_layout.addWidget(picnic_meshrms_label)
        picnic_meshrms_layout.addWidget(self.picnic_meshrms_x_text)
        picnic_meshrms_layout.addWidget(self.picnic_meshrms_y_text)
        picnic_meshrms_layout.addWidget(self.picnic_meshrms_z_text)

        picnic_grid_layout.addLayout(picnic_numofgrid_layout)
        picnic_grid_layout.addLayout(picnic_meshrms_layout)

        picnic_layout.addWidget(self.cb_picnic)
        picnic_layout.addLayout(picnic_grid_layout)

        line = QFrame(self)
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)

        label_sc_method = QLabel("SCMethod")

        sc_method_layout.addWidget(label_sc_method)
        sc_method_layout.addLayout(fft_layout)
        sc_method_layout.addWidget(line)
        sc_method_layout.addLayout(picnic_layout)

        
        group_box_sc_method.setLayout(sc_method_layout)

        self.cb_fft.stateChanged.connect(self.cb_sc_method_change)
        self.cb_picnic.stateChanged.connect(self.cb_sc_method_change)

 ##########################################################
        group_box_multithreading = QGroupBox()

        hbox_multithreading = QHBoxLayout()

        multithreading_label = QLabel("MultiThreading")
        # default_size = multithreading_label.sizeHint()
        # print("Default Size:", default_size) #72 12
        # self.multithreading_x_text = QLineEdit()

        self.multithreading_checkbox = QCheckBox('Using Multithreading', self)
        self.multithreading_checkbox.stateChanged.connect(self.multithreading_change)

        hbox_multithreading.addWidget(multithreading_label)
        # hbox_multithreading.addWidget(self.multithreading_x_text)
        hbox_multithreading.addWidget(self.multithreading_checkbox)
        group_box_multithreading.setLayout(hbox_multithreading)
        ##########################################################
        group_box_scan_phase = QGroupBox()

        hbox_scan_phase = QHBoxLayout()

        scan_phase_label = QLabel("Scan Phase")
        scan_phase_label.setMinimumWidth(84)

        # self.scan_phase_text = QLineEdit()
        self.scan_phase_combo = QComboBox(self)
        self.scan_phase_combo.addItem("Not Scan Phase")
        self.scan_phase_combo.addItem("Scan Phase")
        self.scan_phase_combo.addItem("Read Phase")

        self.scan_phase_combo.currentIndexChanged.connect(self.scan_phase_selection)

        hbox_scan_phase.addWidget(scan_phase_label)
        hbox_scan_phase.addWidget(self.scan_phase_combo)
        # hbox_scan_phase.addWidget(self.scan_phase_text)
        group_box_scan_phase.setLayout(hbox_scan_phase)

        ##########################################################
        group_box_sc_use = QGroupBox()
        hbox_sc_use = QHBoxLayout()

        sc_use_label = QLabel("Space Charge")
        sc_use_label.setMinimumWidth(84)

        self.sc_use_checkbox = QCheckBox('Calculate Space Charge', self)
        self.sc_use_checkbox.stateChanged.connect(self.sc_use_change)

        hbox_sc_use.addWidget(sc_use_label)
        hbox_sc_use.addWidget(self.sc_use_checkbox)
        group_box_sc_use.setLayout(hbox_sc_use)

        #####################################################
        group_box_sc_step = QGroupBox()
        vbox_sc_step = QVBoxLayout()

        hbox_sc_step1 = QHBoxLayout()

        sc_step_label = QLabel('Space-charge step')
        self.sc_step_text = QLineEdit()

        hbox_sc_step2 = QHBoxLayout()
        self.sc_step_meter_checkbox = QCheckBox('meter', self)
        self.sc_step_beta_checkbox = QCheckBox('\u03B2\u03BB', self)

        self.sc_step_meter_checkbox.stateChanged.connect(self.sc_step_meter_change)
        self.sc_step_beta_checkbox.stateChanged.connect(self.sc_step_beta_change)

        hbox_sc_step1.addWidget(sc_step_label)
        hbox_sc_step1.addWidget(self.sc_step_text)

        hbox_sc_step1.addWidget(self.sc_step_meter_checkbox)
        hbox_sc_step1.addWidget(self.sc_step_beta_checkbox)

        vbox_sc_step.addLayout(hbox_sc_step1)

        group_box_sc_step.setLayout(vbox_sc_step)
        #
        ##########################################################
        group_box_step_per_period = QGroupBox()
        vbox_step_per_period = QVBoxLayout()

        step_per_period_label = QLabel("Calsulation step(\u03B2\u03BB)")
        step_per_period_label.setMinimumWidth(100)

        self.step_per_period_text = QLineEdit()


        vbox_step_per_period.addWidget(step_per_period_label)
        vbox_step_per_period.addWidget(self.step_per_period_text)
        group_box_step_per_period.setLayout(vbox_step_per_period)
        ########################################################
        #twst
        hbox_test = QHBoxLayout()
        self.button1 = QPushButton("lattice_mulp")
        self.button2 = QPushButton("lattice_env")

        self.button1.clicked.connect(self.fill_parameter)
        self.button2.clicked.connect(self.save_input)
        hbox_test.addWidget(self.button1)
        hbox_test.addWidget(self.button2)


        #################
        vertical_layout_main.addWidget(group_box_mulp_env)
        vertical_layout_main.addWidget(group_box_sc_method)

        vertical_layout_main.addWidget(group_box_multithreading)
        vertical_layout_main.addWidget(group_box_scan_phase)
        vertical_layout_main.addWidget(group_box_step_per_period)

        vertical_layout_main.addWidget(group_box_sc_use)
        vertical_layout_main.addWidget(group_box_sc_step)

        vertical_layout_main.addLayout(hbox_test)

        vertical_group_box_main.setLayout(vertical_layout_main)
        #########################################################################################

        layout.addWidget(vertical_group_box_main)

        self.setLayout(layout)

    def cb_basic_change(self, state):
        sender_checkbox = self.sender()  # 获取发送信号的复选框对象
        if sender_checkbox == self.cb_mulp:  # 如果发送信号的对象是 cb_mulp 复选框
            self.cb_env.setChecked(not sender_checkbox.isChecked())  # 设置 cb_env 与 cb_mulp 相反的状态
        elif sender_checkbox == self.cb_env:  # 如果发送信号的对象是 cb_env 复选框
            self.cb_mulp.setChecked(not sender_checkbox.isChecked())  # 设置 cb_mulp 与 cb_env 相反的状态

        if self.cb_mulp.isChecked():
            self.basic_signal.emit('basic_mulp')
        elif self.cb_env.isChecked():
            self.basic_signal.emit('basic_env')
        else:
            self.basic_signal.emit(None)
        self.mulp_env_behavior()

    def cb_sc_method_change(self, state):
        sender_checkbox = self.sender()  # 获取发送信号的复选框对象
        if sender_checkbox == self.cb_fft:
            self.cb_picnic.setChecked(not sender_checkbox.isChecked())
        elif sender_checkbox == self.cb_picnic:
            self.cb_fft.setChecked(not sender_checkbox.isChecked())



    def updatePath(self, new_path):
        self.project_path = new_path

    @treat_err
    def fill_parameter(self):
        input_path = os.path.join(self.project_path, "InputFile", "input.txt")
        input_res = read_txt(input_path, out='dict', readdall=1)
        if input_res.get('!simtype') == "mulp":
            self.cb_mulp.setChecked(True)
            if input_res.get('scmethod') == "fft":
                self.cb_fft.setChecked(True)
                if isinstance(input_res.get("numofgrid"), list) and len(input_res.get("numofgrid")) == 3:
                    self.fft_numofgrid_x_text.setText(input_res.get("numofgrid")[0])
                    self.fft_numofgrid_y_text.setText(input_res.get("numofgrid")[1])
                    self.fft_numofgrid_z_text.setText(input_res.get("numofgrid")[2])

                if isinstance(input_res.get('meshrms'), list) and len(input_res.get('meshrms')) == 3:
                    self.fft_meshrms_x_text.setText(input_res.get('meshrms')[0])
                    self.fft_meshrms_y_text.setText(input_res.get('meshrms')[1])
                    self.fft_meshrms_z_text.setText(input_res.get('meshrms')[2])


            elif input_res.get('scmethod') == "picnic":
                self.cb_picnic.setChecked(True)
                if isinstance(input_res.get("numofgrid"), list) and len(input_res.get("numofgrid")) == 3:
                    self.picnic_numofgrid_x_text.setText(input_res.get("numofgrid")[0])
                    self.picnic_numofgrid_y_text.setText(input_res.get("numofgrid")[1])
                    self.picnic_numofgrid_z_text.setText(input_res.get("numofgrid")[2])

                if isinstance(input_res.get('meshrms'), list) and len(input_res.get('meshrms')) == 3:
                    self.picnic_meshrms_x_text.setText(input_res.get('meshrms')[0])
                    self.picnic_meshrms_y_text.setText(input_res.get('meshrms')[1])
                    self.picnic_meshrms_z_text.setText(input_res.get('meshrms')[2])


            self.multithreading_num = int(input_res.get('multithreading', 0))

            if self.multithreading_num == 0:
                self.multithreading_checkbox.setChecked(False)

            elif self.multithreading_num == 1:
                self.multithreading_checkbox.setChecked(True)

            self.scan_phase_num = int(input_res.get('scanphase', 1))
            self.scan_phase_combo.setCurrentIndex(self.scan_phase_num)

            self.sc_use_num = int(input_res.get('spacecharge', 0))
            if self.sc_use_num == 0:
                self.sc_use_checkbox.setChecked(False)
            elif self.sc_use_num == 1:
                self.sc_use_checkbox.setChecked(True)

            self.step_per_period_text.setText(input_res.get('steppercycle', '100'))

        # 对于包络模型的输入
        if input_res.get('!simtype') == "env":
            self.cb_env.setChecked(True)
            self.sc_use_num_env = int(input_res.get('isspacecharge', 3))
            if self.sc_use_num_env == 0:
                self.sc_use_checkbox.setChecked(False)
            elif self.sc_use_num_env == 1:
                self.sc_use_checkbox.setChecked(True)

            self.sc_step_text.setText(input_res.get('spacechargelong'))

            sc_step_type = int(input_res.get('spacechargetype', 0))
            if int(sc_step_type) == 0:
                self.sc_step_meter_checkbox.setChecked(True)
            elif int(sc_step_type) == 1:
                self.sc_step_beta_checkbox.setChecked(True)


    @treat_err2
    def generate_input_list(self, ):

        res = []
        if self.cb_mulp.isChecked():
            res.append(["!simtype",  "mulp"])

            if self.cb_fft.isChecked():
                res.append(['SCMethod', "FFT"])
                res.append(['numofgrid', self.fft_numofgrid_x_text.text(), self.fft_numofgrid_y_text.text(),
                            self.fft_numofgrid_z_text.text()])   
                res.append(['MeshRms', self.fft_meshrms_x_text.text(), self.fft_meshrms_y_text.text(),
                            self.fft_meshrms_z_text.text()])
                
            elif self.cb_picnic.isChecked():
                res.append(['SCMethod', "PICNIC"])
                res.append(['numofgrid', self.picnic_numofgrid_x_text.text(), self.picnic_numofgrid_y_text.text(),
                            self.picnic_numofgrid_z_text.text()])   
                res.append(['MeshRms', self.picnic_meshrms_x_text.text(), self.picnic_meshrms_y_text.text(),
                            self.picnic_meshrms_z_text.text()])

            if self.multithreading_checkbox.isChecked():
                res.append(['MultiThreading', '1'])
            elif not self.multithreading_checkbox.isChecked():
                res.append(['MultiThreading', '0'])


            res.append(['ScanPhase', str(self.scan_phase_combo.currentIndex())])
            if self.sc_use_checkbox.isChecked():
                res.append(['SpaceCharge', '1'])
            else:
                res.append(['SpaceCharge', '0'])

            res.append(['StepPerCycle', self.step_per_period_text.text()])

        elif self.cb_env.isChecked():
            res.append(["!simtype",  "env"])

            if self.sc_use_checkbox.isChecked():
                res.append(['ISSPACECHARGE', '1'])
            else:
                res.append(['ISSPACECHARGE', '0'])


            res.append(['SPACECHARGELONG', self.sc_step_text.text()])


            if self.sc_step_meter_checkbox.isChecked():
                res.append(['SPACECHARGETYPE', "0"])
            elif self.sc_step_beta_checkbox.isChecked():
                res.append(['SPACECHARGETYPE', "1"])

        return res

    # @treat_err
    def save_input(self, ):
        input_list = self.generate_input_list()

        input_path = os.path.join(self.project_path, 'InputFile', 'input.txt')

        # 打开文件以写入数据
        with open(input_path, 'w', encoding='utf-8') as file:
            # 遍历嵌套列表的每个子列表
            for sublist in input_list:
                # 将子列表中的元素转换为字符串，并使用逗号分隔
                line = '   '.join(map(str, sublist))
                # 将每个子列表的字符串写入文件
                file.write(line + '\n')

    def multithreading_change(self, state):
        if state == Qt.Checked:
            self.multithreading_num = 1
        else:
            self.multithreading_num = 0

    def sc_use_change(self, state):
        if state == Qt.Checked:
            self.sc_use_num = 1
        else:
            self.sc_use_num = 0

    def scan_phase_selection(self, index):
        # 处理用户的选择
        selected_option = self.sender().currentText()

    def sc_step_meter_change(self, state):
        # 获取发送信号的复选框
        if state == Qt.Checked:
            self.sc_step_beta_checkbox.setChecked(False)


    def sc_step_beta_change(self, state):
        # 获取发送信号的复选框
        if state == Qt.Checked:
            self.sc_step_meter_checkbox.setChecked(False)

    def inspect(self):
        if not self.step_per_period_text.text():
            e = "Missing calculation step"
            QMessageBox.warning(None, 'Error', e)
            return False
        else:
            return True

    def mulp_env_behavior(self):
        mulp_box = [self.cb_fft, self.cb_picnic, self.multithreading_checkbox]
        mulp_line = [self.fft_numofgrid_x_text, self.fft_numofgrid_y_text, self.fft_numofgrid_z_text,
                     self.fft_meshrms_x_text, self.fft_meshrms_y_text, self.fft_meshrms_z_text,
                     self.picnic_numofgrid_x_text, self.picnic_numofgrid_y_text, self.picnic_numofgrid_z_text,
                     self.picnic_meshrms_x_text, self.picnic_meshrms_y_text, self.picnic_meshrms_z_text,
                     self.step_per_period_text
                     ]

        env_line = [self.sc_step_text]
        env_box = [self.sc_step_meter_checkbox, self.sc_step_beta_checkbox]

        #如果是多粒子模式
        if self.cb_mulp.isChecked():
            for line_edit in env_line:
                line_edit.setEnabled(False)
            for box in env_box:
                box.setEnabled(False)


            for line_edit in mulp_line:
                line_edit.setEnabled(True)

            for box in mulp_box:
                box.setEnabled(True)

            self.scan_phase_combo.setEnabled(True)
            self.scan_phase_combo.setStyleSheet(f"")

        elif self.cb_env.isChecked():
            for line_edit in env_line:
                line_edit.setEnabled(True)
            for box in env_box:
                box.setEnabled(True)

            for line_edit in mulp_line:
                line_edit.setEnabled(False)
            for box in mulp_box:
                box.setEnabled(False)


            self.scan_phase_combo.setEnabled(False)
            self.scan_phase_combo.setStyleSheet(f"QComboBox {{ background-color:  {gray240} }}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = PageInput(r'C:\Users\anxin\Desktop\comparison\avas_test')
    main_window.setGeometry(800, 500, 600, 650)
    main_window.setStyleSheet("background-color: rgb(253, 253, 253);")
    main_window.show()
    sys.exit(app.exec_())