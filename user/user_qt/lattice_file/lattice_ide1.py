from PyQt5.QtGui import QTextCharFormat, QColor, QTextDocument

from pyqode.core import api

from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QKeyEvent, QTextCursor
from PyQt5.QtWidgets import QApplication, QDialog, QLineEdit, QPushButton, QVBoxLayout, QTextEdit, QApplication


class CustomCodeEdit(api.CodeEdit):
    def __init__(self):
        self.i = 0
        super().__init__()

    def wheelEvent(self, event):
        if event.modifiers() & Qt.ControlModifier:
            font = self.font()
            font_size = font.pointSize()

            delta = event.angleDelta().y()
            if delta > 0:
                font_size += 1
            else:
                font_size -= 1

            font.setPointSize(font_size)
            self.setFont(font)
        else:
            delta = event.angleDelta().y()
            scroll_bar = self.verticalScrollBar()
            scroll_bar.setValue(scroll_bar.value() - int(delta/40))

    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress:
            if isinstance(event, QKeyEvent) and event.key() == Qt.Key_F and event.modifiers() & Qt.ControlModifier:

                # 按下 Ctrl+F，弹出搜索窗口
                search_dialog = SearchDialog(self)
                search_dialog.exec_()
                return True


            #专门处理折叠
            if 1:
                is_fold_trigger = False
                fold_state = False
                cursor = self.textCursor()
                if api.utils.TextBlockHelper.is_fold_trigger(cursor.block()):
                    is_fold_trigger = True

                    fold_scope = api.folding.FoldScope(cursor.block())
                    if fold_scope.collapsed:
                        fold_state = True
                    else:
                        fold_state = False

                if fold_state:
                    if isinstance(event, QKeyEvent) and event.key() == Qt.Key_C and event.modifiers() & Qt.ControlModifier:
                        print(50)
                        cursor = self.textCursor()
                        fold_scope = api.folding.FoldScope(cursor.block())
                        start, end = fold_scope.get_range(ignore_blank_lines=False)

                        cursor.movePosition(QTextCursor.StartOfLine)  # 移动到当前行的开头
                        cursor.movePosition(QTextCursor.Down, QTextCursor.KeepAnchor,
                                            end - start+1)  # 从当前行向下移动到第 (end - start) 行并选择文本

                        selected_text = cursor.selectedText()

                        clipboard = QApplication.clipboard()
                        clipboard.setText(selected_text)

                        self.setTextCursor(cursor)
                        return True


                    elif event.key() == Qt.Key_Control:
                        pass
                        return True

                    elif event.key() == Qt.Key_Return:

                        cursor = self.textCursor()
                        # 当内容折叠时，选中整个折叠区域的内容
                        fold_scope = api.FoldScope(cursor.block())
                        start, end = fold_scope.get_range(ignore_blank_lines=False)

                        cursor.movePosition(QTextCursor.StartOfLine)  # 移动到当前行的开头
                        cursor.movePosition(QTextCursor.Down, QTextCursor.MoveAnchor,
                                            end - start + 1)  # 从当前行向下移动到第 (end - start) 行并选择文本


                        self.setTextCursor(cursor)  # 将光标设置回文本编辑器
                        return True


                    else:
                        return super().eventFilter(obj, event)
                else:
                    return super().eventFilter(obj, event)
        else:
            return super().eventFilter(obj, event)
class SearchDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.editor = parent  # 传入文本编辑器对象
        self.setWindowTitle("搜索")

        # 创建搜索框
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("输入搜索内容...")
        self.search_input.returnPressed.connect(self.find_text)  # 按下回车搜索

        # 创建按钮
        self.search_button = QPushButton("查找", self)
        self.search_button.clicked.connect(self.find_text)

        # 布局
        layout = QVBoxLayout()
        layout.addWidget(self.search_input)
        layout.addWidget(self.search_button)
        self.setLayout(layout)

    def find_text(self):
        """执行搜索"""
        search_text = self.search_input.text()
        if search_text:
            self.editor.find(search_text, QTextDocument.FindCaseSensitively)  # 查找匹配项

class MySyntaxHighlighter(api.SyntaxHighlighter):
    def __init__(self, editor):
        super().__init__(editor)

    def highlight_block(self, text, block):
        char_format = QTextCharFormat()

        # 获取每行的文本
        line = text.strip()

        # 使用正则表达式匹配第一个单词
        import re
        match = re.match(r'!?\b\w+\b', line)

        if match:
            first_word = match.group(0)
            if first_word == "field":
                char_format.setForeground(QColor("red"))
            elif first_word == "drift":
                # print('drift')
                char_format.setForeground(QColor("blue"))
            elif first_word.startswith('!'):
                # print("在 '!' 块内")
                char_format.setForeground(QColor("gray"))
            else:
                char_format.setForeground(QColor("black"))

            # 将char_format中定义的文本格式应用到整行文本
            self.setFormat(0, len(text), char_format)


class MyFoldDetector(api.FoldDetector):

    def detect_fold_level(self, prev_block, block):
        """
        自定义折叠级别检测逻辑

        :param prev_block: 前一个文本块
        :param block: 当前文本块
        :return: 折叠级别
        """
        # 获取文本块的文本内容
        text = block.text().strip()

        #自定义折叠触发条件
        if "MODULE" in text:
            return 0  # 一级折叠
        elif "CELL" in text:
            return 1  # 二级折叠
        # 默认情况
        return 2
        # if "fold" in text:
        #     return 0  # 一级折叠
        # else:
        #     return 2
        # elif "CELL" in text:
        #     return 1  # 二级折叠
        # # 默认情况
        # return 2
    # def detect_fold_level(self, prev_block, block):
    #     """
    #     Detects fold level by looking at the block indentation.
    #
    #     :param prev_block: previous text block
    #     :param block: current block to highlight
    #     """
    #     text = block.text()
    #     # round down to previous indentation guide to ensure contiguous block
    #     # fold level evolution.
    #     return (len(text) - len(text.lstrip())) // self.editor.tab_length

    # def get_folded_content(self):
    #     # Find the parent scope of the current cursor position
    #     cursor = self.editor.textCursor()
    #     current_block = cursor.block()
    #     fold_scope = api.folding.FoldScope.parent()
    #
    #     if fold_scope:
    #         # Get the text content of the fold scope
    #         folded_content = fold_scope.text()
    #         # Output the folded content or use it as needed
    #         print(folded_content)