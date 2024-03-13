import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QToolBar, QVBoxLayout, QWidget, QPushButton, \
    QStackedWidget,QMenu, QLabel, QLineEdit, QTextEdit,  QGridLayout, QHBoxLayout,  QFrame, QFileDialog, QGroupBox,\
    QComboBox, QSizePolicy, QMessageBox,QPushButton
import os
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QStandardPaths
from user.user_qt.user_defined import MyQLineEdit

from PyQt5.QtCore import Qt
from utils.readfile import read_txt, read_dst
from utils.treatfile import copy_file

from aftertreat.dataanalysis.caltwiss import CalTwiss
from user_defined import treat_err, treat_err2
from utils.treat_directory import list_files_in_directory
from utils.treatfile import split_file, file_in_directory
gray240 = "rgb(240, 240, 240)"

class PageBeam(QWidget):
    def __init__(self, project_path):
        super().__init__()
        self.project_path = project_path
        self.decimals = 5
        self.initUI()

    def initUI(self):
        # print(self.project_path)
        self.setStyleSheet("background-color: rgb(250, 250, 250);")

        layout = QHBoxLayout()

        # 创建一个垂直组合框
        vertical_group_box1 = QGroupBox("Beam parameters")


        vertical_layout1 = QVBoxLayout()

#####################################################

        vbox_particle_input_file = QVBoxLayout()

        label_particle_input_file = QLabel("Multiparticle input file ")

        # default_size = label_particle_input_file .sizeHint()
        # print("Default Size:", default_size) #72 12

        input_file_select_layout = QHBoxLayout()
        self.text_particle_input_file  = MyQLineEdit(" ")
        self.button_select_input_file = QPushButton(QApplication.style().standardIcon(32),"")
        self.button_select_input_file.clicked.connect(self.select_dst_file)


        input_file_select_layout.addWidget(self.text_particle_input_file)
        input_file_select_layout.addWidget(self.button_select_input_file)


        self.button_import_beam_parameter = QPushButton("Import all beam parameters from file")
        self.button_import_beam_parameter.clicked.connect(self.import_beam_parameter)



        vbox_particle_input_file.addWidget(label_particle_input_file )
        vbox_particle_input_file.addLayout(input_file_select_layout)
        vbox_particle_input_file.addWidget(self.button_import_beam_parameter)

        particle_input_file_group_box = QGroupBox("")

        # particle_input_file_layout = QVBoxLayout()
        # particle_input_file_layout.addLayout(vbox_particle_input_file)
        particle_input_file_group_box.setLayout(vbox_particle_input_file)



        

###############################################
        hbox_charge = QHBoxLayout()

        label_charge = QLabel("Charge")
        label_charge.setFixedSize(90, 12)  # 设置宽度和高度
        label_charge.setAlignment(Qt.AlignCenter)  # 设置水平和垂直居中

        self.text_charge = MyQLineEdit("")
        label_charge_unit = QLabel("e")

        hbox_charge.addWidget(label_charge)
        hbox_charge.addWidget(self.text_charge)
        hbox_charge.addWidget(label_charge_unit)

############################
        hbox_mass = QHBoxLayout()

        label_mass = QLabel("Mass")
        label_mass.setFixedSize(90, 12)  # 设置宽度和高度
        label_mass.setAlignment(Qt.AlignCenter)  # 设置水平和垂直居中

        self.text_mass = MyQLineEdit("")
        label_mass_unit = QLabel("MeV")

        hbox_mass.addWidget(label_mass)
        hbox_mass.addWidget(self.text_mass)
        hbox_mass.addWidget(label_mass_unit)

############################
        hbox_current = QHBoxLayout()

        label_current = QLabel("Current")
        label_current.setFixedSize(90, 12)  # 设置宽度和高度
        label_current.setAlignment(Qt.AlignCenter)  # 设置水平和垂直居中

        self.text_current = MyQLineEdit("")
        label_current_unit = QLabel("MeV")

        hbox_current.addWidget(label_current)
        hbox_current.addWidget(self.text_current)
        hbox_current.addWidget(label_current_unit)
############################
        hbox_current = QHBoxLayout()

        label_current = QLabel("Current")
        label_current.setFixedSize(90, 12)  # 设置宽度和高度
        label_current.setAlignment(Qt.AlignCenter)  # 设置水平和垂直居中

        self.text_current = MyQLineEdit("")
        label_current_unit = QLabel("mA")

        hbox_current.addWidget(label_current)
        hbox_current.addWidget(self.text_current)
        hbox_current.addWidget(label_current_unit)

############################
        hbox_particel_number = QHBoxLayout()

        label_particel_number = QLabel("Num of particle")
        label_particel_number.setFixedSize(90, 12)  # 设置宽度和高度
        label_particel_number.setAlignment(Qt.AlignCenter)  # 设置水平和垂直居中

        self.text_particel_number = MyQLineEdit("")
        label_particel_number_unit = QLabel("")

        hbox_particel_number.addWidget(label_particel_number)
        hbox_particel_number.addWidget(self.text_particel_number)
        hbox_particel_number.addWidget(label_particel_number_unit)

############################
        hbox_frequency = QHBoxLayout()

        label_frequency = QLabel("Frequency")
        label_frequency.setFixedSize(90, 12)  # 设置宽度和高度
        label_frequency.setAlignment(Qt.AlignCenter)  # 设置水平和垂直居中

        self.text_frequency = MyQLineEdit("")
        label_frequency_unit = QLabel("Hz")

        hbox_frequency.addWidget(label_frequency)
        hbox_frequency.addWidget(self.text_frequency)
        hbox_frequency.addWidget(label_frequency_unit)

############################
        hbox_energy = QHBoxLayout()

        label_energy = QLabel("Energy")
        label_energy.setFixedSize(90, 12)  # 设置宽度和高度
        label_energy.setAlignment(Qt.AlignCenter)  # 设置水平和垂直居中

        self.text_energy = MyQLineEdit("")
        label_energy_unit = QLabel("")

        hbox_energy.addWidget(label_energy)
        hbox_energy.addWidget(self.text_energy)
        hbox_energy.addWidget(label_energy_unit)



############################
        line_frame1 = QFrame()
        line_frame1.setFrameShape(QFrame.HLine)  # 设置为水平线
        line_frame1.setFrameShadow(QFrame.Sunken)  # 设置阴影效果
        line_frame1.setLineWidth(2)  # 设置线宽度
        line_frame1.setStyleSheet("color: blue;")  # 设置线颜色
#############################
        grid_twiss = QGridLayout()

        label_alpha_xx = QLabel("\u03B1<sub>xx‘</sub>")
        self.alpha_xx_text = MyQLineEdit()

        label_beta_xx = QLabel("\u03B2<sub>xx‘</sub>")
        self.beta_xx_text = MyQLineEdit()
        beta_xx_unit = QLabel("mm/\u03C0 mrad")


        label_alpha_yy = QLabel("\u03B1<sub>yy‘</sub>")
        self.alpha_yy_text = MyQLineEdit()

        label_beta_yy = QLabel("\u03B2<sub>yy‘</sub>")
        self.beta_yy_text = MyQLineEdit()
        beta_yy_unit = QLabel("mm/\u03C0 mrad")

        label_alpha_zz = QLabel("\u03B1<sub>zz‘</sub>")
        self.alpha_zz_text = MyQLineEdit()

        label_beta_zz = QLabel("\u03B2<sub>zz‘</sub>")
        self.beta_zz_text = MyQLineEdit()
        beta_zz_unit = QLabel("mm/\u03C0 mrad")


        grid_twiss.addWidget(label_alpha_xx, 0, 0)
        grid_twiss.addWidget(self.alpha_xx_text, 0, 1)

        grid_twiss.addWidget(label_beta_xx, 1, 0)
        grid_twiss.addWidget(self.beta_xx_text, 1, 1)
        grid_twiss.addWidget(beta_xx_unit, 1, 2)

        grid_twiss.addWidget(label_alpha_yy, 2, 0)
        grid_twiss.addWidget(self.alpha_yy_text, 2, 1)

        grid_twiss.addWidget(label_beta_yy, 3, 0)
        grid_twiss.addWidget(self.beta_yy_text, 3, 1)
        grid_twiss.addWidget(beta_yy_unit, 3, 2)


        grid_twiss.addWidget(label_alpha_zz, 4, 0)
        grid_twiss.addWidget(self.alpha_zz_text, 4, 1)

        grid_twiss.addWidget(label_beta_zz, 5, 0)
        grid_twiss.addWidget(self.beta_zz_text, 5, 1)
        grid_twiss.addWidget(beta_zz_unit, 5, 2)

 ############################
        line_frame2 = QFrame()
        line_frame2.setFrameShape(QFrame.HLine)  # 设置为水平线
        line_frame2.setFrameShadow(QFrame.Sunken)  # 设置阴影效果
        line_frame2.setLineWidth(2)  # 设置线宽度
        line_frame2.setStyleSheet("color: blue;")  # 设置线颜色

########################################################
        outer_group_box = QGroupBox("Twiss parameter")
        outer_layout = QVBoxLayout()
        outer_layout.addLayout(grid_twiss)
        outer_group_box.setLayout(outer_layout)


#######################################
        grid_emittince = QGridLayout()

        label_varepsilon_xx = QLabel("\u03B5<sub>xx‘</sub>")
        self.varepsilon_xx_text = MyQLineEdit()
        varepsilon_xx_unit = QLabel("\u03C0.mm.mrad")

        label_varepsilon_yy = QLabel("\u03B5<sub>yy‘</sub>")
        self.varepsilon_yy_text = MyQLineEdit()
        varepsilon_yy_unit = QLabel("\u03C0.mm.mrad")

        label_varepsilon_zz = QLabel("\u03B5<sub>zz‘</sub>")
        self.varepsilon_zz_text = MyQLineEdit()
        varepsilon_zz_unit = QLabel("\u03C0.mm.mrad")

        grid_emittince.addWidget(label_varepsilon_xx, 0 , 0)
        grid_emittince.addWidget(self.varepsilon_xx_text, 0, 1)
        grid_emittince.addWidget(varepsilon_xx_unit, 0, 2)

        grid_emittince.addWidget(label_varepsilon_yy, 1, 0)
        grid_emittince.addWidget(self.varepsilon_yy_text, 1, 1)
        grid_emittince.addWidget(varepsilon_yy_unit, 1, 2)

        grid_emittince.addWidget(label_varepsilon_zz, 2, 0)
        grid_emittince.addWidget(self.varepsilon_zz_text, 2, 1)
        grid_emittince.addWidget(varepsilon_zz_unit, 2, 2)

        emittance_group_box = QGroupBox("Emittance")
        emittance_layout = QVBoxLayout()
        emittance_layout.addLayout(grid_emittince)
        emittance_group_box.setLayout(emittance_layout)

###############################
        vertical_layout1.addWidget(particle_input_file_group_box)
        vertical_layout1.addLayout(hbox_charge)
        vertical_layout1.addLayout(hbox_mass)
        vertical_layout1.addLayout(hbox_current)
        vertical_layout1.addLayout(hbox_particel_number)
        vertical_layout1.addLayout(hbox_frequency)
        vertical_layout1.addLayout(hbox_energy)

        vertical_layout1.addWidget(line_frame1)
        vertical_layout1.addWidget(outer_group_box)
        vertical_layout1.addWidget(line_frame2)

        vertical_layout1.addWidget(emittance_group_box)


        vertical_group_box1.setLayout(vertical_layout1)
#########################################################################################


        vertical_group_box2 = QGroupBox()
        vertical_layout2 = QVBoxLayout()

#############################################################

        hbox_distribution = QHBoxLayout()

        label_distribution = QLabel("Distribution")

        # default_size = label_distribution.sizeHint()
        # print("Default Size:", default_size) #72 12

        # self.text_distribution = MyQLineEdit("")

#横向
        self.distribution_combo_trans = QComboBox(self)
        self.distribution_combo_trans.addItem("")
        self.distribution_combo_trans.addItem("GS")
        self.distribution_combo_trans.addItem("WB")
        self.distribution_combo_trans.addItem("PB")
        self.distribution_combo_trans.addItem("kv")


        # combo_font = QFont("Arial", 12)  # 使用 Arial 字体，大小为 12
        # distribution_combo_trans.setFont(combo_font)

        # 连接下拉框的currentIndexChanged信号到处理函数
        self.distribution_combo_trans.currentIndexChanged.connect(self.distribution_selection_trans)

#纵向
        self.distribution_combo_longi= QComboBox(self)
        self.distribution_combo_longi.addItem("")
        self.distribution_combo_longi.addItem("GS")
        self.distribution_combo_longi.addItem("WB")
        self.distribution_combo_longi.addItem("PB")
        self.distribution_combo_longi.addItem("kv")


        # combo_font = QFont("Arial", 12)  # 使用 Arial 字体，大小为 12
        # distribution_combo_longi.setFont(combo_font)

        # 连接下拉框的currentIndexChanged信号到处理函数
        self.distribution_combo_longi.currentIndexChanged.connect(self.distribution_selection_longi)



        hbox_distribution.addWidget(label_distribution)
        hbox_distribution.addStretch(2)
        hbox_distribution.addWidget(self.distribution_combo_trans)
        hbox_distribution.addStretch(1)
        hbox_distribution.addWidget(self.distribution_combo_longi)
        hbox_distribution.addStretch(1)
###########################################################################
        hbox_displacePos = QHBoxLayout()

        label_displacePos = QLabel("Position Deviation")
        label_displacePos.setFixedSize(150, 12)  # 设置宽度和高度
        label_displacePos.setAlignment(Qt.AlignCenter)  # 设置水平和垂直居中

        self.text_displacePos_x = MyQLineEdit("")
        self.text_displacePos_y = MyQLineEdit("")
        self.text_displacePos_z = MyQLineEdit("")



        hbox_displacePos.addWidget(label_displacePos)
        hbox_displacePos.addWidget(self.text_displacePos_x)
        hbox_displacePos.addWidget(self.text_displacePos_y)
        hbox_displacePos.addWidget(self.text_displacePos_z)

###########################################################################
        hbox_displaceDpos = QHBoxLayout()

        label_displaceDpos = QLabel("Momentum Deviation")
        label_displaceDpos.setFixedSize(150, 12)  # 设置宽度和高度
        label_displaceDpos.setAlignment(Qt.AlignCenter)  # 设置水平和垂直居中

        self.text_displaceDpos_x = MyQLineEdit("")
        self.text_displaceDpos_y = MyQLineEdit("")
        self.text_displaceDpos_z = MyQLineEdit("")


        hbox_displaceDpos.addWidget(label_displaceDpos)
        hbox_displaceDpos.addWidget(self.text_displaceDpos_x)
        hbox_displaceDpos.addWidget(self.text_displaceDpos_y)
        hbox_displaceDpos.addWidget(self.text_displaceDpos_z)



####################################################################################


        vertical_layout2.addLayout(hbox_distribution)
        vertical_layout2.addLayout(hbox_displacePos)
        vertical_layout2.addLayout(hbox_displaceDpos)
        vertical_layout2.addStretch(1)




        vertical_group_box2.setLayout(vertical_layout2)


#######################################################

        vertical_group_box1.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        vertical_group_box2.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        vertical_group_box1.setMinimumWidth(300)

        layout.addWidget(vertical_group_box1)
        layout.addWidget(vertical_group_box2)


        self.setLayout(layout)

        self.text_particle_input_file.textChanged.connect(self.onParticleInputTextChanged)
    def updatePath(self, new_path):
        self.project_path = new_path

    # @treat_err
    def read_beam(self):
        beam_path = os.path.join(self.project_path, 'inputFile', 'beam.txt')
        # print(beam_path)
        if os.path.exists(beam_path):
            print(read_txt(beam_path))

    # @treat_err
    def refreshUI(self):
        self.initUI()  # Call initUI to refresh the UI


    def distribution_selection_trans(self, index):
        # 处理用户的选择
        selected_option = self.sender().currentText()
        # self.label_result.setText(f"Selected Option: {selected_option}")
    def distribution_selection_longi(self, index):
        # 处理用户的选择
        selected_option = self.sender().currentText()
        # self.label_result.setText(f"Selected Option: {selected_option}")

    def sc_method_selection(self, index):
        # 处理用户的选择
        selected_option = self.sender().currentText()
        # self.label_result.setText(f"Selected Option: {selected_option}")


    def fill_parameter(self):
        beam_path = os.path.join(self.project_path, "InputFile", "beam.txt")
        beam_res = read_txt(beam_path)


        if beam_res.get("readparticledistribution") is not None:
            self.text_particle_input_file.setText(beam_res.get("readparticledistribution"))
            # dst_path = os.path.join(self.project_path, "InputFile", self.text_particle_input_file.text())
            #
            # if os.path.exists(dst_path):
            #     pass
            # else:
            #     QMessageBox.warning(None, 'Error', f'{self.text_particle_input_file.text()} does not exist')
            #
            # dst_res = read_dst(dst_path)
            #
            # #print(dst_res)
            self.text_charge.setText(beam_res.get('numofcharge'))
            # self.text_mass.setText(str(dst_res.get('basemassinmev')))
            # self.text_current.setText(str(dst_res.get('ib')))
            # self.text_particel_number.setText(str(dst_res.get('number')))
            # self.text_frequency.setText(str(dst_res.get('freq')))
            #
            # obj = CalTwiss(dst_path)
            # obj.get_data()
            # energy = round(obj.energy, self.decimals)
            # self.text_energy.setText(str(energy))
            #
            # twiss = CalTwiss(dst_path).get_emit_xyz()
            #
            # self.alpha_xx_text.setText(str(round(twiss[0][0], self.decimals)))
            # self.beta_xx_text.setText(str(round(twiss[0][1], self.decimals)))
            #
            # self.alpha_yy_text.setText(str(round(twiss[1][0], self.decimals)))
            # self.beta_yy_text.setText(str(round(twiss[1][1], self.decimals)))
            #
            # self.alpha_zz_text.setText(str(round(twiss[2][0], self.decimals)))
            # self.beta_zz_text.setText(str(round(twiss[2][1], self.decimals)))
            #
            # self.varepsilon_xx_text.setText(str(round(twiss[0][2], self.decimals)))
            # self.varepsilon_yy_text.setText(str(round(twiss[1][2],self.decimals)))
            # self.varepsilon_zz_text.setText(str(round(twiss[2][2], self.decimals)))



        else:
            self.text_particle_input_file.clear()
            self.text_charge.setText(beam_res.get('numofcharge'))
            self.text_mass.setText(beam_res.get('particlerestmass'))
            self.text_current.setText(beam_res.get('current'))
            self.text_particel_number.setText(beam_res.get('particlenumber'))
            self.text_frequency.setText(beam_res.get('frequency'))
            self.text_energy.setText(beam_res.get('kneticenergy'))

            if isinstance(beam_res.get('twissx'), list) and len(beam_res.get('twissx')) == 3:
                self.alpha_xx_text.setText(beam_res.get('twissx')[0])
                self.beta_xx_text.setText(beam_res.get('twissx')[1])
                self.varepsilon_xx_text.setText(beam_res.get('twissx')[2])
            else:
                self.alpha_xx_text.clear()
                self.beta_xx_text.clear()
                self.varepsilon_xx_text.clear()


            if isinstance(beam_res.get('twissy'), list) and  len(beam_res.get('twissy')) == 3:
                self.alpha_yy_text.setText(beam_res.get('twissy')[0])
                self.beta_yy_text.setText(beam_res.get('twissy')[1])
                self.varepsilon_yy_text.setText(beam_res.get('twissy')[2])
            else:
                self.alpha_yy_text.clear()
                self.beta_yy_text.clear()
                self.varepsilon_yy_text.clear()


            if isinstance(beam_res.get('twissz'), list) and len(beam_res.get('twissz')) == 3:
                self.alpha_zz_text.setText(beam_res.get('twissz')[0])
                self.beta_zz_text.setText(beam_res.get('twissz')[1])
                self.varepsilon_zz_text.setText(beam_res.get('twissz')[2])
            else:
                self.alpha_zz_text.clear()
                self.beta_zz_text.clear()
                self.varepsilon_zz_text.clear()


            if isinstance(beam_res.get('distribution'), list) and len(beam_res.get('distribution')) == 2:
                self.distribution_combo_trans.setCurrentText(beam_res.get('distribution')[0])
                self.distribution_combo_longi.setCurrentText(beam_res.get('distribution')[1])
            else:
                self.distribution_combo_trans.setCurrentIndex(0)
                self.distribution_combo_longi.setCurrentIndex(0)

            if isinstance(beam_res.get('displacepos'), list) and len(beam_res.get('displacepos')) == 3:
                self.text_displacePos_x.setText(beam_res.get('displacepos')[0])
                self.text_displacePos_y.setText(beam_res.get('displacepos')[1])
                self.text_displacePos_z.setText(beam_res.get('displacepos')[2])
            else:
                self.text_displacePos_x.clear()
                self.text_displacePos_y.clear()
                self.text_displacePos_z.clear()

            if isinstance(beam_res.get('displacedpos'), list) and len(beam_res.get('displacedpos')) == 3:
                self.text_displaceDpos_x.setText(beam_res.get('displacedpos')[0])
                self.text_displaceDpos_y.setText(beam_res.get('displacedpos')[1])
                self.text_displaceDpos_z.setText(beam_res.get('displacedpos')[2])
            else:
                self.text_displaceDpos_x.clear()
                self.text_displaceDpos_y.clear()
                self.text_displaceDpos_z.clear()
            # print(self.text_particle_input_file.text())

    # @treat_err
    def generate_beam_list(self):
        res = []

        if self.text_particle_input_file.text():
            res.append(['ReadParticleDistribution', self.text_particle_input_file.text()])

            res.append(['numOfCharge', self.text_charge.text()])


            # res.append(['ParticleRestMass', self.text_mass.text()])
            # res.append(['Current', self.text_current.text()])
            # res.append(['ParticleNumber', self.text_particel_number.text()])
            #
            # res.append(['frequency', self.text_frequency.text()])
            #
            # res.append(['KneticEnergy', self.text_energy.text()])
            #
            # res.append(['twissx', self.alpha_xx_text.text(), self.beta_xx_text.text(), self.varepsilon_xx_text.text()])
            # res.append(['twissy', self.alpha_yy_text.text(), self.beta_yy_text.text(), self.varepsilon_yy_text.text()])
            # res.append(['twissz', self.alpha_zz_text.text(), self.beta_zz_text.text(), self.varepsilon_zz_text.text()])

            # res.append(['distribution', self.distribution_combo_trans.currentText(),
            #             self.distribution_combo_longi.currentText()])
            # res.append(['displacePos', self.text_displacePos_x.text(), self.text_displacePos_y.text(),
            #             self.text_displacePos_z.text()])
            # res.append(['displaceDpos', self.text_displaceDpos_x.text(), self.text_displaceDpos_y.text(),
            #             self.text_displaceDpos_z.text()])

        else:
            res.append(['numOfCharge', self.text_charge.text()])
            res.append(['ParticleRestMass', self.text_mass.text()])
            res.append(['Current', self.text_current.text()])
            res.append(['particlenumber', self.text_particel_number.text()])

            res.append(['frequency', self.text_frequency.text()])

            res.append(['KneticEnergy', self.text_energy.text()])

            res.append(['twissx', self.alpha_xx_text.text(), self.beta_xx_text.text(), self.varepsilon_xx_text.text()])
            res.append(['twissy', self.alpha_yy_text.text(), self.beta_yy_text.text(), self.varepsilon_yy_text.text()])
            res.append(['twissz', self.alpha_zz_text.text(), self.beta_zz_text.text(), self.varepsilon_zz_text.text()])
            if self.distribution_combo_trans.currentText() and self.distribution_combo_longi.currentText():
                res.append(['distribution', self.distribution_combo_trans.currentText(), self.distribution_combo_longi.currentText()])
            if self.text_displacePos_x.text() and self.text_displacePos_y.text() and self.text_displacePos_z.text():
                res.append(['displacePos', self.text_displacePos_x.text(), self.text_displacePos_y.text(), self.text_displacePos_z.text()])
            if self.text_displaceDpos_x.text() and self.text_displaceDpos_y.text() and self.text_displaceDpos_z.text():
                res.append(['displaceDpos', self.text_displaceDpos_x.text(), self.text_displaceDpos_y.text(), self.text_displaceDpos_z.text()])
        return res

    def import_beam_parameter(self):
        if not self.text_particle_input_file.text():
            QMessageBox.warning(None, 'Error', f'No dst file')
            return False


        dst_path = os.path.join(self.project_path, "InputFile", self.text_particle_input_file.text())

        if os.path.exists(dst_path):
            dst_res = read_dst(dst_path)
            # print(dst_res)
            self.text_mass.setText(str(dst_res.get('basemassinmev')))
            self.text_current.setText(str(dst_res.get('ib')))
            self.text_particel_number.setText(str(dst_res.get('number')))
            self.text_frequency.setText(str(dst_res.get('freq')))

            obj = CalTwiss(dst_path)
            obj.get_data()
            energy = round(obj.energy, self.decimals)
            self.text_energy.setText(str(energy))

            twiss = CalTwiss(dst_path).get_emit_xyz()

            self.alpha_xx_text.setText(str(round(twiss[0][0], self.decimals)))
            self.beta_xx_text.setText(str(round(twiss[0][1], self.decimals)))

            self.alpha_yy_text.setText(str(round(twiss[1][0], self.decimals)))
            self.beta_yy_text.setText(str(round(twiss[1][1], self.decimals)))

            self.alpha_zz_text.setText(str(round(twiss[2][0], self.decimals)))
            self.beta_zz_text.setText(str(round(twiss[2][1], self.decimals)))

            self.varepsilon_xx_text.setText(str(round(twiss[0][2], self.decimals)))
            self.varepsilon_yy_text.setText(str(round(twiss[1][2], self.decimals)))
            self.varepsilon_zz_text.setText(str(round(twiss[2][2], self.decimals)))
        else:
            QMessageBox.warning(None, 'Error', f'{self.text_particle_input_file.text()} does not exist')

    def save_beam(self):
        beam_list = self.generate_beam_list()
        if not beam_list:
            return False
        beam_path = os.path.join(self.project_path, 'InputFile', 'beam.txt')

        # 打开文件以写入数据
        with open(beam_path, 'w', encoding='utf-8') as file:
            # 遍历嵌套列表的每个子列表
            for sublist in beam_list:
                # 将子列表中的元素转换为字符串，并使用逗号分隔
                line = '   '.join(map(str, sublist))
                # 将每个子列表的字符串写入文件
                file.write(line + '\n')

    # @treat_err
    def onParticleInputTextChanged(self):
        text_group = [
        self.text_mass, self.text_current, self.text_current, self.text_particel_number, self.text_frequency,
        self.text_energy, self.alpha_xx_text, self.beta_xx_text, self.alpha_yy_text, self.beta_yy_text, self.alpha_zz_text, self.beta_zz_text,
        self.varepsilon_xx_text, self.varepsilon_yy_text, self.varepsilon_zz_text, self.text_displacePos_x,
        self.text_displacePos_y, self.text_displacePos_z, self.text_displaceDpos_x, self.text_displaceDpos_y,
        self.text_displaceDpos_z
        ]
        QComboBox_group = [self.distribution_combo_trans, self.distribution_combo_longi]

        particle_input_text = self.text_particle_input_file.text()
        for line_edit in text_group:
            line_edit.setReadOnly(bool(particle_input_text))
            # 设置只读文本字段的背景颜色为灰色
            if bool(particle_input_text):
                line_edit.setStyleSheet(f"QLineEdit {{ background-color:  {gray240} }}")
            else:
                line_edit.setStyleSheet("")  # 恢复默认样式
        
        for box in QComboBox_group:
            box.setEnabled(not bool(particle_input_text))  # 反转布尔值以设置只读状态

            # 设置只读文本字段的背景颜色为灰色
            if bool(particle_input_text):
                box.setStyleSheet(f"QComboBox {{ background-color:  {gray240} }}")
            else:
                box.setStyleSheet("")  # 恢复默认样式


    def inspect(self):
        if not self.text_charge.text():
            e = "Missing charge"
            QMessageBox.warning(None, 'Error', e)
            return False
        else:
            return True

    def select_dst_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        dst_file_path, _ = QFileDialog.getOpenFileName(self, "Select dst File", options=options)

        if dst_file_path:
            # print(dst_file_path)

            source_file = dst_file_path

            relative_dst_file_path = split_file(dst_file_path)[-1]
            target_folder = os.path.join(self.project_path, "InputFile")

            target_dst_file = os.path.join(self.project_path, "InputFile", relative_dst_file_path)

            #如果文件已经文件夹中
            if file_in_directory(source_file, target_folder):
                print(1)
                self.text_particle_input_file.setText(relative_dst_file_path)

            #如果文件不在文件夹中并且没有重名
            elif not file_in_directory(source_file, target_folder) and \
                split_file(source_file)[-1] != split_file(target_dst_file)[-1]:
                print(2)
                copy_file(source_file, target_folder)
                self.text_particle_input_file.setText(relative_dst_file_path)

            # 如果文件不在文件夹中并且重名了
            elif not file_in_directory(source_file, target_folder) and \
                split_file(source_file)[-1] == split_file(target_dst_file)[-1]:

                copy_file(source_file, target_folder)
                msg = QMessageBox.question(self, '文件已存在', '文件已存在，是否要覆盖？',
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

                if msg == QMessageBox.No:
                    print(3)
                    return 0
                elif msg == QMessageBox.Yes:
                    print(4)
                    copy_file(source_file, target_folder)
                    self.text_particle_input_file.setText(relative_dst_file_path)



        # particle_input_text = self.text_particle_input_file.text()
        # if particle_input_text:
        #     for line_edit in text_group:
        #         line_edit.setReadOnly(True)
        #         line_edit.setStyleSheet("background-color: rgb(240, 240, 240);")
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     main_window = PageBeam(r'C:\Users\anxin\Desktop\test')
#     main_window.fill_parameter()
#     main_window.setGeometry(800, 500, 600, 650)
#     main_window.setStyleSheet("background-color: rgb(253, 253, 253);")
#     main_window.show()
#     main_window.fill_parameter()
#     main_window.save_beam()
#     sys.exit(app.exec_())