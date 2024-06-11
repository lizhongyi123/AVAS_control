import os
import shutil
from send2trash import send2trash
def list_files_in_directory(directory):
    """
    查找一个文件夹下面的所有文件
    :param directory:
    :return:【】
    """
    files = []
    for root, _, file_names in os.walk(directory):
        for file_name in file_names:
            files.append(os.path.join(root, file_name))
        break

    files1 = []
    for root, _, file_names in os.walk(directory):
        files1.append(root)
    files += files1[1:]
    return files

# folder_path = r'C:\Users\anxin\Desktop\test_control\test_error\OutputFile\stat_error_middle\output_0'  # 将此路径替换为您要遍历的文件夹路径
#
# files = list_files_in_directory(folder_path)

def copy_directory(source_folder, destination_folder, new_name=None):
    """
    复制一个文件夹
    :param source_folder:
    :param destination_folder:
    :param new_name:
    :return:
    """
    # 修改目标文件夹的名字
    if not new_name:
        destination_folder = os.path.join(destination_folder, source_folder.split("\\")[-1])
    else:
        destination_folder = os.path.join(destination_folder, new_name)

    shutil.copytree(source_folder, destination_folder)

def delete_directory(path):
    """
    删除一个文件夹
    :param path:
    :return:
    """
    send2trash(path)
    # shutil.rmtree(path)
if __name__ == "__main__":

    path = r"C:\Users\anxin\Desktop\test_mulp\OutputFile\error_output"
    res = list_files_in_directory(path)
    print(res)