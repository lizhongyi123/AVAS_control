import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QMessageBox

from PyQt5.QtCore import QStandardPaths, pyqtSignal, QSettings, QThread
from core.MultiParticle import MultiParticle
from core.MultiParticleEngine import MultiParticleEngine
class SimThread(QThread):
    def __init__(self, ):
        super().__init__()
        self.engine = MultiParticleEngine()

    def run(self):
        path = r"C:\Users\shliu\Desktop\test_lattice"
        item = {"project_path": path, "mulp_engine": self.engine}
        obj = MultiParticle(item)
        obj.run()

    def stop(self):
        path = r"C:\Users\shliu\Desktop\test_lattice"
        item = {"project_path": path, "mulp_engine": self.engine}
        obj = MultiParticle(item)
        obj.stop()

        self.quit()  # 让 QThread 退出
        self.wait()  # 确保线程彻底结束

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("打开 / 关闭 示例")
        self.setGeometry(100, 100, 300, 100)

        # 创建按钮
        self.open_button = QPushButton("打开")
        self.close_button = QPushButton("关闭")

        # 设置按钮点击事件
        self.open_button.clicked.connect(self.open_clicked)
        self.close_button.clicked.connect(self.close_clicked)

        # 垂直布局
        layout = QVBoxLayout()
        layout.addWidget(self.open_button)
        layout.addWidget(self.close_button)

        self.setLayout(layout)

    def open_clicked(self):


        self.sim_thread = SimThread()
        self.sim_thread.start()

    def close_clicked(self):
        self.sim_thread.stop()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
