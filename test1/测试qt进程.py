from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtCore import QThread, pyqtSignal
import sys
import time
from core.MultiParticle import MultiParticle  # 假设 MultiParticle 在 core 目录下
import multiprocessing
class MultiParticleThread(QThread):
    finished = pyqtSignal()  # 任务完成信号

    def __init__(self, project_path):
        super().__init__()
        self.project_path = project_path
        self.running = True
        self.multiparticle_obj = MultiParticle1(self.project_path)

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


class MultiParticle1():
    def __init__(self, project_path):
        self.project_path = project_path
        self.multiparticle_obj = MultiParticle(self.project_path)

    def run(self, ):
        self.process1 = multiprocessing.Process(target=self.multiparticle_obj.run)
        self.process1.start()
        self.process1.join()
        print(40, '大发大师傅', self.multiparticle_obj.process)

    def stop(self):
        print("进程结束")
        # 使用 terminate 强制终止子进程
        if self.process1 and self.process1.is_alive():
            self.stop_flag = True
            # self.multiparticle_obj.stop()
            self.process1.terminate()
            self.process1.join(timeout=3)  # 使用超时等待最多 5 秒
            if self.process1.is_alive():
                print("Process did not terminate within timeout")
        print(self.multiparticle_obj.process)


class AppDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.task_thread = None
        self.project_path = r"C:\Users\shliu\Desktop\test1113\test2"

    def initUI(self):
        self.setWindowTitle('Task Control Panel')
        self.setGeometry(100, 100, 300, 150)

        layout = QVBoxLayout()

        self.start_btn = QPushButton('Start Task', self)
        self.start_btn.clicked.connect(self.start_task)
        layout.addWidget(self.start_btn)

        self.stop_btn = QPushButton('Stop Task', self)
        self.stop_btn.clicked.connect(self.stop_task)
        layout.addWidget(self.stop_btn)

        self.setLayout(layout)

    def start_task(self):
        if not self.task_thread or not self.task_thread.isRunning():
            self.task_thread = MultiParticleThread(self.project_path)
            self.task_thread.finished.connect(self.on_task_finished)
            self.task_thread.start()

    def stop_task(self):
        if self.task_thread and self.task_thread.isRunning():
            self.task_thread.stop()
            self.task_thread.wait()  # 等待线程终止
            print("Task stopped.")

    def on_task_finished(self):
        print("Task finished.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = AppDemo()
    demo.show()
    sys.exit(app.exec_())

