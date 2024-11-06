

import configparser
import os

class IniConfig():
    def __init__(self):
        self.ini_parameter = \
        {"project": {"project_path": "undefined"},
        "lattice":{"length": 0},
         "input": {"sim_type": 0},
         "match": {"cal_input_twiss": 0, "match_with_twiss": 0, "use_initial_value": 0},
         "error": {"error_type": "undefined", "seed": 0, "if_normal": 0},
         }
        self.str_keys = ["sim_type", "project_path", "error_type"]
    # def initialize_ini(self):


    def creat_from_file(self, path):
        """
        读取 INI 文件并返回其内容作为一个字典。

        :return: 包含 INI 文件内容的字典
        """
        if not os.path.exists(path):
            print(f"文件路径 {path} 不存在。")
            return False

        config = configparser.ConfigParser()
        config.read(path, encoding='utf-8')  # 确保文件以正确的编码读取

        for section in config.sections():
            for key, value in config.items(section):
                if key not in self.str_keys:
                    self.ini_parameter[section][key] = int(value)
                else:
                    self.ini_parameter[section][key] = value

        return self.ini_parameter

    def set_param(self, **kwargs):

        """
        更新 INI 文件中的值。

        :param kwargs: 字典格式的键值对，用于更新 INI 文件
        """
        for section, values in kwargs.items():
            if section in self.ini_parameter:
                self.ini_parameter[section].update(values)
            else:
                print(f"节 {section} 不存在。")

        return self.ini_parameter

    def write_to_file(self, path):
        """
        将字典内容写入 INI 文件。

        :param ini_dict: 包含 INI 文件内容的字典
        :param output_path: 输出 INI 文件的路径
        """
        config = configparser.ConfigParser()

        for section, section_data in self.ini_parameter.items():
            config[section] = section_data

        with open(path, 'w', encoding='utf-8') as configfile:
            config.write(configfile)

        return True

# 示例用法

if __name__ == '__main__':
    file_path = r"C:\Users\shliu\Desktop\eee\InputFile\ini.ini"  # 替换为你的 INI 文件路径
    cfg = IniConfig()
    res = cfg.creat_from_file(file_path)
    print(res)
    # cfg.write_to_file(file_path)

    cfg.set_ini(
        project={"project_path": "C:/new/path"},
        lattice={"length": 100},
        match={"use_initial_value": 1}
    )
    #
    #
    # print(cfg.ini_dict)
    # ini_dict = cfg.initialize()
    # cfg.write_ini(ini_dict)

