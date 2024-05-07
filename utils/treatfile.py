import shutil
import os
from utils.treat_directory import list_files_in_directory
import time
from datetime import datetime
# 复制文件到目标文件夹
def copy_file(source_file, target_folder):
    shutil.copy(source_file, target_folder)

#将文件切割成一个个列表（/ \）
def split_file(file_path):
    # 将文件路径使用"/"进行分割
    parts = file_path.split('/')
    # 对每个部分再次使用"\\"进行分割，并将结果扁平化
    parts = [subpart.lower() for part in parts for subpart in part.split('\\')]
    return parts

# 判断哪一个文件是否在文件夹中():
def file_in_directory(file, directory):
    file_list = split_file(file)
    directory_list = [split_file(i) for i in list_files_in_directory(directory)]
    print(file_list, directory_list)
    if file_list in directory_list:
        return True
    else:
        return False


def check_file_update(file_path):
    """
    检查指定文件的最后修改时间。

    参数:
    file_path (str): 文件的完整路径。

    返回:
    str: 文件最后修改时间的人类可读字符串，如果文件不存在则返回错误信息。
    """
    # 检查文件是否存在
    if os.path.exists(file_path):
        # 获取文件的最后修改时间
        last_modified_time = os.stat(file_path).st_mtime
        now = datetime.now().timestamp()
        if now - last_modified_time <= 0.1:
            #正在更新
            return 1
        else:
            #停止更新
            return 0

    else:
        #"文件不存在"
        return 2

if __name__ == "__main__":
    # project_path = r'C:/Users/anxin/Desktop/comparison/avas'
    # target_folder = os.path.join(project_path, "InputFile")
    # print(target_folder)
    # relative_dst_file_path = split_file(target_folder)
    # print(relative_dst_file_path)
    #
    # # print(list_files_in_directory(target_folder))
    # v1 = list_files_in_directory(target_folder)[0]
    # print(v1)
    # v2 = split_file(v1)
    # print(v2)
    p1 = r"C:\Users\anxin\Desktop\test_zhao/inputFile/beam.txt"
    p2 = r"C:/Users/anxin/Desktop/comparison/avas_test\InputFile"
    p3 = r"C:\Users\anxin\Desktop\test_zhao/OutputFile/DataSet.txt"

    res = check_file_update(p3)
    # # res = file_in_directory(p1,p2)
    print(res)
