

from user.user_qt.user_pyqt import MainWindow
import multiprocessing

from PyQt5.QtWidgets import QApplication
import sys

if __name__ == "__main__":
    multiprocessing.freeze_support()
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())
