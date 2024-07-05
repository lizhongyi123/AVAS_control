

from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QToolBar, QVBoxLayout, QWidget, QPushButton, \
    QStackedWidget, QMenu, QLabel, QLineEdit, QTextEdit,  QGridLayout, QHBoxLayout,  QFrame, QFileDialog, QGroupBox, \
    QComboBox, QSizePolicy, QDialog, QCheckBox, QButtonGroup, QMessageBox

from matplotlib.backends.backend_qtagg import FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt

from PyQt5.QtCore import pyqtSignal


class PictureDialog1(QDialog):
    resize_signal = pyqtSignal()  # ��ȷ��ʼ���Զ����ź�
    def __init__(self, project_path, func):
        super().__init__()
        self.func = func
        self.project_path = project_path
        self.figsize = (6.4, 4.6)

    def initUI(self):
        winflags = Qt.Dialog
        # �����С����ť
        winflags |= Qt.WindowMinimizeButtonHint
        # �����󻯰�ť
        winflags |= Qt.WindowMaximizeButtonHint
        # ��ӹرհ�ť
        winflags |= Qt.WindowCloseButtonHint
        # ���õ�������
        self.setWindowFlags(winflags)

        # ����һ�����ɹ�������ͼ��� QWidget
        self.setWindowTitle('��������')
        # self.setGeometry(200, 200, 640, 480)

################################
        self.fig = plt.figure(figsize=self.figsize)  # ����figure����
        self.canvas = FigureCanvas(self.fig)  # ����figure����
        self.figtoolbar = NavigationToolbar(self.canvas, self)  # ����figure������
###############################
        container_widget = QWidget(self)

        layout = QVBoxLayout()
        container_widget.setLayout(layout)

        toolbar = QToolBar()
        layout.addWidget(toolbar)


        # self.image_label = QLabel(self)

        # self.image_label.setScaledContents(True)

        #############
        layout.addWidget(self.figtoolbar)  # ��������ӵ����ڲ�����
        layout.addWidget(self.canvas)  # ������ӵ����ڲ�����
        # layout.addWidget(self.image_label)

        self.setLayout(layout)
        self.resize_signal.connect(self.on_resize)  # �����źźͲ�

    def resizeEvent(self, event):
        # �����ڱ�����ʱ�������Զ����ź�
        self.resize_signal.emit()
        return super().resizeEvent(event)


    def on_resize(self):
        self.fig.tight_layout()
        # self.fig.subplots_adjust(left=0.5 )

    def closeEvent(self, event):
        event.accept()