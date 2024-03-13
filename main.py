

from user.user_qt.user_pyqt import MainWindow
import multiprocessing

from PyQt5.QtWidgets import QApplication

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if __name__ == "__main__":
    multiprocessing.freeze_support()
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())
