# class CfgConfig():
#     def __init__(self, cfg_path):
#         self.cfg_path = cfg_path
#
#     def read_cfg(self):
#
import configparser
import os


class IniConfig():
    def __init__(self, ini_path):
        self.ini_path = ini_path

    def initialize(self):

        ini_dict = \
        {"project": {"project_path": 0},
        "lattice":{"length": 0},
         "input": {"sim_type": 0},
         "match": {"cal_input_twiss": 0, "match_with_twiss": 0, "use_initial_value": 0},
         "error": {"error_type": 0, "seed": 0},
         }
        return ini_dict

    def read_ini(self):
        """
        读取 INI 文件并返回其内容作为一个字典。

        :return: 包含 INI 文件内容的字典
        """
        if not os.path.exists(self.ini_path):
            print(f"文件路径 {self.ini_path} 不存在。")
            return {}

        config = configparser.ConfigParser()
        config.read(self.ini_path, encoding='utf-8')  # 确保文件以正确的编码读取

        ini_dict = {}
        for section in config.sections():
            ini_dict[section] = {}
            for key, value in config.items(section):
                ini_dict[section][key] = value

        return ini_dict


    def write_ini(self, ini_dict):
        """
        将字典内容写入 INI 文件。

        :param ini_dict: 包含 INI 文件内容的字典
        :param output_path: 输出 INI 文件的路径
        """
        config = configparser.ConfigParser()

        for section, section_data in ini_dict.items():
            config[section] = section_data

        with open(self.ini_path, 'w', encoding='utf-8') as configfile:
            config.write(configfile)

# 示例用法


# file_path = r'C:\Users\shliu\Desktop\78\InputFile\78.ini'  # 替换为你的 INI 文件路径
# cfg = IniConfig(file_path)
# ini_dict = cfg.initialize()
# cfg.write_ini(ini_dict)

