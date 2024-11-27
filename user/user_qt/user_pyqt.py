
import sys
import time

sys.path.append(r'C:\Users\anxin\Desktop\AVAS_control')
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QAction, QToolBar, QVBoxLayout, QWidget, QPushButton, \
    QStackedWidget,QMenu, QLabel, QLineEdit, QTextEdit,  QGridLayout, QHBoxLayout,  QFrame, QFileDialog, QMessageBox,\
    QApplication
import os
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QStandardPaths, pyqtSignal, QSettings, QThread

from utils.readfile import read_txt, read_dst
from user.user_qt.page_beam import PageBeam
from user.user_qt.page_lattice import PageLattice
from user.user_qt.page_analysis import PageAnalysis
from user.user_qt.page_input import PageInput
from user.user_qt.page_error import PageError
from user.user_qt.page_longdistance import PageLongdistance
from user.user_qt.page_match import PageMatch
from user.user_qt.page_others import PageOthers
from user.user_qt.page_output import PageOutput


from user.user_qt.page_data import PageData
from api import basic_mulp, match_twiss, circle_match, \
    err_dyn, err_stat, err_stat_dyn
import multiprocessing
from api import basic_env
from user.user_qt.user_defined import treat_err
from user.user_qt.page_acc import PageAccept
from send2trash import send2trash
from utils.iniconfig import IniConfig
from apis.qt_api.SimMode import SimMode
from apis.qt_api.createbasicfile import CreateBasicProject
from core.MultiParticle import MultiParticle
class MultiParticleThread(QThread):
    finished = pyqtSignal()  # 任务完成信号

    def __init__(self, project_path):
        super().__init__()
        self.project_path = project_path
        self.running = True
        self.multiparticle_obj = MultiParticle(self.project_path)

    def run(self):
        # 调用 MultiParticle 的 run 方法
        try:
            self.multiparticle_obj.run()
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.finished.emit()  # 任务完成时发出信号

    def stop(self):
        # 停止 MultiParticle 的逻辑
        self.running = False
        self.multiparticle_obj.stop()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.project_path = ''

        self.input_signal = None
        self.match_signal = None
        self.error_signal = None

        self.task_thread = None
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
        runMenu.addAction(run_stop_act)

########################
        toolbar = QToolBar("工具栏标题")
        self.addToolBar(toolbar)

        self.page_beam = PageBeam(self.project_path)
        self.page_lattice = PageLattice(self.project_path)
        self.page_analysis = PageAnalysis(self.project_path)
        self.page_input = PageInput(self.project_path)
        # self.page_function = PageFunction(self.project_path)
        self.page_match = PageMatch(self.project_path)
        self.page_others = PageOthers(self.project_path)

        self.page_data = PageData(self.project_path)
        self.page_error = PageError(self.project_path)
        # self.page_longdistance = PageLongdistance(self.project_path)
        self.page_output = PageOutput(self.project_path)
        self.page_accept = PageAccept(self.project_path)



        page_beam_action = QAction("beam", self)
        page_lattice_action = QAction("lattice", self)
        page_analysis_action = QAction('analysis', self)
        page_input_action = QAction('input', self)
        # page_function_action = QAction('function', self)
        page_match_action = QAction('match', self)
        page_others_action = QAction('others', self)

        page_data_action = QAction('data', self)
        page_error_action = QAction('error', self)
        page_output_action = QAction('output', self)
        page_accept_action = QAction('accept', self)

        # page_longdistance_action = QAction('long distance', self)


        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.page_beam)
        self.stacked_widget.addWidget(self.page_lattice)
        self.stacked_widget.addWidget(self.page_analysis)
        self.stacked_widget.addWidget(self.page_input)
        # self.stacked_widget.addWidget(self.page_function)
        self.stacked_widget.addWidget(self.page_match)

        self.stacked_widget.addWidget(self.page_data)
        self.stacked_widget.addWidget(self.page_error)
        self.stacked_widget.addWidget(self.page_output)
        self.stacked_widget.addWidget(self.page_accept)

        # self.stacked_widget.addWidget(self.page_others)

        # self.stacked_widget.addWidget(self.page_longdistance)


        page_beam_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.page_beam))
        page_lattice_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.page_lattice))
        page_analysis_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.page_analysis))
        page_input_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.page_input))
        # page_function_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.page_function))
        page_match_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.page_match))

        page_data_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.page_data))
        self.stacked_widget.currentChanged.connect(self.handle_page_change)

        page_error_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.page_error))
        # page_others_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.page_others))
        page_output_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.page_output))
        page_accept_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.page_accept))

        # page_longdistance_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.page_longdistance))

        toolbar.addAction(page_beam_action)
        toolbar.addAction(page_lattice_action)
        toolbar.addAction(page_input_action)
        # toolbar.addAction(page_function_action)
        toolbar.addAction(page_match_action)
        toolbar.addAction(page_error_action)

        toolbar.addAction(page_output_action)
        toolbar.addAction(page_data_action)
        toolbar.addAction(page_analysis_action)
        toolbar.addAction(page_accept_action)

        # toolbar.addAction(page_others_action)

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

        self.page_input.input_signal.connect(self.get_input_signal)
        #
        self.page_error.error_signal.connect(self.get_error_signal)
        self.page_match.match_signal.connect(self.get_match_signal)

        # self.basci_mulp_process = multiprocessing.Process()
        # self.basci_env_process = multiprocessing.Process()
        # self.err_process = multiprocessing.Process()
        # self.match_process = multiprocessing.Process()
        self.sim_process = multiprocessing.Process()
        central_widget.setLayout(central_layout)  # 将布局设置给中央部件

        self.setCentralWidget(central_widget)  # 将中央部件设置为主窗口的中央部件
        self.show()
        self.initialize_page()



    # @treat_err

    def create_project(self):
        desktop_path = QStandardPaths.writableLocation(QStandardPaths.DesktopLocation)
        default_folder_path = desktop_path

        new_folder_path, _ = QFileDialog.getSaveFileName(self, "Create New Folder", default_folder_path, filter="Folders (*)")
        new_folder_path = os.path.normpath(new_folder_path)

        if new_folder_path:

            self.project_path = new_folder_path
            self.path_text.setText(self.project_path)
            self.refresh_page_project_path()


            item = {
                "projectPath": self.project_path,
                "beamKeys": [],
                "inputkeys": []
            }
            create_project_obj = CreateBasicProject(item, 'qt')
            res = create_project_obj.create_project()
            if res['code'] == -1:
                raise Exception(res["data"]['msg'])
                return -1
            self.page_fill_parameter()

        self.settings.setValue("lastProjectPath", self.project_path)

    @treat_err
    def open_project(self):
        # desktop_path = QStandardPaths.writableLocation(QStandardPaths.DesktopLocation)
        # default_folder_path = desktop_path
        #
        # folder_path, _ = QFileDialog.getOpenFileName(self, "Create New Folder", default_folder_path,
        #                                                  filter="Folders (*)")
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        folder_path = QFileDialog.getExistingDirectory(self, "Select Directory", options=options)
        folder_path = os.path.normpath(folder_path)

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
        # self.page_function.updatePath(self.project_path)
        self.page_match.updatePath(self.project_path)

        self.page_data.updatePath(self.project_path)
        self.page_analysis.updatePath(self.project_path)
        self.page_error.updatePath(self.project_path)
        # self.page_longdistance.updatePath(self.project_path)
        self.page_others.updatePath(self.project_path)
        self.page_output.updatePath(self.project_path)
        self.page_accept.updatePath(self.project_path)




    @treat_err
    def page_fill_parameter(self):
        self.page_beam.fill_parameter()
        self.page_lattice.fill_parameter()
        self.page_input.fill_parameter()
        # self.page_longdistance.fill_parameter()
        self.page_error.fill_parameter()

    @treat_err
    def save_project(self):
        if not self.project_path:
            raise Exception('No project')

        self.page_beam.save_beam()
        self.page_lattice.save_all_lattice()
        self.page_input.save_input()
        self.save_ini()

    def save_ini(self):
        item = {"projectPath": self.project_path}
        ini_obj = IniConfig()

        set_dict = {'input': self.input_signal,
                    'match': self.match_signal,
                    'error': self.error_signal,
        }
        set_dict = {k: v for k, v in set_dict.items() if v}
        res = ini_obj.set_param(**set_dict)
        if res["code"] == -1:
            raise Exception(res['data']['msg'])

        ini_path = os.path.join(self.project_path, "inputFile", 'ini.ini')
        res = ini_obj.write_to_file(item)
        if res["code"] == -1:
            raise Exception(res['data']['msg'])




    def run(self):
        self.stop()
        # res = self.inspect()
        # if not res:
        #     return None
        self.save_project()

        if not self.task_thread or not self.task_thread.isRunning():
            self.task_thread = MultiParticleThread(self.project_path)
            self.task_thread.finished.connect(self.on_task_finished)
            self.task_thread.start()
        # self.refresh_lattice()

    def on_task_finished(self):
        print("Task finished.")


    # def run(self):
    #         # delay_ms = 3000  # 延迟 2000 毫秒（即 2 秒）
    #         # QTimer.singleShot(delay_ms, lambda: self.activate_output('basic_mulp'))
    #         try:
    #             self.page_data.fill_parameter()
    #         except Exception as e:
    #             print(e)
    #
    #
    #     # self.refresh_lattice()


    def activate_output(self, signal):

        if signal == "basic_mulp":
            self.runsignal = os.path.join(self.project_path, 'OutputFile', 'runsignal.txt')

            with open(self.runsignal, 'w') as f:
                f.write('1')
            try:
                # dataset_path = os.path.join(self.project_path, 'OutputFile', 'DataSet.txt')
                dataset_path = os.path.join(self.project_path, 'OutputFile', 'DataSet.txt').replace('/', '\\')
                # print(dataset_path)
                send2trash(dataset_path)
            except:
                pass

            try:
                print(428)
                self.page_output.update_progress()
            except Exception as e:
                print(e)


    @treat_err
    def stop(self):
        if self.task_thread and self.task_thread.isRunning():
            self.task_thread.stop()
            self.task_thread.wait()  # 等待线程终止
            print("Task stopped.")

        # if self.basci_mulp_process.is_alive():
        #     self.basci_mulp_process.terminate()
        #     self.basci_mulp_process.join()
        #
        # elif self.err_process.is_alive():
        #     self.err_process.terminate()
        #     self.err_process.join()
        #
        # elif self.match_process.is_alive():
        #     self.match_process.terminate()
        #     self.match_process.join()
        self.page_output.stop_update_progress()
        print('结束进程')

#################################

    def func_sim(self):
        obj = SimMode(self.project_path)
        if not self.sim_process.is_alive():
            self.sim_process = multiprocessing.Process(target=obj.run, )
            self.sim_process.start()

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

    def get_input_signal(self, signal):
        self.input_signal = signal
        print(self.input_signal)
    def get_error_signal(self, signal):
        self.error_signal = signal
        print(self.error_signal)
    def get_match_signal(self, signal):
        self.match_signal = signal
        print(self.match_signal)

    def initialize_page(self):
        print(self.settings.value("lastProjectPath", None))
        if self.settings.value("lastProjectPath", None) is None:
            pass

        else:
            self.project_path = self.settings.value("lastProjectPath", "")
            print(self.project_path)
            self.path_text.setText(self.project_path)

            if os.path.exists(self.project_path):

                self.refresh_page_project_path()
                self.page_fill_parameter()

    def inspect(self):
        r1 = self.page_beam.inspect()
        r2 = self.page_lattice.inspect()
        r3 = self.page_input.inspect()
        # r4 = self.page_function.inspect()
        return all([r1, r2, r3])

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

