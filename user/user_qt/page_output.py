import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QProgressBar, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer
from dataprovision.datasetparameter import DatasetParameter
from dataprovision.latticeparameter import LatticeParameter
import os

import sys
from PyQt5.QtWidgets import QMainWindow, QAction, QToolBar, QVBoxLayout, QWidget, QPushButton, \
    QStackedWidget,QMenu, QLabel, QLineEdit, QTextEdit,  QGridLayout, QHBoxLayout,  QFrame, QFileDialog, QMessageBox,\
    QApplication,QHBoxLayout


class PageOutput(QWidget):
    def __init__(self, project_path):
        super().__init__()
        self.project_path = project_path
        self.num_of_z = 0
        self.demical = 2
        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: rgb(250, 250, 250);")

        layout = QVBoxLayout()

        self.layout_1 = QHBoxLayout()

        label_progress = QLabel("Progress")
        self.label_location = QLabel()

        self.layout_1.addWidget(label_progress)
        self.layout_1.addWidget(self.label_location)


        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)

        layout.addLayout(self.layout_1)
        layout.addWidget(self.progress_bar)
        layout.addStretch(1)


        # 初始化进度条的值
        self.progress_value = 0
        self.progress_bar.setValue(self.progress_value)
        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)

    # def update_progress(self):
    #     # 每次调用增加10%的进度
    #     self.progress_value += 10
    #     self.progress_bar.setValue(self.progress_value)
    #
    #     # 如果进度达到100%，则重置为0
    #     if self.progress_value >= 100:
    #         return 0
    def update_progress(self):
        self.timer.start(1000)  # 定时器每隔1000毫秒（1秒）触发一次

        if True:
            dataset_path = os.path.join(self.project_path, 'OutputFile', 'DataSet.txt')
            lattice_path = os.path.join(self.project_path, 'InputFile', 'lattice_mulp.txt')

            if os.path.exists(dataset_path):
                dataset_obj = DatasetParameter(dataset_path)
                dataset_obj.get_parameter()

                z = dataset_obj.z
                num_of_z_this = len(z)
                if self.num_of_z != num_of_z_this:

                    self.num_of_z = num_of_z_this
                    lattice_obj = LatticeParameter(lattice_path)
                    lattice_obj.get_parameter()

                    # location = float(dataset_obj.z[-1])
                    total_length = sum(lattice_obj.v_len)
                    self.label_location.setText(f"{round(z[-1], self.demical)}/{total_length}")
                    ratio = z[-1] / total_length
                    self.progress_bar.setValue(int(ratio*100))
                elif self.num_of_z == num_of_z_this:
                    self.timer.stop()
                    return 0

    def updatePath(self, new_path):
        self.project_path = new_path


def main():
    app = QApplication(sys.argv)
    main_window = PageOutput(r'C:\Users\anxin\Desktop\comparison\avas_test')
    main_window.setGeometry(800, 500, 600, 650)
    main_window.setStyleSheet("background-color: rgb(253, 253, 253);")
    main_window.show()
    main_window.update_progress()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
