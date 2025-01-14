import sys
from PyQt5.QtWidgets import QProgressBar, QVBoxLayout, QWidget, QStackedLayout, QPushButton
from PyQt5.QtCore import Qt

import sys
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLabel, QApplication, QHBoxLayout


class PageOutput(QWidget):
    def __init__(self, project_path):
        super().__init__()
        self.project_path = project_path
        self.num_of_z = 0
        self.demical = 2
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()  # 主布局

        # 添加按钮布局
        button_layout = QHBoxLayout()
        self.normal_button = QPushButton("Normal Page")
        self.error_button = QPushButton("Error Page")
        button_layout.addWidget(self.normal_button)
        button_layout.addWidget(self.error_button)

        # 堆叠布局，用于切换页面
        self.stacked_layout = QStackedLayout()
        self.normal_widget = self.create_normal_widget()
        self.error_widget = self.create_error_widget()
        self.stacked_layout.addWidget(self.normal_widget)
        self.stacked_layout.addWidget(self.error_widget)

        # 将按钮布局和堆叠布局添加到主布局
        main_layout.addLayout(button_layout)
        main_layout.addLayout(self.stacked_layout)

        self.setLayout(main_layout)

        # 连接按钮点击信号到切换方法
        self.normal_button.clicked.connect(lambda: self.switch_page("normal"))
        self.error_button.clicked.connect(lambda: self.switch_page("error"))

    def create_normal_widget(self):
        normal_widget = QWidget()
        layout = QVBoxLayout()

        progress_bar = QProgressBar()
        progress_bar.setMinimum(0)
        progress_bar.setMaximum(100)
        layout.addWidget(progress_bar)

        length_label = QLabel("Length:")
        layout.addWidget(length_label)

        normal_widget.setLayout(layout)
        return normal_widget

    def create_error_widget(self):
        error_widget = QWidget()
        layout = QVBoxLayout()

        error_label = QLabel("An error occurred!")
        error_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(error_label)

        error_widget.setLayout(layout)
        return error_widget

    def switch_page(self, condition):
        if condition == "normal":
            self.stacked_layout.setCurrentWidget(self.normal_widget)
        elif condition == "error":
            self.stacked_layout.setCurrentWidget(self.error_widget)

def main():
    app = QApplication(sys.argv)
    main_window = PageOutput(r'E:\using\test_avas_qt\fileld_ciads')
    main_window.setGeometry(800, 500, 600, 650)
    main_window.setStyleSheet("background-color: rgb(253, 253, 253);")
    main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
