from utils.initilaconfig import InitialConfig

class InputConfig(InitialConfig):
    def __init__(self):
        super().__init__(self.path)

    # 将整个人文件格式化
    def format_file(self):
        pass

    # 将变化的内容格式化
    def format_change(self):
        pass

    # 将变化的内容更新进整个文件格式化后结果
    def update(self):
        pass
