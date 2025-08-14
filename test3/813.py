from PyQt5 import QtWidgets, QtCore

class CollapsibleSection(QtWidgets.QWidget):
    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self.toggle = QtWidgets.QToolButton(text=title, checkable=True, checked=False)
        self.toggle.setStyleSheet("QToolButton { border: none; font-weight: 600; }")
        self.toggle.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toggle.setArrowType(QtCore.Qt.RightArrow)
        self.toggle.toggled.connect(self.on_toggled)

        self.body = QtWidgets.QWidget()
        self.body.setVisible(False)
        self.body.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.body_layout = QtWidgets.QFormLayout(self.body)
        # 方便外部通过 section.form 添加行
        self.form = self.body_layout

        lay = QtWidgets.QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self.toggle)
        lay.addWidget(self.body)

    def on_toggled(self, checked):
        self.toggle.setArrowType(QtCore.Qt.DownArrow if checked else QtCore.Qt.RightArrow)
        self.body.setVisible(checked)

class SettingsPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        v = QtWidgets.QVBoxLayout(self)
        self.search = QtWidgets.QLineEdit(placeholderText="搜索设置…")
        v.addWidget(self.search)

        # 滚动区域
        scroll = QtWidgets.QScrollArea(widgetResizable=True)
        v.addWidget(scroll)
        container = QtWidgets.QWidget()
        scroll.setWidget(container)
        self.container_layout = QtWidgets.QVBoxLayout(container)

        # —— 示例分组 1：运行设置
        sec_run = CollapsibleSection("运行设置")
        sec_run.toggle.setChecked(True)
        sec_run.form.addRow("多粒子(Multi_particles)：", QtWidgets.QCheckBox())
        sec_run.form.addRow("SPICNIC：", QtWidgets.QCheckBox())
        phase = QtWidgets.QComboBox(); phase.addItems(["Scan Phase","Fixed Phase","Auto"])
        sec_run.form.addRow("Scan Phase：", phase)
        calc_step = QtWidgets.QSpinBox(); calc_step.setRange(1, 10_000); calc_step.setValue(100)
        sec_run.form.addRow("Calculation step(βλ)：", calc_step)
        self.container_layout.addWidget(sec_run)

        # —— 示例分组 2：空间电荷
        sec_sc = CollapsibleSection("空间电荷")
        chk_sc = QtWidgets.QCheckBox("启用空间电荷计算")
        sec_sc.form.addRow(chk_sc)
        grid = QtWidgets.QSpinBox(); grid.setRange(16, 2048); grid.setValue(300)
        step = QtWidgets.QDoubleSpinBox(); step.setRange(0.0, 10.0); step.setDecimals(4); step.setSuffix(" m")

        grid = QtWidgets.QTextEdit()
        step = QtWidgets.QTextEdit()

        sec_sc.form.addRow("Density grid：", grid)
        sec_sc.form.addRow("Space-charge step：", step)
        # 勾选才启用子项
        def on_sc_toggled(b):
            for i in range(1, sec_sc.form.rowCount()):
                w = sec_sc.form.itemAt(i, QtWidgets.QFormLayout.FieldRole).widget()
                if w: w.setEnabled(b)
        chk_sc.toggled.connect(on_sc_toggled)
        on_sc_toggled(False)
        self.container_layout.addWidget(sec_sc)

        # 占位伸展
        self.container_layout.addStretch(1)

        # 搜索过滤（按标题和行标签）
        def filter_sections(text):
            text = text.strip().lower()
            for i in range(self.container_layout.count()-1):
                w = self.container_layout.itemAt(i).widget()
                if not isinstance(w, CollapsibleSection): continue
                title_hit = text in w.toggle.text().lower()
                row_hit = any(text in (w.form.itemAt(row, QtWidgets.QFormLayout.LabelRole).widget().text().lower())
                              for row in range(w.form.rowCount())
                              if w.form.itemAt(row, QtWidgets.QFormLayout.LabelRole))
                w.setVisible(text == "" or title_hit or row_hit)
        self.search.textChanged.connect(filter_sections)

class Main(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("设置示例")
        h = QtWidgets.QHBoxLayout(self)

        # 左侧目录
        self.list = QtWidgets.QListWidget()
        self.list.addItems(["常规", "高级"])
        self.list.setFixedWidth(140)
        h.addWidget(self.list)

        # 右侧堆叠页
        self.stack = QtWidgets.QStackedWidget()
        h.addWidget(self.stack, 1)
        self.stack.addWidget(SettingsPage())   # 常规
        self.stack.addWidget(SettingsPage())   # 高级（示意，可换成别的页）

        self.list.currentRowChanged.connect(self.stack.setCurrentIndex)
        self.list.setCurrentRow(0)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Main(); w.resize(900, 600); w.show()
    sys.exit(app.exec_())
