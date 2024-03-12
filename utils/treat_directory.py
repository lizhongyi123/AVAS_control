import os
import shutil

def list_files_in_directory(directory):
    """
    查找一个文件夹下面的所有文件
    :param directory:
    :return:【】
    """
    files = []
    for root, _, file_names in os.walk(directory):
        # print(root)
        # print(file_names)
        # print(file_names)
        for file_name in file_names:
            files.append(os.path.join(root, file_name))
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
    shutil.rmtree(path)
if __name__ == "__main__":
    project_path = r'C:/Users/anxin/Desktop/comparison/avas'
    target_folder = os.path.join(project_path, "InputFile")
    print(target_folder)
    relative_dst_file_path = target_folder.split("/")
    print(relative_dst_file_path)

    print(list_files_in_directory(target_folder))
    v1 = list_files_in_directory(target_folder)[0]
    print(v1)
    v2 = v1.split("\\")
    print(v2)