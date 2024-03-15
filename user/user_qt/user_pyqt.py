
import sys
sys.path.append(r'C:\Users\anxin\Desktop\AVAS_control')
from PyQt5.QtWidgets import QMainWindow, QAction, QToolBar, QVBoxLayout, QWidget, QPushButton, \
    QStackedWidget,QMenu, QLabel, QLineEdit, QTextEdit,  QGridLayout, QHBoxLayout,  QFrame, QFileDialog, QMessageBox,\
    QApplication
import os
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QStandardPaths, pyqtSignal, QSettings

from utils.readfile import read_txt, read_dst
from user.user_qt.page_beam import PageBeam
from user.user_qt.page_lattice import PageLattice
from user.user_qt.page_analysis import PageAnalysis
from user.user_qt.page_input import PageInput
from user.user_qt.page_error import PageError
from user.user_qt.page_longdistance import PageLongdistance

from user.user_qt.page_function import PageFunction
from user.user_qt.page_data import PageData
from api import basic_mulp, match_twiss, circle_match, \
    err_dyn, err_stat, err_stat_dyn
import multiprocessing
from utils.tolattice import write_mulp_to_lattice
from api import basic_env
from user.user_qt.user_defined import treat_err

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.project_path = ''
        self.basic_signal = None
        self.error_signal = None
        self.match_signal = None
        self.settings = QSettings('IMP', 'AVAS')

        self.initUI()

    def initUI(self):
        self.setGeometry(800, 500, 600, 700)
        self.setWindowTitle('AVAS')
        self.setWindowIcon(QIcon('web.png'))
        self.setStyleSheet("background-color: rgb(253, 253, 253);")  # Replace RGB values with your desired color
        main_layout = QVBoxLayout(self)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')

        newAct = QAction('New', self)
        newAct.triggered.connect(self.create_project)

        openAct = QAction('open', self)
        openAct.triggered.connect(self.open_project)

        saveAct = QAction('save', self)
        saveAct.triggered.connect(self.save_project)

        # impMenu = QMenu('Import', self)
        # impAct = QAction('Import mail', self)
        # impMenu.addAction(impAct)


        fileMenu.addAction(newAct)
        fileMenu.addAction(openAct)
        fileMenu.addAction(saveAct)
######################
        refreshMenu = menubar.addMenu('refresh')

        refresh_beam_act = QAction('beam', self)
        refresh_beam_act.triggered.connect(self.refresh_beam)

        refresh_input_act = QAction('input', self)
        refresh_input_act.triggered.connect(self.refresh_input)

        refresh_lattice_act = QAction('lattice', self)
        refresh_lattice_act.triggered.connect(self.refresh_lattice)

        refreshMenu.addAction(refresh_beam_act)
        refreshMenu.addAction(refresh_input_act)
        refreshMenu.addAction(refresh_lattice_act)

########################
        runMenu = menubar.addMenu('run')

        run_act = QAction('run', self)
        run_act.triggered.connect(self.run)

        run_stop_act = QAction('stop', self)
        run_stop_act.triggered.connect(self.stop)


        runMenu.addAction(run_act)
        runMenu.addAction(run_stop_act)

########################
        toolbar = QToolBar("工具栏标题")
        self.addToolBar(toolbar)

        self.page_beam = PageBeam(self.project_path)
        self.page_lattice = PageLattice(self.project_path)
        self.page_analysis = PageAnalysis(self.project_path)
        self.page_input = PageInput(self.project_path)
        self.page_function = PageFunction(self.project_path)
        self.page_data = PageData(self.project_path)
        self.page_error = PageError(self.project_path)
        self.page_longdistance = PageLongdistance(self.project_path)


        page_beam_action = QAction("beam", self)
        page_lattice_action = QAction("lattice", self)
        page_analysis_action = QAction('analysis', self)
        page_input_action = QAction('input', self)
        page_function_action = QAction('function', self)
        page_data_action = QAction('data', self)
        page_error_action = QAction('error', self)
        page_longdistance_action = QAction('long distance', self)


        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.page_beam)
        self.stacked_widget.addWidget(self.page_lattice)
        self.stacked_widget.addWidget(self.page_analysis)
        self.stacked_widget.addWidget(self.page_input)
        self.stacked_widget.addWidget(self.page_function)
        self.stacked_widget.addWidget(self.page_data)
        self.stacked_widget.addWidget(self.page_error)
        # self.stacked_widget.addWidget(self.page_longdistance)


        page_beam_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.page_beam))
        page_lattice_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.page_lattice))
        page_analysis_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.page_analysis))
        page_input_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.page_input))
        page_function_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.page_function))

        page_data_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.page_data))
        self.stacked_widget.currentChanged.connect(self.handle_page_change)

        page_error_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.page_error))
        # page_longdistance_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.page_longdistance))

        toolbar.addAction(page_beam_action)
        toolbar.addAction(page_lattice_action)
        toolbar.addAction(page_input_action)
        toolbar.addAction(page_function_action)
        toolbar.addAction(page_data_action)
        toolbar.addAction(page_analysis_action)
        toolbar.addAction(page_error_action )

        # toolbar.addAction(page_longdistance_action)


        frame = QFrame()  # 创建外边框小部件

        # 设置框架的边框样式


        hbox = QHBoxLayout()

        label = QLabel("project path")
        # label.setStyleSheet("background-color: rgb(225, 225, 225); border: 0px solid black;")

        self.path_text = QLineEdit("")
        self.path_text.setReadOnly(True)  # 设置为只读模式

        hbox.addWidget(label)
        hbox.addWidget(self.path_text)
        self.path_text.setStyleSheet("background-color: rgb(240, 240, 240);")

        # 创建用于表示线的QFrame
        line_frame = QFrame()
        line_frame.setFrameShape(QFrame.HLine)  # 设置为水平线
        line_frame.setFrameShadow(QFrame.Sunken)  # 设置阴影效果

        central_widget = QWidget()  # 创建一个中央部件

        central_layout = QVBoxLayout()  # 在中央部件上设置一个垂直布局
        central_layout.addLayout(hbox)  # 将带有边框的框架添加到布局中
        central_layout.addWidget(line_frame)  # 将表示线的框架添加到布局中
        central_layout.addWidget(self.stacked_widget)  # 将堆叠小部件添加到布局中

        self.page_function.basic_signal.connect(self.get_basic_signal)

        self.page_function.error_signal.connect(self.get_error_signal)
        self.page_function.match_signal.connect(self.get_match_signal)

        self.basci_mulp_process = multiprocessing.Process()
        self.basci_env_process = multiprocessing.Process()

        self.err_process = multiprocessing.Process()
        self.match_process = multiprocessing.Process()

        central_widget.setLayout(central_layout)  # 将布局设置给中央部件

        self.setCentralWidget(central_widget)  # 将中央部件设置为主窗口的中央部件
        self.show()
        self.initialize_page()



    # @treat_err

    def create_project(self):
        desktop_path = QStandardPaths.writableLocation(QStandardPaths.DesktopLocation)
        default_folder_path = desktop_path

        new_folder_path, _ = QFileDialog.getSaveFileName(self, "Create New Folder", default_folder_path, filter="Folders (*)")

        if new_folder_path:
            os.makedirs(new_folder_path)
            input_file = os.path.join(new_folder_path, 'InputFile')
            output_file = os.path.join(new_folder_path, 'OutputFile')
            os.makedirs(input_file)
            os.makedirs(output_file)

            self.project_path = new_folder_path
            self.path_text.setText(self.project_path)
            self.create_basic_txt_file()
            self.refresh_page_project_path()
            self.page_fill_parameter()

        self.settings.setValue("lastProjectPath", self.project_path)

    # @treat_err
    def open_project(self):
        # desktop_path = QStandardPaths.writableLocation(QStandardPaths.DesktopLocation)
        # default_folder_path = desktop_path
        #
        # folder_path, _ = QFileDialog.getOpenFileName(self, "Create New Folder", default_folder_path,
        #                                                  filter="Folders (*)")
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        folder_path = QFileDialog.getExistingDirectory(self, "Select Directory", options=options)

        if folder_path:
            self.project_path = folder_path
            self.path_text.setText(self.project_path)

            # self.create_backup_file()
            self.refresh_page_project_path()
            self.page_fill_parameter()
        self.settings.setValue("lastProjectPath", self.project_path)

    # @treat_err
    def refresh_page_project_path(self):
        self.page_beam.updatePath(self.project_path)
        self.page_lattice.updatePath(self.project_path)
        self.page_input.updatePath(self.project_path)
        self.page_function.updatePath(self.project_path)
        self.page_data.updatePath(self.project_path)
        self.page_analysis.updatePath(self.project_path)
        self.page_error.updatePath(self.project_path)
        self.page_longdistance.updatePath(self.project_path)

    @treat_err
    def page_fill_parameter(self):
        self.page_beam.fill_parameter()
        self.page_lattice.fill_parameter()
        self.page_input.fill_parameter()
        self.page_data.fill_parameter()
        self.page_longdistance.fill_parameter()

    @treat_err
    def save_project(self):
        if not self.project_path:
            raise Exception('No project')

        self.page_beam.save_beam()
        self.page_lattice.save_all_lattice()
        self.page_input.save_input(self.basic_signal)


    @treat_err
    def create_basic_txt_file(self):
        beam = os.path.join(self.project_path, "InputFile", "beam.txt")
        input = os.path.join(self.project_path, "InputFile", "input.txt")
        lattice = os.path.join(self.project_path, "InputFile", "lattice.txt")
        lattice_mulp = os.path.join(self.project_path, "InputFile", "lattice_mulp.txt")


        with open(beam, "w") as file:
            file.write("")
        with open(input, "w") as file:
            file.write("")
        with open(lattice, "w") as file:
            file.write("")
        with open(lattice_mulp, "w") as file:

            file.write("")
    @treat_err
    def run(self ):
        res = self.inspect()
        if not res:
            return None
        self.save_project()
        if self.match_signal == 'match_twiss_ini':
            self.func_match(1, 1)
        elif self.match_signal == 'match_twiss':
            self.func_match(1, 0)
        elif self.match_signal == 'period_match':
            self.func_match(0)
        
        elif self.error_signal == 'stat_error':
            print('stat')
            self.func_err('stat')

        elif self.error_signal == 'dyn_error':
            self.func_err('dyn')

        elif self.error_signal == 'stat_dyn':
            self.func_err('stat_dyn')
        
        elif self.basic_signal == 'basic_mulp':
            lattice_mulp_path = os.path.join(self.project_path, 'InputFile', 'lattice_mulp.txt')
            lattice_path = os.path.join(self.project_path, 'InputFile', 'lattice.txt')
            write_mulp_to_lattice(lattice_mulp_path, lattice_path)
            self.func_basic_mulp()
        elif self.basic_signal == 'basic_env':
            self.func_basic_env()
        else:
            print('Nothing was chosen')

        self.refresh_lattice()
    @treat_err
    def stop(self):
        if self.basci_mulp_process.is_alive():
            self.basci_mulp_process.terminate()
            self.basci_mulp_process.join()

        elif self.err_process.is_alive():
            self.err_process.terminate()
            self.err_process.join()

        elif self.match_process.is_alive():
            self.match_process.terminate()
            self.match_process.join()
        print('结束进程')

#################################
    #此处对应的是run和stop对应的函数

    def func_basic_mulp(self):
        print("start simulation")
        if not self.basci_mulp_process.is_alive():
            self.basci_mulp_process = multiprocessing.Process(target=basic_mulp, args=(self.project_path,))
            self.basci_mulp_process.start()


    def func_basic_env(self):
        print("start simulation")
        lattice_env = os.path.join(self.project_path, 'InputFile', 'lattice_env.txt')
        if not self.basci_env_process.is_alive():
            self.basci_env_process = multiprocessing.Process(target=basic_env, args=(self.project_path, lattice_env))
            self.basci_env_process.start()


    #误差分析
    def func_err(self, err_type):
        print("start err")
        if not self.err_process.is_alive():
            if err_type == 'stat':
                target = err_stat
            elif err_type == 'dyn':
                target = err_dyn
            elif err_type == 'stat_dyn':
                target = err_stat_dyn

            self.err_process = multiprocessing.Process(target=target, args=(self.project_path,))
            self.err_process.start()

    def func_match(self, match_choose, use_ini=0):
        print(match_choose)
        print("start match")
        if not self.match_process.is_alive():

            if match_choose == 0:
                # 周期匹配
                target = circle_match
                args = (self.project_path,)


            elif match_choose == 1:
                # twiss command匹配
                target = match_twiss
                args = (self.project_path, use_ini)
            else:
                return 0

            self.match_process = multiprocessing.Process(target=target, args=args)
            self.match_process.start()
            # 启用监测器，开始检查进程状态


    def check_basci_mulp_process_status(self):
        if self.basci_mulp_process is not None:
            if self.basci_mulp_process.is_alive():
                # 进程仍在运行
                self.button_simulation.setEnabled(False)  # 禁用按钮
            else:
                # 进程已结束
                self.button_simulation.setEnabled(True)  # 启用按钮
                # 停止监测器



#####################################
    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


    def refresh_beam(self):
        self.page_beam.fill_parameter()

    @treat_err
    def refresh_lattice(self):
        self.page_lattice.fill_parameter()

    @treat_err
    def refresh_input(self):
        self.page_input.fill_parameter()

    def get_basic_signal(self, signal):
        self.basic_signal = signal


    def get_error_signal(self, signal):
        self.error_signal = signal
        print(signal)


    def get_match_signal(self, signal):
        self.match_signal = signal

    def initialize_page(self):
        if self.settings.value("lastProjectPath", None) is None:
            pass

        else:
            self.project_path = self.settings.value("lastProjectPath", "")
            self.path_text.setText(self.project_path)

            if os.path.exists(self.project_path):
                print("存在", self.project_path)
                self.refresh_page_project_path()
                self.page_fill_parameter()

    def inspect(self):
        r1 = self.page_beam.inspect()
        r2 = self.page_lattice.inspect()
        r3 = self.page_input.inspect()
        r4 = self.page_function.inspect()
        return all([r1, r2, r3, r4])

    def handle_page_change(self, index):
        # print(1)
        # 获取当前显示的页面名称
        current_page_name = self.stacked_widget.widget(index).objectName()
        # print(current_page_name)
        # 如果当前页面是 'data'，则设置窗口大小
        if current_page_name == 'page_data':
            self.resize(1200, 700)  # 修改为适当的尺寸
        else:
            self.resize(600, 700)  # 恢复到默认尺寸或其他尺寸

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())

