import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QToolBar, QVBoxLayout, QWidget, QPushButton, \
    QStackedWidget, QMenu, QLabel, QLineEdit, QTextEdit, QGridLayout, QHBoxLayout, QFrame, QFileDialog, QGroupBox, \
    QComboBox, QSizePolicy, QCheckBox, QMessageBox

import os

from PyQt5.QtCore import Qt, pyqtSignal
from utils.readfile import read_txt, read_dst
from user.user_qt.user_defined import treat_err, treat_err2, gray240
from utils.inputconfig import InputConfig

class PageInput(QWidget):
    basic_signal = pyqtSignal(str)

    def __init__(self, project_path):
        super().__init__()
        self.project_path = project_path
        # self.multithreading_num = -1

        self.initUI()

    def initUI(self):
        # print(self.project_path)
        self.setStyleSheet("background-color: rgb(250, 250, 250);")

        layout = QHBoxLayout()


        vertical_group_box_main = QGroupBox("Operation setting")


        vertical_layout_main = QVBoxLayout()



        cb_picnic = QCheckBox('PICNIC', self)


        vertical_group_box_main.setLayout(vertical_layout_main)

        layout.addWidget(vertical_group_box_main)
        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = PageInput(r'C:\Users\anxin\Desktop\comparison\avas_test')
    main_window.setGeometry(800, 500, 600, 650)
    main_window.setStyleSheet("background-color: rgb(253, 253, 253);")
    main_window.show()
    sys.exit(app.exec_())