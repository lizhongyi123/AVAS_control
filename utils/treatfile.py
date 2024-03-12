import shutil
import os
# from treat_directory import list_files_in_directory

# 复制文件到目标文件夹
def copy_file(source_file, target_folder):
    shutil.copy(source_file, target_folder)

def split_file(file_path):
    # 将文件路径使用"/"进行分割
    parts = file_path.split('/')
    # 对每个部分再次使用"\\"进行分割，并将结果扁平化
    parts = [subpart for part in parts for subpart in part.split('\\')]
    return parts

# if __name__ == "__main__":
#     project_path = r'C:/Users/anxin/Desktop/comparison/avas'
#     target_folder = os.path.join(project_path, "InputFile")
#     print(target_folder)
#     relative_dst_file_path = split_file(target_folder)
#     print(relative_dst_file_path)
#
#     # print(list_files_in_directory(target_folder))
#     v1 = list_files_in_directory(target_folder)[0]
#     print(v1)
#     v2 = split_file(v1)
#     print(v2)
