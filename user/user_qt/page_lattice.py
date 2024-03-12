import time

from PyQt5.QtWidgets import QApplication, QMainWindow, QAction,\
    QVBoxLayout, QWidget, QPushButton, QLineEdit, QTextEdit, QHBoxLayout, QToolBar, QStackedWidget, \
    QButtonGroup, QShortcut,QMessageBox
import sys
import os

from lattice_file.lattice_ide import CustomCodeEdit, MySyntaxHighlighter, MyFoldDetector
from pyqode.core import api, modes, panels
from user_defined import treat_err
class PageLattice(QWidget):
    def __init__(self, project_path):
        super().__init__()
        self.project_path = project_path
        self.lattice_mulp_path = ''
        self.lattice_env_path = ''
        self.ctrl_pressed = False  # 添加一个标志来跟踪Ctrl键是否被按住
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        hbox_control = QHBoxLayout()

        self.button_save = QPushButton("Save")
        self.button_save.setStyleSheet("background-color: rgb(240, 240, 240); border: 1px solid black;")
        self.button_save.clicked.connect(self.save_file)
        self.text_file_path = QLineEdit()
        self.text_file_path.setReadOnly(True)


        hbox_control.addWidget(self.button_save)
        hbox_control.addWidget(self.text_file_path)
########################################################################


        hbox_cut = QHBoxLayout()
        self.button_lattice = QPushButton("lattice_mulp")
        self.button_match_lattice = QPushButton("lattice_env")
        # self.button_match_result = QPushButton("match result")
        # self.button_match_twiss = QPushButton("match twiss")
        self.button_input_twiss = QPushButton("input twiss")


        hbox_cut.addWidget(self.button_lattice)
        hbox_cut.addWidget(self.button_match_lattice)
        # hbox_cut.addWidget(self.button_match_result)
        # hbox_cut.addWidget(self.button_match_twiss)
        hbox_cut.addWidget(self.button_input_twiss)

        self.button_group = QButtonGroup()
        self.button_group.addButton(self.button_lattice)
        self.button_group.addButton(self.button_match_lattice)
        # self.button_group.addButton(self.button_match_result)
        # self.button_group.addButton(self.button_match_twiss)
        self.button_group.addButton(self.button_input_twiss)

        self.button_group.setExclusive(True)

        self.button_lattice.setCheckable(True)
        self.button_match_lattice.setCheckable(True)
        # self.button_match_result.setCheckable(True)
        # self.button_match_twiss.setCheckable(True)
        self.button_input_twiss.setCheckable(True)

###########################################################
        self.text_lattice = CustomCodeEdit()
        self.text_match_lattice = QTextEdit()
        # self.text_match_result = QTextEdit()
        # self.text_match_twiss = QTextEdit()

        self.text_input_twiss = QTextEdit()


        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.text_lattice)
        self.stacked_widget.addWidget(self.text_match_lattice)
        # self.stacked_widget.addWidget(self.text_match_result)
        # self.stacked_widget.addWidget(self.text_match_twiss)
        self.stacked_widget.addWidget(self.text_input_twiss)


        self.button_lattice.clicked.connect(self.lattice_click)
        self.button_match_lattice.clicked.connect(self.match_lattice_click)
        # self.button_match_result.clicked.connect(self.match_result_click)
        # self.button_match_twiss.clicked.connect(self.match_twiss_click)
        self.button_input_twiss.clicked.connect(self.input_twiss_click)




########################################################
        layout.addLayout(hbox_control)
        layout.addLayout(hbox_cut)
        layout.addWidget(self.stacked_widget)

        self.setLayout(layout)


        # # 连接文本输入框的文本更改信号到处理函数

        self.ignore_text_changed = False


        if True:
            self.text_lattice.modes.append(modes.CodeCompletionMode())
            sh_text_lattice = self.text_lattice.modes.append(MySyntaxHighlighter(self.text_lattice.document()))
            sh_text_lattice.fold_detector = MyFoldDetector()
            self.text_lattice.panels.append(panels.FoldingPanel())




        # 连接光标位置改变事件
        # self.text_lattice.cursorPositionChanged.connect(self.cursorPositionChanged)
        # self.text_lattice.wheelEvent = self.wheelEvent1
        # self.text_lattice.installEventFilter(self)  # 安装事件过滤器
    #     self.text_lattice.keyPressEvent = self.keyPressEvent
    #
    # def keyPressEvent(self, event):
    #     if event.key()==(Qt.Key_Control and Qt.Key_Z):
    #         cursor = self.text_lattice.textCursor()
    #         cursor.movePosition(QTextCursor.StartOfBlock)  # 移动到当前行的开头
    #         cursor.movePosition(QTextCursor.EndOfBlock, QTextCursor.KeepAnchor)  # 选中整个行
    #         cursor.removeSelectedText()
    #
    #         cursor.movePosition(QTextCursor.Up)  # 移动到上一行
    #         cursor.movePosition(QTextCursor.EndOfBlock)  # 移动到上一行的末尾
    #         self.text_lattice.setTextCursor(cursor)
    #     else:
    #         super().keyPressEvent(event)
        #To get the remaining functionality back (e.g. without this, typing would not work):


    # def wheelEvent1(self, event):
    #     if event.modifiers() & Qt.ControlModifier:  # 检测是否按下了 Ctrl 键
    #         font = self.text_lattice.font()
    #         font_size = font.pointSize()  # 获取当前字体大小
    #
    #         delta = event.angleDelta().y()  # 获取滚轮滚动的垂直距离
    #         if delta > 0:
    #             font_size += 1  # 增加字体大小
    #         else:
    #             font_size -= 1  # 减小字体大小
    #
    #         font.setPointSize(font_size)  # 设置新的字体大小
    #         self.text_lattice.setFont(font)  # 应用新的字体
    #     else:
    #         print(101)
    #         delta = event.angleDelta().y()  # 获取滚轮滚动的垂直距离
    #         scroll_bar = self.text_lattice.verticalScrollBar()
    #         scroll_bar.setValue(scroll_bar.value() - (delta-10))



    # def eventFilter(self, obj, event):
    #     if event.type() == QEvent.KeyPress:  # 使用QEvent.KeyPress
    #         if event.key() == Qt.Key_Control:
    #             self.ctrl_pressed = True
    #     elif event.type() == QEvent.KeyRelease:  # 使用QEvent.KeyRelease
    #         if event.key() == Qt.Key_Control:
    #             self.ctrl_pressed = False
    #     # print(self.ctrl_pressed)
    #     return super().eventFilter(obj, event)


    # def colorize_text(self):
    #     cursor = QTextCursor(self.text_lattice.document())
    #
    #     # 逐行着色
    #     cursor.movePosition(QTextCursor.Start)
    #
    #     while not cursor.atEnd():
    #         cursor.movePosition(QTextCursor.StartOfLine)
    #
    #         # 它将光标移动到当前行的结尾，并使用 QTextCursor.KeepAnchor参数将该行的文本内容选中，
    #         # 以便后续操作可以应用于选中的文本。
    #         cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
    #         line = cursor.selectedText().strip()  # 获取当前行文本，并移除前导和尾随空格
    #
    #         # 使用正则表达式匹配首个单词
    #         match = re.match(r'\w+', line)
    #         if match:
    #             first_word = match.group(0)
    #             char_format = QTextCharFormat()
    #
    #             if first_word == "field":
    #                 char_format.setForeground(QColor("red"))
    #             elif first_word == "drift":
    #                 char_format.setForeground(QColor("blue"))
    #             # 将char_format中定义的文本格式应用到文本游标(cursor)当前选中的文本部分。在这种情况下，您使用char_format设置了文本的颜色。
    #             else:
    #                 char_format.setForeground(QColor("black"))
    #             cursor.mergeCharFormat(char_format)
    #         cursor.movePosition(QTextCursor.NextBlock)
    #
    # def cursorPositionChanged(self):
    #     cursor = self.text_lattice.textCursor()
    #     line_number = cursor.blockNumber()  # 获取当前行号
    #     column_number = cursor.columnNumber()  # 获取当前列号
    #
    #     # 获取光标所在行的文本
    #     cursor.movePosition(QTextCursor.StartOfBlock)  # 移动到当前行的开头
    #     cursor.movePosition(QTextCursor.EndOfBlock, QTextCursor.KeepAnchor)  # 选中整个行
    #     line = cursor.selectedText().strip()   # 获取整行文本
    #
    #     match = re.match(r'\w+', line)
    #     if match:
    #         first_word = match.group(0)
    #         char_format = QTextCharFormat()
    #
    #         if first_word == "field":
    #             char_format.setForeground(QColor("red"))
    #         elif first_word == "drift":
    #             char_format.setForeground(QColor("blue"))
    #         else:
    #             char_format.setForeground(QColor("black"))
    #         # 将char_format中定义的文本格式应用到文本游标(cursor)当前选中的文本部分。在这种情况下，您使用char_format设置了文本的颜色。
    #         cursor.mergeCharFormat(char_format)
    #
    #     print(f"光标位置 - 行: {line_number + 1}")
    #     print(f"行文本: {line}")

    # @treat_err
    def updatePath(self, new_path):
        self.project_path = new_path
        self.lattice_mulp_path = os.path.join(self.project_path, "InputFile", "lattice_mulp.txt")
        self.lattice_env_path = os.path.join(self.project_path, "InputFile", "lattice_env.txt")

    # @treat_err
    def fill_parameter(self):

        if os.path.exists(self.lattice_mulp_path):
            self.stacked_widget.setCurrentWidget(self.text_lattice)
            self.lattice_mulp_path = os.path.join(self.project_path, 'InputFile', 'lattice_mulp.txt')
            # print(self.lattice_path)
            self.text_file_path.setText(self.lattice_mulp_path)

            with open(self.lattice_mulp_path, 'r', encoding='utf-8') as file:
                file_contents = file.read()

            self.text_lattice.setPlainText(file_contents, mime_type="text/plain", encoding='utf-8')
            self.button_lattice.setChecked(True)
            self.button_state()

        if os.path.exists(self.lattice_env_path):
            self.lattice_env_path = os.path.join(self.project_path, 'InputFile', 'lattice_env.txt')
            self.text_file_path.setText(self.lattice_env_path)

            if not os.path.exists(self.lattice_env_path):
                with open(self.lattice_env_path, 'w', encoding='utf-8') as file:
                    file.write("")

            with open(self.lattice_env_path, 'r', encoding='utf-8') as file:
                file_contents = file.read()

            self.text_match_lattice.setPlainText(file_contents)


    @treat_err
    def save_file(self):
        if not self.project_path:
            return None
        current_index = self.stacked_widget.currentIndex()

        if current_index == 0:
            path = self.lattice_mulp_path
            text = self.text_lattice.toPlainText()
        elif current_index == 1:
            path = self.lattice_env_path
            text = self.text_match_lattice.toPlainText()
        else:
            return None
        # 打开文件以写入数据
        with open(path, 'w', encoding='utf-8') as file:
            # 遍历嵌套列表的每个子列表
            file.write(text)

    @treat_err
    def save_all_lattice(self):
        path = self.lattice_mulp_path
        text = self.text_lattice.toPlainText()
        if os.path.exists(path):
            with open(path, 'w', encoding='utf-8') as file:
                # 遍历嵌套列表的每个子列表
                file.write(text)
        else:
            pass

        path = self.lattice_env_path
        #如果路径为空, 那么不保存
        if os.path.exists(path):
            text = self.text_match_lattice.toPlainText()
            with open(path, 'w',encoding='utf-8') as file:
                # 遍历嵌套列表的每个子列表
                file.write(text)
        else:
            pass

    # @treat_err
    def fill_text_lattice_path(self, path):
        self.text_lattice_path.setText(path)

    # @treat_err
    def lattice_click(self):
        if not self.project_path:
            pass
        else:
            self.button_state()

            self.stacked_widget.setCurrentWidget(self.text_lattice)
            # self.lattice_mulp_path = os.path.join(self.project_path, 'InputFile', 'lattice_mulp.txt')
            # self.text_file_path.setText(self.lattice_mulp_path)
            #
            # with open(self.lattice_mulp_path, 'r', encoding='utf-8') as file:
            #     file_contents = file.read()
            #
            # self.text_lattice.setPlainText(file_contents, mime_type="text/plain", encoding='utf-8')

    @treat_err
    def match_lattice_click(self):
        if not self.project_path:
            pass
        else:
            self.button_state()
            self.stacked_widget.setCurrentWidget(self.text_match_lattice)
            # self.lattice_env_path = os.path.join(self.project_path, 'InputFile', 'lattice_env.txt')
            # self.text_file_path.setText(self.lattice_env_path)
            #
            # if not os.path.exists(self.lattice_env_path):
            #     with open(self.lattice_env_path, 'w', encoding='utf-8') as file:
            #         file.write("")
            #
            # with open(self.lattice_env_path, 'r', encoding='utf-8') as file:
            #     file_contents = file.read()
            #
            # self.text_match_lattice.setPlainText(file_contents)


    @treat_err
    def input_twiss_click(self):
        if not self.project_path:
            pass
        else:
            self.button_state()
            self.stacked_widget.setCurrentWidget(self.text_input_twiss)
            self.input_twiss_path = os.path.join(self.project_path, 'OutputFile', 'env_input_twiss.txt')
            self.text_file_path.setText(self.input_twiss_path)

            if not os.path.exists(self.input_twiss_path):
                return 0

            with open(self.input_twiss_path, 'r', encoding='utf-8') as file:
                file_contents = file.read()
                self.text_input_twiss.setPlainText(file_contents)

    # @treat_err
    def button_state(self):
        button = self.sender()
        if button is None:
            button = self.button_lattice
        # print(button)

        if button.isChecked():
            for other_button in self.button_group.buttons():
                if other_button is not button:
                    other_button.setChecked(False)


        # 自定义选中按钮的样式
        for btn in self.button_group.buttons():
            if btn.isChecked():
                btn.setStyleSheet("background-color: rgb(240, 240, 240); ")
            else:
                btn.setStyleSheet("")  # 恢复默认样式
    def inspect(self):
        pass
        return True
    # def color_text_by_starting_word(self, text):
    #     cursor = QTextCursor(self.text_lattice.document())
    #     cursor.beginEditBlock()
    #
    #     lines = text.split('\n')
    #
    #     for line in lines:
    #         words = line.split()
    #         if words:
    #             first_word = words[0]
    #             if first_word == "drift":
    #                 format = QTextCharFormat()
    #                 format.setForeground(QColor('blue'))
    #                 cursor.setCharFormat(format)
    #                 cursor.insertText(line)
    #
    #             elif first_word == "field":
    #                 format = QTextCharFormat()
    #                 format.setForeground(QColor('green'))
    #                 cursor.setCharFormat(format)
    #                 cursor.insertText(line)
    #             else:
    #                 format = QTextCharFormat()
    #                 format.setForeground(QColor('black'))
    #                 cursor.setCharFormat(format)
    #                 cursor.insertText(line)
    #
    #         else:
    #             cursor.insertText(line)
    #
    #         cursor.insertBlock()
    #
    #     cursor.endEditBlock()
    #
    # def color_new_text_by_starting_word(self):
    #     # 防止触发无限循环
    #     if not self.ignore_text_changed:
    #         self.ignore_text_changed = True
    #         # 获取新输入的文本
    #         new_text = self.text_lattice.toPlainText()
    #         self.text_lattice.clear()  # 清除文本框内容
    #         self.color_text_by_starting_word(new_text)  # 调用颜色处理函数处理新文本
    #         self.ignore_text_changed = False  # 重新允许文本更改信号触发
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     main_window = PageLattice(r'C:\Users\anxin\Desktop\test')
#     main_window.setGeometry(800, 500, 600, 650)
#     main_window.setStyleSheet("background-color: rgb(253, 253, 253);")
#     main_window.show()
#     sys.exit(app.exec_())
