import sys
import os
import time
import traceback
from PyQt5.QtWidgets import QApplication, QMessageBox
import multiprocessing
# try:
#     # 你的代码
#     from user.user_qt.user_pyqt import MainWindow
#     import multiprocessing
#     from PyQt5.QtWidgets import QApplication
#
# except Exception as e:
#     # 打印详细的错误堆栈信息
#     with open("errli.txt", "w") as f:
#         f.write(str(e))
#     print("发生错误，详细信息如下：")
#     traceback.print_exc()

if __name__ == "__main__":
    multiprocessing.freeze_support()

    def exception_handler(type, value, traceback):
        # 显示错误信息
        QMessageBox.critical(None, "Critical Error", f"An unexpected error occurred:\n{value}")
        # 输出到控制台（调试用）
        sys.__excepthook__(type, value, traceback)


    # 将全局异常处理器设置为自定义的函数
    sys.excepthook = exception_handler

    from user.user_qt.user_pyqt import MainWindow
    import multiprocessing
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())

