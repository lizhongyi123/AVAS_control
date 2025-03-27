#列出需要打包的所有文件

from utils.treat_directory import list_files_in_directory
import os

if __name__ == "__main__":
    AVAS_path = r"C:\Users\anxin\Desktop\AVAS_control"
    files = [ "aftertreat\picture", "aftertreat\dataanalysis", r"apis\basic_api", r"apis\qt_api",
              "apps",
              "core", "dataprovision", "otherdemand",
              r"user\user_qt", r"user\user_qt\lattice_file", r"user\user_qt\page_utils",
              "utils"]

    # files = [
    #     r"user\user_qt"
    #     , r"user\user_qt\lattice_file", r"user\user_qt\page_utils",
    # ]

    all_files = list_files_in_directory(AVAS_path)
    v1 = []
    for i in files:
        path = os.path.join(AVAS_path, i)
        res = list_files_in_directory(path)
        v1 = v1 + res
    # print(v1)
    # print(v1[0])
    new_path = updated_paths = [path.replace('C:/Users/anxin/Desktop/AVAS_control', '.') for path in v1]
    new_path = updated_paths = [path.replace('\\', r'/') for path in new_path]
    new_path = updated_paths = [path.replace('\\', r'/') for path in new_path if "__pycache__" not in path]
    # print(new_path)
    for i in new_path:
        print(f"'{i}',")