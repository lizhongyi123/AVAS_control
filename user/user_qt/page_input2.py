import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QToolBar, QVBoxLayout, QWidget, QPushButton, \
    QStackedWidget, QMenu, QLabel, QLineEdit, QTextEdit, QGridLayout, QHBoxLayout, QFrame, QFileDialog, QGroupBox, \
    QComboBox, QSizePolicy, QCheckBox, QMessageBox

import os

from PyQt5.QtCore import Qt
from utils.readfile import read_txt, read_dst
from user.user_qt.user_defined import treat_err, treat_err2

class PageInput(QWidget):
    def __init__(self, project_path):
        super().__init__()
        self.project_path = project_path
        self.multithreading_num = -1
        self.sc_use_num = -1
        self.scan_phase_num = -1
        self.sc_step_type =- 1
        self.initUI()

    def initUI(self):
        # print(self.project_path)
        self.setStyleSheet("background-color: rgb(250, 250, 250);")

        layout = QHBoxLayout()


        # 创建一个垂直组合框
        vertical_group_box_main = QGroupBox("Operation setting")


        vertical_layout_main = QVBoxLayout()
##########################################################################


        group_box_sc_method = QGroupBox()

        hbox_sc_method = QHBoxLayout()

        label_sc_method = QLabel("SCMethod")
        label_sc_method.setMinimumWidth(84)

        # default_size = label_distribution.sizeHint()
        # print("Default Size:", default_size) #72 12

        # self.text_distribution = MyQLineEdit("")

        self.sc_method_combo = QComboBox(self)
        self.sc_method_combo.addItem("FFT")
        self.sc_method_combo.addItem("PICNIC")

        # combo_font = QFont("Arial", 12)  # 使用 Arial 字体，大小为 12
        # distribution_combo.setFont(combo_font)

        # 连接下拉框的currentIndexChanged信号到处理函数
        self.sc_method_combo.currentIndexChanged.connect(self.sc_method_selection)

        hbox_sc_method.addWidget(label_sc_method)
        hbox_sc_method.addWidget(self.sc_method_combo)

        group_box_sc_method.setLayout(hbox_sc_method)


##########################################################
        group_box_numofgrid = QGroupBox()
        hbox_numofgrid = QHBoxLayout()

        numofgrid_label = QLabel("Numofgrid")
        numofgrid_label.setMinimumWidth(84)

        self.numofgrid_x_text = QLineEdit()
        self.numofgrid_y_text = QLineEdit()
        self.numofgrid_z_text = QLineEdit()

        hbox_numofgrid.addWidget(numofgrid_label)
        hbox_numofgrid.addWidget(self.numofgrid_x_text)
        hbox_numofgrid.addWidget(self.numofgrid_y_text)
        hbox_numofgrid.addWidget(self.numofgrid_z_text)

        group_box_numofgrid.setLayout(hbox_numofgrid)
##########################################################
        group_box_meshrms = QGroupBox()
        
        hbox_meshrms = QHBoxLayout()

        meshrms_label = QLabel("MeshRms")
        meshrms_label.setMinimumWidth(84)

        self.meshrms_x_text = QLineEdit()
        self.meshrms_y_text = QLineEdit()
        self.meshrms_z_text = QLineEdit()

        hbox_meshrms.addWidget(meshrms_label)
        hbox_meshrms.addWidget(self.meshrms_x_text)
        hbox_meshrms.addWidget(self.meshrms_y_text)
        hbox_meshrms.addWidget(self.meshrms_z_text)
        group_box_meshrms.setLayout(hbox_meshrms)
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

        hbox_sc_step1.addWidget( self.sc_step_meter_checkbox)
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
        vertical_layout_main.addWidget(group_box_sc_method)
        vertical_layout_main.addWidget(group_box_numofgrid)
        vertical_layout_main.addWidget(group_box_meshrms)
        vertical_layout_main.addWidget(group_box_multithreading)
        vertical_layout_main.addWidget(group_box_scan_phase)
        vertical_layout_main.addWidget(group_box_sc_use)
        vertical_layout_main.addWidget(group_box_sc_step)
        vertical_layout_main.addWidget(group_box_step_per_period)

        vertical_group_box_main.setLayout(vertical_layout_main)
        #########################################################################################




        layout.addWidget(vertical_group_box_main)

        self.setLayout(layout)

    def sc_method_selection(self, index):
        selected_text = self.sc_method_combo.itemText(index)

        print("Selected SCMethod:", selected_text)

        # 在这里可以根据选中的文本进行相应的处理
        if selected_text == "FFT":
            # 处理 FFT 方法的情况
            self.numofgrid_x_text.setText('64')
            self.numofgrid_y_text.setText('64')
            self.numofgrid_z_text.setText('64')

            self.meshrms_x_text.setText('6.5')
            self.meshrms_y_text.setText('6.5')
            self.meshrms_z_text.setText('6.5')



        elif selected_text == "PICNIC":
            self.numofgrid_x_text.setText('18')
            self.numofgrid_y_text.setText('18')
            self.numofgrid_z_text.setText('18')

            self.meshrms_x_text.setText('3.5')
            self.meshrms_y_text.setText('3.5')
            self.meshrms_z_text.setText('3.5')

        else:
            # 处理其他情况
            pass

    def updatePath(self, new_path):
        self.project_path = new_path

    # @treat_err
    def fill_parameter(self):
        input_path = os.path.join(self.project_path, "InputFile", "input.txt")
        input_res = read_txt(input_path)
        self.sc_method_combo.setCurrentText(input_res.get('scmethod', 'FFT'))


        if isinstance(input_res.get("numofgrid"), list) and len(input_res.get("numofgrid")) == 3:
            self.numofgrid_x_text.setText(input_res.get("numofgrid")[0])
            self.numofgrid_y_text.setText(input_res.get("numofgrid")[1])
            self.numofgrid_z_text.setText(input_res.get("numofgrid")[2])
        # else:
        #     self.numofgrid_x_text.setText('64')
        #     self.numofgrid_y_text.setText('64')
        #     self.numofgrid_z_text.setText('64')

        if isinstance(input_res.get('meshrms'), list) and len(input_res.get('meshrms')) == 3:
            self.meshrms_x_text.setText(input_res.get('meshrms')[0])
            self.meshrms_y_text.setText(input_res.get('meshrms')[1])
            self.meshrms_z_text.setText(input_res.get('meshrms')[2])
        # else:
        #     self.meshrms_x_text.setText('8.0')
        #     self.meshrms_y_text.setText('8.0')
        #     self.meshrms_z_text.setText('8.0')

        elif self.sc_method_combo.currentText() == 'FFT':
            self.sc_method_selection(0)
        elif self.sc_method_combo.currentText() == 'PICNIC':
            self.sc_method_selection(1)


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



        #对于包络模型的输入
        if True:
            self.sc_use_num_env = int(input_res.get('isspacecharge', 3))
            if self.sc_use_num_env == 0:
                self.sc_use_checkbox.setChecked(False)
            elif self.sc_use_num_env == 1:
                self.sc_use_checkbox.setChecked(True)

            self.sc_step_text.setText(input_res.get('spacechargelong'))

            sc_step_type = input_res.get('spacechargetype', 0)
            if int(sc_step_type) == 0:
                self.sc_step_meter_checkbox.setChecked(True)
            elif int(sc_step_type) == 0:
                self.sc_step_beta_checkbox.setChecked(True)




        self.step_per_period_text.setText(input_res.get('steppercycle', '100'))

    @treat_err2
    def generate_input_list(self, mulp_env_type):

        res = []
        if mulp_env_type == 'basic_mulp':
            res.append(['SCMethod', self.sc_method_combo.currentText()])
            if self.numofgrid_x_text.text() and self.numofgrid_y_text.text() and self.numofgrid_z_text.text():
                res.append(['numofgrid', self.numofgrid_x_text.text(), self.numofgrid_y_text.text(),
                            self.numofgrid_z_text.text()])
            if self.meshrms_x_text.text() and self.meshrms_y_text.text() and self.meshrms_z_text.text():
                res.append(['MeshRms', self.meshrms_x_text.text(), self.meshrms_y_text.text(),
                            self.meshrms_z_text.text()])


            res.append(['MultiThreading', str(self.multithreading_num)])
            res.append(['ScanPhase', str(self.scan_phase_combo.currentIndex())])
            res.append(['SpaceCharge',  str(self.sc_use_num)])
            res.append(['StepPerCycle', self.step_per_period_text.text()])

        elif mulp_env_type == 'basic_env':
            res.append(['ISSPACECHARGE', '1'])
            res.append(['SPACECHARGELONG', self.sc_step_text.text()])
            res.append(['SPACECHARGETYPE', self.sc_step_type])

        return res


    # @treat_err
    def save_input(self, mulp_env_type):
        if mulp_env_type is None:
            mulp_env_type = 'basic_mulp'
        input_list = self.generate_input_list(mulp_env_type)
        print('input', input_list)
        # print(input_list)

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
            self.sc_step_type = 0

    def sc_step_beta_change(self, state):
        # 获取发送信号的复选框
        if state == Qt.Checked:
            self.sc_step_meter_checkbox.setChecked(False)
            self.sc_step_type = 1

    def inspect(self):
        if not self.step_per_period_text.text():
            e = "Missing calculation step"
            QMessageBox.warning(None, 'Error', e)
            return False
        else:
            return True

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     main_window = PageInput(r'C:\Users\anxin\Desktop\00000')
#     main_window.fill_parameter()
#     main_window.setGeometry(800, 500, 600, 650)
#     main_window.setStyleSheet("background-color: rgb(253, 253, 253);")
#     main_window.show()
#     sys.exit(app.exec_())