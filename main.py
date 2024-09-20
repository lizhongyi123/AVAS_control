import sys
import os
import time
import traceback

try:
    # 你的代码
    from user.user_qt.user_pyqt import MainWindow
    import multiprocessing
    from PyQt5.QtWidgets import QApplication

except Exception as e:
    # 打印详细的错误堆栈信息
    print("发生错误，详细信息如下：")
    traceback.print_exc()
    time.sleep(10)

if __name__ == "__main__":
    multiprocessing.freeze_support()
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())

